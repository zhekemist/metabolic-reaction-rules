# Miscellaneous Scripts

The various scripts in `bin/utils` are shortly described here. 
Most of them provide information about their arguments via the `-h` command line flag.

#### KEGG-ID Checker

- reads a list of supposed KEGG-IDs and checks if they still exist in the KEGG database
- outputs a JSON file with a list containing elements of the form `{"id": <supposed KEGG-ID>,"exists": boolean}`

#### Data Preparation Script for the Rule Testing

- probably non-reusable script, which had the objective of cleaning the reaction and compounds data
- most importantly performs the following actions:
  - remove invalid compound entries, i.e. the ones without SMILES representation
  - unify compounds, which are isomorphic to each other
  - replace compounds, which have non-connected structures, with alternative graphs specified in the config

#### Rule Assistant

- simple program for slightly improving the workflow while creating GML rules
- allows the user to select a GML reaction rule file, which will then be visualized in a PDF using MØD, if the file changes the script will automatically recompile the PDF
- additionally has a feature to create the skeleton of a reaction rule from a SMILES string

#### Rule Formatter

- properly formats GML graph rewrite rules in a given directory by loading them into MØD and reserializing them
- also supports GML templates

#### `viz` scripts

- useful utility scripts to visualize SMILES strings or graph rewrite rules in GML format using MØD
- visualization of GML reaction rules with `vizRule` also supports GML templates

```bash
~$ python vizSMI.py -s 'CC(C(=O)C)C1CCCC1' 'CC(C(=O)C)C1CCC(C)CC1'
~$ python vizRule.py ../Rules/1_1_1_a.gml ../Rules/1_1_1_a_rev.gml
```