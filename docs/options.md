Options and Arguments
---------------------
```
Main cellsnake executable, version: 0.1.1c

Usage:
    cellsnake <INPUT> [--resolution <text>] [--percent_mt <text>] [--configfile <text>] [--gene <text>] [--jobs <integer>] [--option <text>]... [--release-the-kraken <text>] [--taxa <text>] [--unlock|--remove] [--dry]
    cellsnake <INPUT> [--unlock|--remove] [--dry]
    cellsnake --generate-template
    cellsnake --install-packages
    cellsnake (-h | --help)
    cellsnake --version
    cellsnake --init

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


