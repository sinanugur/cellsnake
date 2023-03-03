Installation
------------
To install this package with conda run:

```
conda install cellsnake -c bioconda -c conda-forge 
```

You may want to install Mamba first, which will reduce installation time.

To install this package with Mamba run:

```
conda install mamba -c conda-forge
mamba install cellsnake -c bioconda -c conda-forge 
```

Alternative method:
```
git clone https://github.com/sinanugur/cellsnake.git
cd cellsnake
pip install .
```

Check if the installation works by calling the main script.
```
cellsnake --help
```

then install and check if all the R packages are installed by typing:
```
cellsnake --install-packages

You should see this message if all the packages are available:
[1] "All packages were installed...OK"
```

Note: If installation of any R packages fail, you have to install them manually!