#!/usr/bin/env python
'''
Created on 02/12/2022
cellsnake main
@author: Sinan U. Umu, sinanugur@gmail.com
'''

#from __future__ import print_function
import re
from docopt import docopt
import os
import sys
import subprocess
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

__doc__="""Main cellsnake executable

Usage:
    cellsnake --input <text> [--cpu <integer>] 
    cellsnake --input <text> [--unlock|--remove] [--dry]
    cellsnake (-h | --help)
    cellsnake --version

Arguments:
    -i <text>, --input <text>              Input directory or a file to process.
    -c <integer>, --cpu <integer>          CPUs. [default: 2]

Options:
    -u, --unlock            Rescue stalled jobs (Try this if the previous job ended prematurely).
    -r, --remove            Clear all output files (this won't remove input files).
    -d, --dry               Dry run, nothing will be generated.
    -h, --help              Show this screen.
    --version               Show version.

"""


def run_cellsnake():
    arguments = docopt(__doc__, version=__version__)
    params="'{p}'".format(p=" ".join(sys.argv))
    dry_run="-n" if arguments["--dry"] else ""
    unlock="--unlock" if arguments["--unlock"] else ""
    remove="--delete-all-output" if arguments["--remove"] else ""
    print(type(arguments['--cpu']))
    snakemake_argument="snakemake --rerun-incomplete {dry} {unlock} {remove} -j {cpu} -s {cellsnake_path}/workflow/Snakefile --config cellsnake_path={cellsnake_path} --configfile=config.yaml".format(
    cpu=arguments['--cpu'],
    cellsnake_path=cellsnake_path,
    dry=dry_run,
    unlock=unlock,
    remove=remove,
    params=params)
    
    subprocess.check_call(snakemake_argument,shell=True)



def main():
        run_cellsnake()

