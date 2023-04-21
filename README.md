# <table border="0" cellspacing="0" cellpadding="0"> <tbody> <tr> <td rowspan="4"> <img src="cellsnake-logo-blue-small.png"> </td> <td> [![Docker Pulls](https://img.shields.io/docker/pulls/sinanugur/cellsnake)](https://hub.docker.com/r/sinanugur/cellsnake) [![Documentation Status](https://readthedocs.org/projects/cellsnake/badge/?version=latest)](https://cellsnake.readthedocs.io/en/latest/?badge=latest)  </td>  </tr> <tr>    <td> [![PyPI version](https://badge.fury.io/py/cellsnake.svg)](https://badge.fury.io/py/cellsnake) </td>  </tr>  <tr>    <td> [![Anaconda-Server Badge](https://anaconda.org/bioconda/cellsnake/badges/latest_release_relative_date.svg)](https://anaconda.org/bioconda/cellsnake) </td>  </tr>  <tr>    <td> [![Anaconda-Server Badge](https://anaconda.org/bioconda/cellsnake/badges/downloads.svg)](https://anaconda.org/bioconda/cellsnake)  </td>  </tr></tbody></table>

A command line tool for easy and scalable single cell RNA sequencing analysis  


Installation
------------

Please use Bioconda repo for installation and first installation of Mamba is recommended. Then install to a clean environment.
```
conda install mamba -c conda-forge

mamba create -n cellsnake -c bioconda -c conda-forge

```

Apple Silicon computers have to force Osx64, you can install like this.

```
conda install mamba -c conda-forge

CONDA_SUBDIR=osx-64 mamba create -n cellsnake -c bioconda -c conda-forge

```


Check if the installation works by calling the main script.  
```
conda activate cellsnake
cellsnake --help
```

Then install and check if all the R packages are installed by typing. 
```
cellsnake --install-packages
```


You should see this message if all the packages are available:
```
cellsnake --install-packages
[1] "All packages were installed...OK"
```

Cellsnake auto install most of the packages when necessary or during the environment creation but it is good to check if they are installable. 
Only do this once. You can then move the environment to an offline location as well if required. We recommend our Docker image and it is a better solution for installation problems.

Quick start examples
-------------------
Run `cellsnake` in a clean directory and `cellsnake` will create the required directories while running. You may download publicly available fetal brain dataset to test your `cellsnake` installation. The link is here.

https://www.dropbox.com/sh/1qn2odtnci0vvtr/AADPxHH-GR4h-OuQG0TLQyxWa?dl=0

After downloading the dataset, just point the data folder which contains the two dataset folders, this will trigger a standard cellsnake workflow:
```
cellsnake standard data
```

After the pipeline finishes, go through the output files etc. You then can also integrate these two samples which makes sense.
```
cellsnake integrate data
```

Lets work on the integrated object from now on, we already processed the samples separately. 

Lets do a minimal run, this will also generate a clustree plot as well which can be used to investigate the optimal resolution.
```
cellsnake integrated minimal analyses_integrated/seurat/integrated.rds
```

Let's say you want a resolution of 0.1 after checking clustree plot, then you can trigger a run with this resolution.
```
cellsnake integrated standard analyses_integrated/seurat/integrated.rds --resolution 0.1
```

It is also possible to use automatic resolution selection, however this might be very slow in large datasets.
```
cellsnake integrated standard analyses_integrated/seurat/integrated.rds --resolution auto
```

See our documentation for detailed explanations and to read full features: https://cellsnake.readthedocs.io/

Options and Arguments
---------------------
```
Usage:
    cellsnake <command> <INPUT> [options] [--unlock|--remove] [--dry]
    cellsnake integrated <command> <INPUT> [options] [--unlock|--remove] [--dry]
    cellsnake --generate-template
    cellsnake --install-packages
    cellsnake (-h | --help)
    cellsnake --version

commands:
    minimal                                Run cellsnake with minimal workflow.
    standard                               Run cellsnake with standard workflow.
    advanced                               Run cellsnake with advanced workflow.
    clustree                               Run cellsnake with clustree workflow.
    integrate                              Run cellsnake to integrate samples under analyses folder.
                                           This option expects you have already finished processing multiple samples.

main arguments:
    INPUT                                  Input directory or a file to process (if a directory given, batch mode is ON).
    --configfile <text>                    Config file name in YAML format, for example, "config.yaml". No default but can be created with --generate-template.
    --metadata <text>                      Metadata file name in CSV, TSV or Excel format, for example, "metadata.csv", header required, first column sample name. No default but can be created with --generate-template.
    --metadata_column <text>               Metadata column for differential expression analysis [default: condition].

other arguments:
    --gene <gene or filename>              Create publication ready plots for a gene or a list of genes from a text file.

main options:
    --percent_mt <double>                  Maximum mitochondrial gene percentage cutoff,
                                           for example, 5 or 10, write "auto" for auto detection [default: 10].
    --resolution <double>                  Resolution for cluster detection, write "auto" for auto detection [default: 0.8].

other options:
    --doublet_filter <bool>                [default: True] #this may fail on some samples
    --percent_rp <double>                  [default: 0] #Ribosomal genes minimum percentage (0-100), default no filtering
    --min_cells <integer>                  [default: 3] #seurat default, recommended
    --min_features <integer>               [default: 200] #seurat default, recommended, nFeature_RNA
    --max_features <integer>               [default: Inf] #seurat default, nFeature_RNA, 5000 can be a good cutoff
    --min_molecules <integer>              [default: 0] #seurat default, nCount_RNA, min_features usually handles this so keep it 0
    --max_molecules <integer>              [default: Inf] #seurat default, nCount_RNA, to filter potential doublets, doublet filtering is already default, so keep this Inf
    --highly_variable_features <integer>   [default: 2000] #seurat defaults, recommended
    --variable_selection_method <text>     [default: vst] #seurat defaults, recommended

    --normalization_method <text>          [default: LogNormalize]
    --scale_factor <integer>               [default: 10000]
    --logfc_threshold <double>             [default: 0.25]
    --test_use <text>                      [default: wilcox]


    --mapping <text>                       [default: org.Hs.eg.db] #you may install others from Bioconductor, this is for human
    --organism <text>                      [default: hsa] #alternatives https://www.genome.jp/kegg/catalog/org_list.html
    --species <text>                       [default: human] for cellchat, #only human or mouse is accepted

plotting parameters:
    --min_percentage_to_plot <double>        [default: 2] #only show clusters more than % of cells on the legend
    --show_labels <bool>                     [default: True] #
    --marker_plots_per_cluster_n <integer>   [default: 20] #plot summary marker plots for top markers
    --umap_markers_plot <bool>               [default: True]
    --tsne_markers_plot <bool>               [default: False]

annotation options:
    --singler_ref <text>                    [default: BlueprintEncodeData] # https://bioconductor.org/packages/release/data/experiment/vignettes/celldex/inst/doc/userguide.html#1_Overview
    --celltypist_model <text>               [default: Immune_All_Low.pkl] #refer to Celltypist for another model

microbiome options:
    --kraken_db_folder <text>              No default, you need to provide a folder with kraken2 database
    --taxa <text>                          [default: genus] # available options "domain", "kingdom", "phylum", "class", "order", "family", "genus", "species"
    --microbiome_min_cells <integer>       [default: 1]
    --microbiome_min_features <integer>    [default: 3]
    --confidence <double>                  [default: 0.05] #see kraken2 manual
    --min_hit_groups <integer>             [default: 4] #see kraken2 manual

integration options:
    --dims <integer>                       [default: 30] #refer to Seurat for more details
    --reduction <text>                     [default: cca] #refer to Seurat for more details

others:
    --generate-template                    Generate config file template and metadata template in the current directory.
    --install-packages                     Install, reinstall or check required R packages.
    -j <integer>, --jobs <integer>         Total CPUs. [default: 2]
    -u, --unlock                           Rescue stalled jobs (Try this if the previous job ended prematurely or currently failing).
    -r, --remove                           Delete all output files (this won't affect input files).
    -d, --dry                              Dry run, nothing will be generated.
    -h, --help                             Show this screen.
    --version                              Show version.
```


Output
------
The `cellsnake` main executable will generate two main folders: analyses and results. If an integrated dataset available, analyses_integrated and results_integrated will be created.  

The main directory structure will look like this, __resolution__ and __percent_mt__ can be visible on directory names. These are the only parameters that will generate a separate folders.

```
results/integrated/percent_mt~auto/resolution~0.8/ #for regular samples
results_integrated/integrated/percent_mt~auto/resolution~0.8/ #for integrated samples
```


