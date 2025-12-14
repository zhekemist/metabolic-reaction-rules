# Initial version provided by Christoph Flamm
# (Theoretical Biochemistry Group, University of Vienna)
# usage: vizSMI.py -s SMILES1 -s SMILES2 ...

import argparse
import os
import subprocess
import sys

from gmltools.modimport import mod, mod_loc, mod_lib
from mod import *

# make sure that out directory exists
if not os.path.exists("./out"): os.makedirs("./out")

modpost = mod_loc + '_post'

# create command line argument parser object
parser = argparse.ArgumentParser(description
                                 ='Visualize SMILES strings using mød')

# define command line argument --smi
parser.add_argument('-s', '--smi',
                    nargs='+',
                    help="<required> specify SMILES string (option can be given multiple times)",
                    required=True,
                    type=str)

# parse command line
args = parser.parse_args()

for mol in args.smi:
    smiles(mol)

for m in inputGraphs:
    m.print()

post.flushCommands()
subprocess.run([modpost])

print('\nTo look at a graphical rendering of the SMILES use the command:\n',
      '\n  evince summary/summary.pdf &\n')
