# SPTS - single particle tracking and sizing


### Installation

Clone this repo.
```
git clone git@github.com:YellowSub17/spts.git
```

Create a conda environment.
```
conda create --name spts python=3.13 -y 
conda activate spts
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
```

Activate the environment.
```
conda activate spts
```

Get Max H. packages.
```
git clone git@github.com:YellowSub17/mulpro.git
git clone git@github.com:YellowSub17/h5writer.git
```

Install Max H. packages. This will add some directories to your path to make some scripts available to run.
```
cd mulpro; pip install -e .; cd ../
cd h5writer; pip install -e .; cd ../
cd spts; pip install -e .; cd ../
```

Install the module as a jupyter notebook kernel.
```
python -m ipykernel install --user --name spts --display-name "Python 3.13 (spts)"
```
