#!/usr/bin/env python
import argparse
import re
import subprocess
import sys
from pathlib import Path

NEW_DATA_DIR = Path('/home/pat/spts-ana/data/newdata')
DATA_DIR = Path('/home/pat/spts-ana/data/')


def parse_args():
    parser = argparse.ArgumentParser(
        description="Set up an SPTS analysis directory for a given config and .cxi "
                    "file (found in NEW_DATA_DIR), then run the SPTS worker pipeline on it."
    )
    parser.add_argument("conf", type=Path, help="Path to the *.conf file.")
    parser.add_argument("cxi", type=Path,
                        help="Name of the *.cxi file (expected to live in %s)." % NEW_DATA_DIR)
    args = parser.parse_args()

    if args.conf.suffix != ".conf":
        parser.error("conf file must have a .conf extension, got: %s" % args.conf)
    if not args.conf.is_file():
        parser.error("conf file does not exist: %s" % args.conf)

    if args.cxi.suffix != ".cxi":
        parser.error("cxi file must have a .cxi extension, got: %s" % args.cxi)
    if not (NEW_DATA_DIR / args.cxi.name).is_file():
        parser.error("cxi file does not exist: %s" % (NEW_DATA_DIR / args.cxi.name))

    return args


def extract_number(cxi_path):
    """Pull the numeric run ID out of the cxi filename, e.g. 'data01271.cxi' -> '01271'."""
    match = re.search(r"\d+", cxi_path.stem)
    if match is None:
        sys.exit("Could not find a numeric ID in cxi filename: %s" % cxi_path.name)
    return match.group()


def run(cmd, **kwargs):
    print(" ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True, **kwargs)


def main():
    args = parse_args()

    number = extract_number(args.cxi)
    analysis_dir = DATA_DIR / Path("data%s_%s" % (number, args.conf.stem))
    analysis_dir.mkdir(exist_ok=True)

    conf_dest = analysis_dir / "spts.conf"
    frames_dest = analysis_dir / "frames.cxi"
    cxi_source = NEW_DATA_DIR / args.cxi.name

    if frames_dest.exists() or frames_dest.is_symlink():
        if frames_dest.is_symlink() and frames_dest.resolve() == cxi_source.resolve():
            print("%s already links to %s, skipping." % (frames_dest, cxi_source))
        else:
            sys.exit("%s already exists and does not point to %s -- refusing to overwrite. "
                     "Remove it manually if you want to redo this analysis." % (frames_dest, cxi_source))
    else:
        run(["ln", "-s", str(cxi_source), str(frames_dest)])

    run(["cp", str(args.conf), str(conf_dest)])
    run(["run_spts.py", "-v"], cwd=analysis_dir)


if __name__ == "__main__":
    main()
