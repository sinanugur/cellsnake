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


#from schema import Schema, And, Or, Use, SchemaError

from collections import defaultdict

import cellsnake
cellsnake_path=os.path.dirname(cellsnake.__file__)
options = ["clustree","clusteringTree","minimal","standard","advanced"] #and integration


__author__ = 'Sinan U. Umu'
__version__= '0.2.0.dev9'
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

"""


def check_command_line_arguments(arguments):
    if not os.path.exists(arguments["<INPUT>"]):
        print("File or input directory not found : ",arguments["<INPUT>"])
        return False
    if arguments["--configfile"]:
         if not os.path.isfile(arguments["--configfile"]):
            print("Config file given not found : ",arguments["--configfile"])
            return False
    if [o for o in arguments["--option"] if o not in ["minimal", "standard", "clustree", "integration", "advanced"]]:
        print("Select a correct option for analyses : ",arguments["--option"])
        print("Possible options : ",["minimal", "standard", "clustree", "advanced","integration"])
        print("You may combine integration with others so the integrated sample will be processed accordingly.")
        print("The default is : standard ")
        return False
    elif len(arguments["--option"]) > 1 and all(o  in arguments["--option"] for o in ["minimal", "standard", "clustree", "advanced"]):
        print(arguments["--option"])
        print("You cannot combine two options, except integration, choose one of these : ",["minimal", "standard", "clustree", "advanced"])
        return False

    if arguments["--release-the-kraken"]:
        if not os.path.exists(arguments["--release-the-kraken"]) and not os.path.isfile(arguments["--release-the-kraken"] + "/inspect.txt"):
            print("KrakenDB directory not found : ",arguments["--release-the-kraken"])
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
        
    def __str__(self):
        return self.snakemake
    def __repr__(self):
        return self.snakemake
    



        

    def add_config_argument(self):
        self.snakemake = self.snakemake + " --config " + " ".join(self.config)


    def load_and_add_default_configfile_argument(self,arguments):
        if self.configfile_loaded is False:
            if arguments["--configfile"]:
                self.snakemake = self.snakemake + " --configfile={}".format(arguments["--configfile"])
                configfile=arguments["--configfile"]
            else:
                self.snakemake = self.snakemake + " --configfile={}".format(cellsnake_path + "/scrna/config.yaml")
                configfile=cellsnake_path + "/scrna/config.yaml"

            with open(configfile) as f:
                self.parameters=yaml.load(f,Loader=SafeLoader)
            self.configfile_loaded=True
        
        self.change_parameters(arguments)

    def change_parameters(self,arguments): #change parameters if there is a config file
        if self.configfile_loaded is True and arguments["--configfile"]:
            arguments["--resolution"] = self.parameters["resolution"]
            arguments["--percent_mt"] = self.parameters["percent_mt"]
            arguments["--taxa"] = self.parameters["taxa"]






        

    def prepare_arguments(self,arguments):
        self.snakemake = self.snakemake +  " -j {} ".format(arguments['--jobs']) #set CPU number
        self.snakemake = self.snakemake +  " -s {} ".format(f"{cellsnake_path}/scrna/workflow/Snakefile") #set Snakefile location
        self.load_and_add_default_configfile_argument(arguments)
        if self.is_this_an_integration_run is False and self.is_integrated_sample is False:
            self.config.append("datafolder={}".format(arguments['<INPUT>']))

        self.config.append(f"cellsnake_path={cellsnake_path}/scrna/")
        self.config.append("resolution={}".format(arguments["--resolution"]))
        self.config.append("percent_mt={}".format(arguments["--percent_mt"]))
        self.config.append("taxa={}".format(arguments["--taxa"]))
        self.config.append("runid={}".format(self.runid))
        if arguments["--gene"]:
            if os.path.isfile(arguments["--gene"]):
                self.config.append("selected_gene_file={}".format(arguments["--gene"]))
            else:
                self.config.append("gene_to_plot={}".format(arguments["--gene"]))

        if arguments["--release-the-kraken"]:
            self.config.append("kraken_db_folder={}".format(arguments["--release-the-kraken"]))
            

        if self.is_integrated_sample:
            self.config.append("is_integrated_sample={}".format("True"))


        if any(x for x in arguments["--option"] if x in options) and self.is_this_an_integration_run is False:
            self.config.append("option={}".format(arguments["--option"][0]))
         
        elif self.is_this_an_integration_run:
            self.config.append("option=integration")
        if arguments["--dry"]:
            self.snakemake = self.snakemake + " -n "
        if arguments["--unlock"]:
            self.snakemake = self.snakemake + " --unlock "
        if arguments["--remove"]:
            self.snakemake = self.snakemake + " --delete-all-output "
        
        self.add_config_argument()
        
    
    def write_to_log(self,start):
        logname = "_".join(["cellsnake",self.runid, datetime.datetime.now().strftime("%y%m%d_%H%M%S"),"runlog"])
        stop = timeit.default_timer()
        with open(logname,"w") as f:
            f.write(__logo__ + "\n")
            f.write("Run ID : " + __version__ + "\n")
            f.write("Cellnake version : " + self.runid + "\n")
            f.write("Cellsnake arguments : " + " ".join(sys.argv) + "\n\n")
            f.write("------------------------------" + "\n")
            f.write("Snakemake arguments : " + str(self.snakemake) + "\n\n")
            f.write("------------------------------" + "\n")
            f.write("Run parameters: " + str(self.parameters) + "\n\n")
            f.write("Total run time: {t:.2f} mins \n".format(t=(stop-start)/60))






def run_cellsnake(arguments):
    start = timeit.default_timer()
    if  "integration" in arguments["--option"]:
        try:
            snakemake_argument=run_integration(arguments)
            snakemake_argument.write_to_log(start)
        except:
            pass
            """
            if not arguments["--dry"]:
                print(arguments)
                snakemake_argument=run_workflow(arguments,option=["minimal"])
                print(arguments)
                snakemake_argument.write_to_log(start)
                snakemake_argument=run_integration(arguments)
                snakemake_argument.write_to_log(start)
            """

    else:
        snakemake_argument=run_workflow(arguments)
        snakemake_argument.write_to_log(start)


def run_integration(arguments):

    if not arguments["--remove"]:
        #first run integration
        snakemake_argument=CommandLine()
        snakemake_argument.is_this_an_integration_run = True
        snakemake_argument.prepare_arguments(arguments)
        subprocess.check_call(str(snakemake_argument),shell=True)

    #then run workflow on integrated dataset
    snakemake_argument=CommandLine()
    snakemake_argument.is_this_an_integration_run = False
    snakemake_argument.is_integrated_sample = True
    snakemake_argument.config.append("datafolder=analyses_integrated/seurat/integrated.rds")
    try:
        arguments["--option"].remove("integration")
    except:
        pass
    snakemake_argument.prepare_arguments(arguments)
    subprocess.check_call(str(snakemake_argument),shell=True)
    return snakemake_argument

def run_workflow(arguments,option=None):
    snakemake_argument=CommandLine()
    if option is not None:
        arguments["--option"]=option
    snakemake_argument.prepare_arguments(arguments)
    subprocess.check_call(str(snakemake_argument),shell=True)
    return snakemake_argument


def main():
        cli_arguments = docopt(__doc__, version=__version__)
        if cli_arguments["--generate-template"]:
            print("Generating config.yaml file...")
            print("You can use this as a template for a cellsnake run. You may change the settings.")
            shutil.copyfile(cellsnake_path + "/scrna/config.yaml", 'config.yaml')
            return
        if cli_arguments["--install-packages"]:
            subprocess.check_call(cellsnake_path + "/scrna/workflow/scripts/scrna-install-packages.R")
            return
        else:
            if check_command_line_arguments(cli_arguments) is False:
                return    
            else:
                run_cellsnake(arguments=cli_arguments)
