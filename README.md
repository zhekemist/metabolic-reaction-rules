# Metabolic Reaction Rules

This repository contains a collection of metabolic reaction rules in GML format (see `data/rules`), derived from the referenced paper by [Henry et al. (2010)](https://doi.org/10.1002/bit.22673). It also provides tools for writing, visualizing, and evaluating these rules.

# Requirements

The required Python packages are listed in `conda_env.txt`. In addition, the chemoinformatics software package [MOD](https://jakobandersen.github.io/mod/) (version 0.14.0) must be installed separately for the tools in this repository to function correctly.

# Docs

1. [Project Structure And Contents](docs/structure_and_contents.md)
2. [GML Templates](docs/gml_templates.md)
   1. [Syntax](docs/gml_templates.md#syntax)
   2. [Semantics](docs/gml_templates.md#semantics)
   3. [Compiler Usage](docs/gml_templates.md#compiler-usage)
3. [Test for GML Rules](docs/test_for_gml_rules.md)
   1. [Usage](docs/test_for_gml_rules.md#usage)
   2. [Input and Configuration](docs/test_for_gml_rules.md#input-and-configuration)
   3. [Output](docs/test_for_gml_rules.md#output)
4. [Miscellaneous Scripts](docs/misc_scripts.md)