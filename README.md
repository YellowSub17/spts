# SPTS - single particle tracking and sizing


### Installation

Clone this repo.
```
git clone git@github.com:YellowSub17/spts.git
```

Create a conda environment.
```
conda create -f spts/env.yml
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
