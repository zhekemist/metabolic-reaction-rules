# Initial version provided by Christoph Flamm
# (Theoretical Biochemistry Group, University of Vienna)
# usage: vizRule.py -r FOO.gml -r BAR.gml ...

import argparse
import re
import subprocess
import os

from gmltools.modimport import mod, mod_loc, mod_lib
from mod import *

# make sure that out directory exists
if not os.path.exists("./out"): os.makedirs("./out")

modpost = mod_loc + '_post'

# create command line argument parser object
parser = argparse.ArgumentParser(description
                                 ='Visualize graph rewrite rules using mød')

# define command line argument
parser.add_argument('rule',             # change to position args for easier usage with bash globs
                    nargs='+',
                    help="<required> specify rule file name (option can be given multiple times)",
                    type=str)

# parse command line
args = parser.parse_args()

p = GraphPrinter()
p.setReactionDefault()
p.withIndex = True


def print_template(raw_string):
    start = raw_string.find('{Template}') + 10
    end = raw_string.find('{Group:', start)
    end = end if end != -1 else len(raw_string)
    rule = mod.ruleGMLString(raw_string[start:end])
    rule.print(p)
    groups = re.findall(r'{Group:(\w+):(\d+)}((?:"{\w*}"|[^{])+)', raw_string, re.DOTALL)
    for group in groups:
        name_string = f'Group {group[0]} (Link-Node: {group[1]})'
        graph = mod.graphGMLString(group[2], name_string)
        graph.print(p)


for rule in args.rule:
    if not os.path.exists(rule):
        print("Error: file `{:s}' does not exist!".format(rule),
              file=sys.stderr)
    else:
        with open(rule, 'r') as f:
            raw_string = f.read()
        if '{Template}' in raw_string:
            print_template(raw_string)
        else:
            rule = mod.ruleGMLString(raw_string)
            rule.print(p)

# generate summary/summery.pdf
post.flushCommands()
subprocess.run([modpost])

print('\nTo look at a graphical rendering of the RULES use the command:\n',
      '\n  evince summary/summary.pdf &\n')
