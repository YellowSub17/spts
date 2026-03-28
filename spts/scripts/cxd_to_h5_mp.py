#!/usr/bin/env python
import argparse
import os
import sys
import olefile
import numpy as np

import scipy
from scipy.ndimage import percentile_filter
import scipy.ndimage


import os
# import h5writer
import h5py
import spts
import spts.camera
from spts.camera import CXDReader
import matplotlib.pyplot as plt
import matplotlib.cm
import matplotlib.patches
from matplotlib.colors import LogNorm
import time

import multiprocessing as mp


from cxd_to_h5 import estimate_background, estimate_flatfield, guess_ROI


def cxd_to_h5_mp(worker_input):

    p_id, n_processes, filename_cxd,  bg, ff, roi, good_pixels, filename_cxi,  skip_raw = worker_input


    # W = h5writer.H5Writer(f'{filename_cxi}.part{p_id}')


    if p_id==0:
        print("*************************************")
        print("*   Particle conversion section     *")
        print("*************************************")
        print("Opening %s" % filename_cxd)
    R = CXDReader(filename_cxd)

    N_total = R.get_number_of_frames()
    frame_0 = R.get_frame(0)  # dtype: uint16
    frame_crop = frame_0[roi]*good_pixels[roi]
    frame_h, frame_w = frame_crop.shape


    if(good_pixels is None):
        if p_id==0:
            print("Warning: Good pixels information is missing. Using all the pixels.")
        good_pixels = np.ones_like(frame)


    # Initialise integration variables
    integrated_raw = None
    integrated_image = None
    integratedsq_raw = None
    integratedsq_image = None



    this_worker_frames = np.array_split(np.arange(0, N_total), n_processes)[p_id]

    N_frames = len(this_worker_frames)


    with h5py.File(f'{filename_cxi}.part{p_id}', 'w') as f:
        f.create_dataset("entry_1/data_1/data",
                shape = (N_frames, frame_h, frame_w),
                dtype=np.float32, ##uint16?
                chunks= (1, frame_h, frame_w)
                )
        f.create_dataset("entry_1/image_1/data",
                shape = (N_frames, frame_h, frame_w),
                dtype=np.float16, ###float32?
                chunks= (1, frame_h, frame_w)
                )


    for i, frame_i in enumerate(this_worker_frames):

        if p_id==0:
            print(f'({i+1}/{N_frames}) Writing frames...', end='\r')

        frame = R.get_frame(frame_i)



        image_raw = frame[roi]*good_pixels[roi]

        bg_corr = bg[roi]
        image_bgcor = ((image_raw.astype(np.float32) -
                           bg_corr.astype(np.float32)).astype(np.float32))*good_pixels[roi]


        with h5py.File(f'{filename_cxi}.part{p_id}', 'a') as f:
            dset = f["entry_1/data_1/data"]
            dset[i,:,:] = image_raw.astype(np.float32)

            dset = f["entry_1/image_1/data"]
            dset[i,:,:] = image_bgcor.astype(np.float16)


        if integrated_raw is None:
            integrated_raw = np.zeros(shape=image_raw.shape, dtype='float32')
        if integratedsq_raw is None:
            integratedsq_raw = np.zeros(shape=image_raw.shape, dtype='float32')
        integrated_raw += np.asarray(image_raw, dtype='float32')
        integratedsq_raw += np.asarray(image_raw, dtype='float32')**2

        if(bg_corr is not None):
            if integrated_image is None:
                integrated_image = np.zeros(
                    shape=image_bgcor.shape, dtype='float32')
            if integratedsq_image is None:
                integratedsq_image = np.zeros(
                    shape=image_bgcor.shape, dtype='float32')
            integrated_image += image_bgcor
            integratedsq_image += np.asarray(image_bgcor, dtype='f')**2



    out = {"entry_1": {"data_1": {}, "image_1": {}}}

    with h5py.File(f'{filename_cxi}.part{p_id}', 'a') as f:
        f["entry_1/data_1/data_mean"] = integrated_raw
        f["entry_1/image_1/data_mean"] = integrated_image

        f["entry_1/data_1/datasq_mean"] = integratedsq_raw
        f["entry_1/image_1/datasq_mean"] = integratedsq_image


    R.close()







if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Conversion of CXD (Hamamatsu file format) to HDF5')
    parser.add_argument('filename', type=str, nargs='?',
                        help='CXD filename of the particle scattering data.')
    parser.add_argument('-b', '--background-filename', type=str,
                        help='CXD filename with photon background data (no injection).')
    parser.add_argument('-bn', '--bg-frames-max', type=int,
                        help='Maximum number of frames used for background calculation.', default=100)

    parser.add_argument('-f', '--flatfield-filename', type=str,
                        help='CXD filename with flat field correction (laser on paper) data.')
    parser.add_argument('-fn', '--ff-frames-max', type=int,
                        help='Maximum number of frames used for flatfield calculation.', default=100)

    parser.add_argument('-rl', '--roi-low-limit', type=int,
                        help='Miminum intensity threshold for ROI calculations from flatfield.', default=10)
    parser.add_argument('-rf', '--roi-fraction', type=int,
                        help='Fraction of intensity above threshold to include in ROI.', default=0.999)

 
    parser.add_argument('-o', '--out-filename', type=str,
                        help='destination file')
    parser.add_argument('-s', '--skip-raw', action='store_true',
                        help='Skip saving the raw data, instead linking to processed data')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="Don't show plots interactively")

    parser.add_argument('-rc', '--read-cache', action='store_true',
                        help="Read and use the cache")

    parser.add_argument('-np', '--n-processes', type=int,
                        help='Number of processes to run.', default=1)

    args = parser.parse_args()

    print(f'Running with {args.n_processes}.')




    bg_mean, good_pixels = estimate_background(
        args.background_filename, args.bg_frames_max, args.read_cache)

    ff = estimate_flatfield(
        args.flatfield_filename, args.ff_frames_max, bg_mean, good_pixels)

    roi = guess_ROI(ff, args.flatfield_filename,
                    args.roi_low_limit, args.roi_fraction)

    if(args.filename is None):
        sys.exit(0)

    if not args.filename.endswith(".cxd"):
        print("ERROR: Given filename %s does not end with \".cxd\". Wrong format!" %
              args.filename)
        sys.exit(-1)

    if args.out_filename:
        f_out = args.out_filename
    else:
        f_out = args.filename[:-4] + ".cxi"




    tasks = [
        (p_id, args.n_processes, args.filename,  bg_mean, ff, roi, good_pixels, f_out, args.skip_raw)
            for p_id in range(args.n_processes)
            ]





    t1 = time.time()
    with mp.Pool(processes=args.n_processes) as pool:
        pool.map(cxd_to_h5_mp, tasks)
    t2 = time.time()
    print(f'Time taken to make parts: {round((t2-t1)/60, 3)} minutes.')



    # part_files = [ for p_id in range(args.n_processes)]

    #datasets to concatenate
    concat_dsets = ['/entry_1/data_1/data', '/entry_1/image_1/data']

    sum_dsets = [ "/entry_1/data_1/data_mean",
    "/entry_1/data_1/datasq_mean",
    "/entry_1/image_1/data_mean",
    "/entry_1/image_1/datasq_mean"]

# --- Open all input files ---
    in_files = [h5py.File(f'{f_out}.part{p_id}', "r") for p_id in range(args.n_processes)]

    with h5py.File(f_out, "w") as fout:

        # --------------------------------------------------
        # 1. CONCATENATED DATASETS (3D)
        # --------------------------------------------------
        for path in concat_dsets:
            # Inspect shapes
            shapes = [f[path].shape for f in in_files]
            dtype = in_files[0][path].dtype

            total_frames = sum(s[0] for s in shapes)
            H, W = shapes[0][1:]

            # Ensure groups exist
            grp_path, name = path.rsplit("/", 1)
            grp = fout.require_group(grp_path)

            dset_out = grp.create_dataset(
                name,
                shape=(total_frames, H, W),
                dtype=dtype,
                chunks=(1, H, W),
            )

            offset = 0
            for i_f, f in enumerate(in_files):
                print(f'Concatenating {path} from part {i_f}.')
                d = f[path]
                n = d.shape[0]
                dset_out[offset:offset+n] = d[...]
                offset += n


        N_total = f[path].shape[0]
        # --------------------------------------------------
        # 2. SUMMED DATASETS (2D)
        # --------------------------------------------------
        for path in sum_dsets:

            print(f'Summing {path} from parts.')
            d0 = in_files[0][path]
            shape = d0.shape
            dtype = d0.dtype

            grp_path, name = path.rsplit("/", 1)
            grp = fout.require_group(grp_path)

            dset_out = grp.create_dataset(
                name,
                shape=shape,
                dtype=dtype,
            )

            # initialize to zero
            dset_out[...] = 0

            for f in in_files:
                dset_out[...] += f[path][...]


            dset_out[...] /= float(N_total)



# Close input files
    for f in in_files:
        f.close()

    t3 = time.time()
    print(f'Time taken to concatenate: {round((t3-t2)/60, 3)} minutes.')
    print(f'Total time: {round((t3-t1)/60, 3)} minutes.')














