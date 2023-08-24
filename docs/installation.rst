************
Installation
************
To install this package with conda run:

.. code-block:: bash
    
    conda install cellsnake -c bioconda -c conda-forge


You may want to install Mamba first, which will reduce installation time.

To install this package with Mamba run:

.. code-block:: bash

    conda install mamba -c conda-forge
    mamba install cellsnake -c bioconda -c conda-forge 

.. code-block:: bash

    #to install on Apple Silicon computers (M1 or newer)
    conda install mamba -c conda-forge
    CONDA_SUBDIR=osx-64 mamba create -n cellsnake -c bioconda -c conda-forge cellsnake



Check if the installation works by calling the main script.

.. code-block:: bash

    cellsnake --help


then install and check if all the R packages are installed by typing:

.. code-block:: bash

    cellsnake --install-packages


You should see this message if all the packages are available:

.. code-block:: bash
    
    [1] "All packages were installed...OK"


Note: If installation of any R packages fail, you have to install them manually!


How to use the Docker Image
---------------------------
Cellsnake has an official Docker image, located here: https://hub.docker.com/r/sinanugur/cellsnake



You can pull the latest build:

.. code-block:: bash

    docker pull sinanugur/cellsnake:latest


You can start a standard run:

.. code-block:: bash
    
    docker run -it --rm -v $PWD:/app sinanugur/cellsnake:latest cellsnake standard data


or you can also use Podman as well, Podman is useful when you are using on HPC platforms without admin access.

.. code-block:: bash

    podman run -it --rm -v $PWD:/app sinanugur/cellsnake:latest cellsnake standard data


.. note::
    
    It is not possible to run cellsnake natively on Apple Silicon (M1 or newer) for now. For example, Kraken2 is not compatible with this architecture and our Docker image is therefore AMD64-based. It is however possible to run without a Docker container using the Bioconda package. Yet still it has to be forced to use Osx-64 architecture and all the dependencies can be resolved. This offers a faster experience than Docker container for Apple laptops. 




How to request higher memory and CPUs?
--------------------------------------
.. code-block:: bash

    #for example request 5 CPUs and 20g ram
    docker run -m 20g --cpus 5 -it --rm -v $PWD:/app sinanugur/cellsnake:latest cellsnake standard data --jobs 5

