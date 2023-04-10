# cellsnake

A command line tool for easy and scalable single cell analysis  
![Docker Pulls](https://img.shields.io/docker/pulls/sinanugur/cellsnake)

Installation
------------

Method for installing directly from the GitHub repo:
```
git clone https://github.com/sinanugur/cellsnake.git
cd cellsnake
pip install .
```

Check if the installation works by calling the main script:  
```
cellsnake --help
```
then install and check if all the R packages are installed by typing:

```
cellsnake --install-packages

You should see this message if all the packages are available:
[1] "All packages were installed...OK"
```


Note: You have to install dependencies if you prefer Github installation. We strongly recommend Bioconda and Mamba. 

`--install-packages` argument must be always called to check if the R packages are available and installed correctly. 

Quick start examples
-------------------
Run `cellsnake` in a clean directory and `cellsnake` will create the required directories while running. You may download publicly available fetal brain dataset to test your `cellsnake` installation. The link is here.

After downloading the dataset, just point the data folder which contains the two dataset folders, this will trigger a standard cellsnake workflow:
```
cellsnake data
```

After the pipeline finishes, you may also integrate these two samples:
```
cellsnake data --option integration
```

To determine a manual resolution parameter, you can also create only a ClusTree:
```
cellsnake data --option integration --option clustree
```

Let's say you want a resolution of 0.1, then you can trigger a run with this resolution:
```
cellsnake data --option integration --resolution 0.1
```

It is also possible to use automatic resolution selection, however this might be very slow in large datasets:
```
cellsnake data --option integration --resolution auto
```

See our documentation for detailed explanations and to read full features: https://cellsnake.readthedocs.io/

Options and Arguments
---------------------
```
Usage:
    cellsnake <INPUT> [--resolution <text>] [--percent_mt <text>] [--configfile <text>] [--gene <text>] [--jobs <integer>] [--option <text>]... [--release-the-kraken <text>] [--taxa <text>] [--unlock|--remove] [--dry]
    cellsnake <INPUT> [--unlock|--remove] [--dry]
    cellsnake --generate-template
    cellsnake --install-packages
    cellsnake (-h | --help)
    cellsnake --version

Arguments:
    INPUT                                   Input directory or a file to process (if a directory given, batch mode is ON).
    -c <text>, --configfile <text>          Config file name (if not supplied, it will use default settings, you may generate a template, change it and use it in your runs).
    --resolution <text>                     Resolution for cluster detection, write "auto" for auto detection [default: 0.8].
    --percent_mt <text>                     Maximum mitochondrial gene percentage cutoff, for example, 5 or 10, write "auto" for auto detection [default: 10].
    --gene <text>                           Create publication ready plots for a gene or a list of genes from a text file.
    --option <text>                         cellsnake run options: "minimal", "standard", "clustree", "advanced" [default: standard]. "integration" is to integrate and run on integrated samples.
    --release-the-kraken <text>             Kraken database folder.
    --taxa <text>                           Microbiome taxonomic level collapse to "domain", "kingdom", "phylum", "class", "order", "family", "genus", "species" [default: genus]
    -j <integer>, --jobs <integer>          Total CPUs. [default: 2]

Options:
    --generate-template                Generate config file template in the current directory.
    --install-packages                 Install, reinstall or check required R packages.
    -u, --unlock                       Rescue stalled jobs (Try this if the previous job ended prematurely or currently failing).
    -r, --remove                       Delete all output files (this won't affect input files).
    -d, --dry                          Dry run, nothing will be generated.
    -h, --help                         Show this screen.
    --version                          Show version.
```

Output
------
The `cellsnake` main executable will generate two main folders: analyses and results.  
If an integrated dataset available, analyses_integrated and results_integrated.


Logs
-----

