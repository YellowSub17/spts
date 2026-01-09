# SPTS - single particle tracking and sizing


### Installation

Clone this repo.
```
git clone git@github.com:YellowSub17/spts.git
```

Create a conda environment.
```
conda create -n spts python==3.13
```
Activate the environment.
```
conda activate spts
```

Install the required packages.
```
conda install numpy==2.3.5 -y
conda install cython==3.2.2 -y
conda install h5py==3.15.1 -y
conda install ipykernel==6.31.0 -y
conda install scipy==1.16.3 -y
conda install matplotlib==3.10.7 -y
conda install pyqtgraph==0.13.7 -y
conda install pyqt==5.15.11 -y
conda install -c conda-forge olefile==0.47 -y
conda install -c conda-forge expiringdict -y
conda install -c conda-forge typing -y
```

Get Max H. packages.
```
git clone git@github.com:YellowSub17/mulpro.git
git clone git@github.com:YellowSub17/h5writer.git
```

Install Max H. packages.
```
cd mulpro; python setup.py install; cd ../
cd spts; python setup.py install; cd ../
cd h5writer; python setup.py install; cd ../
```

Install jupyter notebook kernel.
```
python -m ipykernel install --user --name spts --display-name "Python (spts)"
```
