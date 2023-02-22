# cellsnake

A command line tool for scalable single cell analysis

Installation
------------

Method for installing directly from the GitHub repo:
```
git clone https://github.com/sinanugur/cellsnake.git
cd cellsnake
pip install .
```

Check if the installation works by calling the main script.  
```
cellsnake --help
```

Note: You have to install dependencies if you prefer Github installation.  

Quick start example
-------------------
Create a new directory and run cellsnake there after the installation. cellsnake will create the required directories while running. You may download publicly available fetal brain dataset to test your cellsnake installation.

```
cellsnake data --percent_mt 10 
```

See our documentation for detailed explanations: https://cellsnake.readthedocs.io/

Options and Arguments
---------------------
```
Main cellsnake executable, version: 0.1.0

Usage:
    cellsnake <INPUT> [--resolution <text>] [--percent_mt <text>] [--configfile <text>] [--gene <text>] [--jobs <integer>] [--option <text>]... [--release-the-kraken <text>] [--taxa <text>] [--unlock|--remove] [--dry]
    cellsnake <INPUT> [--unlock|--remove] [--dry]
    cellsnake --generate-configfile-template
    cellsnake (-h | --help)
    cellsnake --version
    cellsnake --init

Arguments:
    INPUT                                   Input directory or a file to process (if a directory given, batch mode is ON).
    -c <text>, --configfile <text>          Config file name (if not supplied, it will use default settings, you may generate a template, change it and use it in your runs).
    --resolution <text>                     Resolution for cluster detection, write "auto" for auto detection [default: 0.8].
    --percent_mt <text>                     Maximum mitochondrial gene percentage cutoff, for example, 5 or 10, write "auto" for auto detection [default: 10].
    --gene <text>                           Create publication ready plots for a gene or a list of genes from a text file.
    --option <text>                         cellsnake run options: "minimal", "standard", "clustree", "advanced" [default: standard]. "integration" is to integrate.
    --release-the-kraken <text>             Kraken database folder.
    --taxa <text>                           Microbiome taxonomic level collapse to "domain", "kingdom", "phylum", "class", "order", "family", "genus", "species" [default: genus]
    -j <integer>, --jobs <integer>          Total CPUs. [default: 2]

Options:
    --generate-configfile-template     Generate config file template in the current directory.
    -u, --unlock                       Rescue stalled jobs (Try this if the previous job ended prematurely or currently failing).
    -r, --remove                       Delete all output files (this won't affect input files).
    -d, --dry                          Dry run, nothing will be generated.
    -h, --help                         Show this screen.
    --version                          Show version.
```

Usage
-----

Output
------
The `cellsnake` main executable will generate two main folders: analyses and results.  
If run on an integrated dataset, analyses_integrated and results_integrated.


