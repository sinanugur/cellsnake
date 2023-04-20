Installation
============
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


How to use the Docker Image
-----------------------
Cellsnake has an official Docker image, located here: https://hub.docker.com/repository/docker/sinanugur/cellsnake



You can pull the latest build:

```
docker pull sinanugur/cellsnake:latest
```

You can start a standard run:
```
docker run -it --rm -v $PWD:/app sinanugur/cellsnake:latest cellsnake standard data
```

or you can also use Podman as well, Podman is useful when you are using on HPC platforms without admin access.

```
podman run -it --rm -v $PWD:/app sinanugur/cellsnake:latest cellsnake standard data
```