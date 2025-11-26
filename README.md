# SPTS - single particle tracking and sizing


### Installation

Create a conda environment.
```
conda create -n spts313 python==3.13
```
Activate the environment.
```
conda activate spts
```

Install the required packages.
```
conda install numpy -y
conda install cython -y
conda install h5py -y
conda install ipykernel -y
conda install scipy -y
conda install matplotlib -y
conda install pyqtgraph -y
conda install pyqt5 -y
conda install -c conda-forge expiringdict -y
conda install -c conda-forge olefile -y
conda install -c conda-forge typing -y
```

Get Max H. packages.
```
git clone https://github.com/YellowSub17/spts.git
git clone https://github.com/YellowSub17/mulpro.git
git clone https://github.com/YellowSub17/h5writer.git
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
