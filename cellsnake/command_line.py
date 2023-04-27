#!/usr/bin/env python
'''
Created on 02/12/2022
cellsnake main
@author: Sinan U. Umu, sinanugur@gmail.com
'''

#from __future__ import print_function
import re
import warnings
warnings.filterwarnings("ignore")
from docopt import docopt
import os
import sys
import subprocess
import shutil
import datetime
import random
#from fuzzywuzzy import fuzz
import timeit
import errno
import os
import yaml
from yaml.loader import SafeLoader
from subprocess import call
import pathlib


#from schema import Schema, And, Or, Use, SchemaError

from collections import defaultdict

import cellsnake
cellsnake_path=os.path.dirname(cellsnake.__file__)
options = ["clustree","clusteringTree","minimal","standard","advanced"] #and integration


__author__ = 'Sinan U. Umu'
__version__= '0.2.0'
__logo__="""
             _  _                     _           
            | || |                   | |          
  ___   ___ | || | ___  _ __    __ _ | | __  ___  
 / __| / _ \| || |/ __|| '_ \  / _` || |/ / / _ \ 
| (__ |  __/| || |\__ \| | | || (_| ||   < |  __/ 
 \___| \___||_||_||___/|_| |_| \__,_||_|\_\ \___| 
                                                  
"""  


__licence__="""
MIT License
Copyright (c) 2023 Sinan U. Umu (SUU) sinanugur@gmail.com
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__doc__=f"""Main cellsnake executable, version: {__version__}
{__logo__} 
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
    
"""


def check_command_line_arguments(arguments):
    if not os.path.exists(arguments["<INPUT>"]):
        print("File or input directory not found : ",arguments["<INPUT>"])
        return False
    if arguments["integrated"] and os.path.isdir(arguments["<INPUT>"]):
        print("You are running integrated option but you provided a directory, not a Seurat object file !")
        print("The default Seurat object is usually here, analyses_integrated/seurat/integrated.rds")
        print("""You can try something like: "cellsnake integrated standard analyses_integrated/seurat/integrated.rds""")
        return False
    if arguments["integrated"] and os.path.isfile(arguments["<INPUT>"]):
        file_extension = pathlib.Path(arguments["<INPUT>"])
        if (file_extension.suffix).lower() not in [".rds"]:
            print("You are running integrated option but you provided not a Seurat object file !")
            print("The default Seurat object is usually here, analyses_integrated/seurat/integrated.rds")
            print("""You can try something like: \n cellsnake integrated standard analyses_integrated/seurat/integrated.rds""")
            return False
    if arguments["--configfile"]:
         if not os.path.isfile(arguments["--configfile"]):
            print("Config file given not found : ",arguments["--configfile"])
            return False
    if arguments["--metadata"]:
         if not os.path.isfile(arguments["--metadata"]):
            print("Metadata file given not found : ",arguments["--metadata"])
            return False
    if arguments["--kraken_db_folder"]:
        if not os.path.exists(arguments["--kraken_db_folder"]) and not os.path.isfile(arguments["--kraken_db_folder"] + "/inspect.txt"):
            print("KrakenDB directory not found : ",arguments["--kraken_db_folder"])
            print("You should download a proper DB from this link (https://benlangmead.github.io/aws-indexes/k2), unpack it and point that directory.")
            return False
    if arguments["--taxa"] not in ["domain", "kingdom", "phylum", "class", "order", "family", "genus", "species"]:
        print("Select a correct taxa level for microbiome analysis:",arguments["--taxa"])
        print("Possible options : ",["domain", "kingdom", "phylum", "class", "order", "family", "genus", "species"])
        return False
    return True


class CommandLine:
    def __init__(self):
        self.snakemake="snakemake --rerun-incomplete -k "
        self.runid="".join(random.choices("abcdefghisz",k=3) + random.choices("123456789",k=5))
        self.config=[]
        self.configfile_loaded=False
        self.is_integrated_sample=False
        self.is_this_an_integration_run=False
        self.parameters=dict()
        self.log=True #if dry unlock etc, no logging
        
    def __str__(self):
        return self.snakemake
    def __repr__(self):
        return self.snakemake
    



        

    def add_config_argument(self):
        self.snakemake = self.snakemake + " --config " + " ".join(self.config)


    def load_configfile_if_available(self,arguments):
        if self.configfile_loaded is False:
            if arguments["--configfile"]:
                self.snakemake = self.snakemake + " --configfile={}".format(arguments["--configfile"])
                configfile=arguments["--configfile"]
            #else:
            #    self.snakemake = self.snakemake + " --configfile={}".format(cellsnake_path + "/scrna/config.yaml")
            #    configfile=cellsnake_path + "/scrna/config.yaml"

                with open(configfile) as f:
                    self.parameters=yaml.load(f,Loader=SafeLoader)
                self.configfile_loaded=True
        
                #self.change_parameters(arguments)

    #def change_parameters(self,arguments): #change parameters if there is a config file
    #    if self.configfile_loaded is True and arguments["--configfile"]:
    #        arguments["--resolution"] = self.parameters["resolution"]
    #        arguments["--percent_mt"] = self.parameters["percent_mt"]
    #        arguments["--taxa"] = self.parameters["taxa"]






        

    def prepare_arguments(self,arguments):
        self.snakemake = self.snakemake +  " -j {} ".format(arguments['--jobs']) #set CPU number
        self.snakemake = self.snakemake +  " -s {} ".format(f"{cellsnake_path}/scrna/workflow/Snakefile") #set Snakefile location
        self.load_configfile_if_available(arguments)
        if self.is_this_an_integration_run is False:
            self.config.append("datafolder={}".format(arguments['<INPUT>']))

        self.config.append(f"cellsnake_path={cellsnake_path}/scrna/")
        for i,b in arguments.items():
            if i not in ["--jobs","integrated","--configfile","--option","--gene","--kraken_db_folder","--unlock","--remove","--dry","--help","--version","<INPUT>","<command>","--install-packages","--generate-template"]:
                k=i.lstrip("--")
                if self.configfile_loaded is False: #if there is no config file, add all parameters given by the command line or defaults. command line parameters have priority over config file parameters
                    self.config.append(k + "=" + str(b))
                    self.parameters[k]=str(b)
                else:
                    if self.parameters.get(k) and i not in sys.argv:
                        self.config.append(k + "=" + str(self.parameters.get(k)))
                    else:
                        self.config.append(k + "=" + str(b))
                        self.parameters[k]=str(b)


        
        self.config.append("runid={}".format(self.runid))
        if arguments["--gene"]:
            if os.path.isfile(arguments["--gene"]):
                self.config.append("selected_gene_file={}".format(arguments["--gene"]))
            else:
                self.config.append("gene_to_plot={}".format(arguments["--gene"]))

        if arguments["--kraken_db_folder"]:
            self.config.append("kraken_db_folder={}".format(arguments["--kraken_db_folder"]))
            

        if self.is_integrated_sample:
            self.config.append("is_integrated_sample={}".format("True"))


        if  self.is_this_an_integration_run is False:
            self.config.append("option={}".format(arguments['<command>']))
         
        elif self.is_this_an_integration_run:
            self.config.append("option=integration")
        if arguments["--dry"]:
            self.snakemake = self.snakemake + " -n "
            self.log=False
        if arguments["--unlock"]:
            self.snakemake = self.snakemake + " --unlock "
            self.log=False
        if arguments["--remove"]:
            self.snakemake = self.snakemake + " --delete-all-output "
            self.log=False
        self.add_config_argument()
        
    
    def write_to_log(self,start):
        logname = "_".join(["cellsnake",self.runid, datetime.datetime.now().strftime("%y%m%d_%H%M%S"),"runlog"])
        stop = timeit.default_timer()
        if self.log:
            with open(logname,"w") as f:
                f.write(__logo__ + "\n")
                f.write("Run ID : " + self.runid + "\n")
                f.write("Cellnake version : " + __version__ + "\n")
                f.write("Cellsnake arguments : " + " ".join(sys.argv) + "\n\n")
                f.write("------------------------------" + "\n")
                f.write("Snakemake arguments : " + str(self.snakemake) + "\n\n")
                f.write("------------------------------" + "\n")
                f.write("Run parameters: " + str(self.parameters) + "\n\n")
                f.write("Total run time: {t:.2f} mins \n".format(t=(stop-start)/60))


def run_integration(arguments):

    start = timeit.default_timer()
    snakemake_argument=CommandLine()
    snakemake_argument.is_this_an_integration_run = True
    snakemake_argument.prepare_arguments(arguments)
    subprocess.check_call(str(snakemake_argument),shell=True)
    snakemake_argument.write_to_log(start)


    #then run workflow on integrated dataset
    #snakemake_argument=CommandLine()
    #snakemake_argument.is_this_an_integration_run = False
    #snakemake_argument.is_integrated_sample = True
    #snakemake_argument.config.append("datafolder=analyses_integrated/seurat/integrated.rds")
    #try:
    #    arguments["--option"].remove("integration")
    #except:
    #    pass
    #snakemake_argument.prepare_arguments(arguments)
    #subprocess.check_call(str(snakemake_argument),shell=True)
    #return snakemake_argument

def run_workflow(arguments):
    start = timeit.default_timer()
    snakemake_argument=CommandLine()
    if arguments["integrated"]:
        snakemake_argument.is_integrated_sample = True
    snakemake_argument.prepare_arguments(arguments)
    subprocess.check_call(str(snakemake_argument),shell=True)
    snakemake_argument.write_to_log(start)


def main():
        cli_arguments = docopt(__doc__, version=__version__)
        if cli_arguments["--generate-template"]:
            print("Generating config.yaml file...")
            print("You can use this as a template for a cellsnake run. You may change the settings.")
            shutil.copyfile(cellsnake_path + "/scrna/config.yaml", 'config.yaml')
            print("Generating metadata.csv file...")
            with open("metadata.csv","w") as f:
                f.write("sample,condition\n")
                f.write("sample1,condition1\n")
                f.write("sample2,condition2\n")
            return
        if cli_arguments["--install-packages"]:
            subprocess.check_call(cellsnake_path + "/scrna/workflow/scripts/scrna-install-packages.R")
            return
        
        if not check_command_line_arguments(cli_arguments):
            print("""Please check your command line arguments. Use "cellsnake --help" for more information""")
            return


        if cli_arguments['<command>'] == 'minimal':
            run_workflow(cli_arguments)
        if cli_arguments['<command>'] == 'standard':
            run_workflow(cli_arguments)
        if cli_arguments['<command>'] == 'advanced':
            run_workflow(cli_arguments)
        if cli_arguments['<command>'] == 'clustree':
            run_workflow(cli_arguments)
        if cli_arguments['<command>'] == 'integrate':
            run_workflow(cli_arguments)
