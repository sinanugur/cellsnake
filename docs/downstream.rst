*******************
Downstream analysis
*******************

Cellsnake provides RDS files for downstream analysis. 


The RDS files are saved in the `analyses` or `analyses_integrated` directories. 


The RDS files can be loaded into R using the readRDS function.

For example, to load the Seurat object for the analysis with 10% MT threshold and 0.8 resolution, use the following command:

.. code-block:: R

    library(Seurat)
    seurat_object <- readRDS("analyses/processed/percent_mt~10/resolution~0.8/sample_name.rds")


Annotation of cell types for this same dataset can be found in the `analyses/singler` directory.

.. code-block:: R

    library(Seurat)
    seurat_object <- readRDS("./analyses/singler/percent_mt~10/resolution~0.8/sample_name.rds")


Kraken2 predictions (metagenomics results) for this same dataset can be found in the `analyses/kraken` directory.

.. code-block:: R

    library(Seurat)
    seurat_object <- readRDS("./analyses/kraken/0_3/percent_mt~10/resolution~0.8/sample_name/microbiome-full-genus-level.rds")


