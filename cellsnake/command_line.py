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


__author__ = 'Sinan U. Umu'
__version__= '0.1.0'


__licence__="""
MIT License
Copyright (c) 2022 Sinan Ugur Umu (SUU) sinanugur@gmail.com
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

Usage:
    cellsnake <INPUT> [--resolution <text>] [--percent_mt <text>] [--configfile <text>] [--jobs <integer>] [--species <text>] [--dry]
    cellsnake <INPUT> --only-clustree [--percent_mt <text>] [--configfile <text>] [--jobs <integer>] [--dry]
    cellsnake <INPUT> --minimal [--resolution <text>] [--percent_mt <text>] [--configfile <text>] [--jobs <integer>] [--species <text>] [--dry]
    cellsnake --seurat-integration [--resolution <text>]  [--configfile <text>] [--jobs <integer>] [--species <text>] [--dry]
    cellsnake <INPUT> [--unlock|--remove] [--dry]
    cellsnake --generate-configfile-template
    cellsnake (-h | --help)
    cellsnake --version

Arguments:
    INPUT                                   Input directory or a file to process (if a directory given, batch mode is ON).
    -c <test>, --configfile <text>          Config file name (if not supplied, it will use default settings, you may generate a template, change it and use it in your runs).
    --resolution <text>                     Resolution for cluster detection, write "auto" for auto detection [default: 0.8].
    --percent_mt <text>                     Maximum mitochondrial gene percentage cutoff, for example 5 or 10 [default: auto]. NA for integration.
    -j <integer>, --jobs <integer>          Total CPUs. [default: 2]
    --species <text>                        Species: human or mouse [default: human] 
    --gene <text>                           Create publication ready plots for a selected gene. You need an RDS file from the main pipeline.

Options:
    --only-clustree                    Generate only clustree plot (see github.com/lazappi/clustree).
    --generate-configfile-template     Generate config file template in the current directory.
    --seurat-integration               Use Seurat integration, run inside a "cellsnake" folder after regular workflow successfully concludes for multiple samples.
    --minimal                          Minimal pipeline, will skip marker analysis. Better to use for later integration.
    -u, --unlock                       Rescue stalled jobs (Try this if the previous job ended prematurely).
    -r, --remove                       Clear all output files (this won't remove input files).
    -d, --dry                          Dry run, nothing will be generated.
    -h, --help                         Show this screen.
    --version                          Show version.

"""


class CommandLine:
    def __init__(self):
        self.snakemake="snakemake --rerun-incomplete"
        self.runid="".join(random.choices("abcdefghisz",k=3) + random.choices("123456789",k=5))
        self.config=[]
        self.configfile=False
        self.is_integrated_sample=False
        self.is_this_an_integration_run=False
        self.paramaters=dict()
        
    def __str__(self):
        return self.snakemake
    def __repr__(self):
        return self.snakemake
    
    def check_arguments(self,arguments):
        if not os.path.exists(arguments["<INPUT>"]) and self.is_this_an_integration_run is False:
            print("File or directory not found:",arguments["<INPUT>"])
            return False


        

    def add_config_argument(self):
        self.snakemake = self.snakemake + " --config " + " ".join(self.config)


    def load_and_add_default_configfile_argument(self,arguments):
        if self.configfile is False:
            if arguments["--configfile"]:
                self.snakemake = self.snakemake + " --configfile={}".format(arguments["--configfile"])
                configfile=arguments["--configfile"]
            else:
                self.snakemake = self.snakemake + " --configfile={}".format(cellsnake_path + "/scrna/config.yaml")
                configfile=cellsnake_path + "/scrna/config.yaml"

            with open(configfile) as f:
                self.paramaters=yaml.load(f,Loader=SafeLoader)
            self.configfile=True
        self.change_paramaters(arguments)

    def change_paramaters(self,arguments):
        if self.configfile is True:
            self.paramaters["resolution"] = arguments["--resolution"]
            self.paramaters["percent_mt"] = arguments["--percent_mt"]
            self.paramaters["species"] = arguments["--species"]




        

    def prepare_arguments(self,arguments):
        self.snakemake = self.snakemake +  " -j {} ".format(arguments['--jobs']) #set CPU number
        self.snakemake = self.snakemake +  " -s {} ".format(f"{cellsnake_path}/scrna/workflow/Snakefile") #set Snakefile location
        self.load_and_add_default_configfile_argument(arguments)
        if self.is_this_an_integration_run is False and self.is_integrated_sample is False:
            self.config.append("datafolder={}".format(arguments['<INPUT>']))

        self.config.append(f"cellsnake_path={cellsnake_path}/scrna/")
        self.config.append("resolution={}".format(arguments["--resolution"]))
        self.config.append("percent_mt={}".format(arguments["--percent_mt"]))
        self.config.append("species={}".format(arguments["--species"]))
        if self.is_integrated_sample:
            self.config.append("is_integrated_sample={}".format("True"))


        if arguments["--only-clustree"]:
            self.config.append("route=clustree")
        elif arguments["--minimal"]:
            self.config.append("route=minimal")
        elif self.is_this_an_integration_run:
            self.config.append("route=integration")
        if arguments["--dry"]:
            self.snakemake = self.snakemake + " -n "
        if arguments["--unlock"]:
            self.snakemake = self.snakemake + " --unlock "
        
        self.add_config_argument()
        
    
    def write_to_log(self,start):
        filename = "_".join(["cellsnake",self.runid, datetime.datetime.now().strftime("%y%m%d_%H%M%S"),"runlog"])
        stop = timeit.default_timer()
        with open(filename,"w") as f:
            f.write("Cellsnake command line arguments: " + " ".join(str(sys.argv)) + "\n")
            f.write("Snakemake workflow arguments: " + str(self.snakemake) + "\n")
            f.write(str(self.paramaters) + "\n")
            f.write("Total run time: {t:.2f} mins \n".format(t=(stop-start)/60))






def run_cellsnake(arguments):
    start = timeit.default_timer()
    snakemake_argument=CommandLine()
    #if snakemake_argument.check_arguments(arguments) is False:
    #    return
    
    

    if arguments["--seurat-integration"]:
        snakemake_argument.is_this_an_integration_run = True
        snakemake_argument.prepare_arguments(arguments)
        #print (str(snakemake_argument))
        subprocess.check_call(str(snakemake_argument),shell=True)
        snakemake_argument=CommandLine()
        snakemake_argument.is_this_an_integration_run = False
        snakemake_argument.is_integrated_sample = True
        snakemake_argument.config.append("datafolder=analyses_integrated/seurat/combined.rds")
    
    snakemake_argument.prepare_arguments(arguments)
    
    #print (str(snakemake_argument))
    subprocess.check_call(str(snakemake_argument),shell=True)
    snakemake_argument.write_to_log(start)


"""
def run_cellsnake(arguments):
    params="'{p}'".format(p=" ".join(sys.argv))

    dry_run="-n" if arguments["--dry"] else ""
    unlock="--unlock" if arguments["--unlock"] else ""
    configfile=arguments['--configfile'] if arguments['--configfile'] else cellsnake_path + "/scrna/config.yaml"
    remove="--delete-all-output" if arguments["--remove"] else ""
    clustree="route=clustree" if arguments["--only-clustree"] else ""


    snakemake_argument="snakemake --rerun-incomplete {dry} {unlock} {remove} -j {jobs} -s {cellsnake_path}workflow/Snakefile --config cellsnake_path={cellsnake_path} {clustree} --configfile={configfile}".format(
    jobs=arguments['--jobs'],
    configfile=configfile,
    cellsnake_path=cellsnake_path + "/scrna/",
    dry=dry_run,
    clustree=clustree,
    unlock=unlock,
    remove=remove,
    params=params)
    
    subprocess.check_call(snakemake_argument,shell=True)
"""


def main():
        arguments = docopt(__doc__, version=__version__)
        if arguments["--generate-configfile-template"]:
            print("Generating config.yaml file...")
            print("You can use this as a template for a cellsnake run. You may change the settings.")
            shutil.copyfile(cellsnake_path + "/scrna/config.yaml", 'config.yaml')
            return
        run_cellsnake(arguments)
