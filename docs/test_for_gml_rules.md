# Test for GML Rules

The idea behind the test for the GML rules is described in more detail in the thesis, especially in the chapters *Grundideen* and *Implementierung*.
The basic principle is the following: The input for the test is a set of reaction rules, along with data about the actually expected reactions and the structures of the participating compounds.
For each of the reaction rules the following steps are performed:
1. **preselection of educts**: The structure patterns on the left side of the rule are split into connected components and fitting educt candidates among the real compounds selected by finding monomorphism from the pattern onto the compounds.
2. **application of the rules**: The reaction rule is then applied to the compounds selected in the previous step.

At the end the results of all the different rules are gathered as one and the following information collected:
1. **unexpected educts**: compounds, which matched with at least one of the rules, but never appear as an educt in the real reactions
2. **missing educts**: compounds, which appeared as an educt in the reference data, but did not match with any rule
3. **unexpected products**: compounds that were produced by the application of at least one rule, but never appeared on the product side of any reference reaction
4. **missing products**: compounds, which, according to the reference data, should have been produced by at least one rule, but did not

The two "missing categories" can only be output for the entire set of reaction rules, while the two "unexpected categories" are additionally grouped by the reaction rules, i.e. it is also indicated which of the reaction rules led to the unexpected compound.

## Usage

```bash
~$ python bin/ruletest.py 
      -d dir/with/rules 
      -r path/to/reaction_data.json
      -c path/to/compound_data.json
      [-cf path/to/test_config.json]
      [--debug]
      <3rd level ec numbers, e.g. 1.1.1>
```

- `-d --ruledir`:
    - **required**
    - directory which contains the GML reaction rule files
- `-r --reactions-data`:
    - **required**
    - file containing the data for the reaction
- `-c --compounds-data`:
    - **required**
    - file containing the data for the compounds
- `-cf --config`:
    - configuration file for the test
    - contains the cofactor declarations and ids
- `--debug`:
    - flag to set logger level to `logging.DEBUG`
    - outputs a little bit more information while running the test
- `<3rd level ec numbers>`:
  - **required**
  - format: `x.y.z`
  - used for:
    1. selecting the relevant GML rules, practically with the pattern `ruledir/x_y_z_*.gml`
    2. filtering out reactions belonging to the class from the reference data
  - if multiple EC-classes are given, then each of them is tested independently
    
#### Example usage with this repo

```bash
~$ python bin/ruletest.py -d data/rules -r data/iAF1260b_reacs.json -c data/iAF1260b_chems.json -cf data/test_config.json 1.1.1
```
- runs the test for the set of reaction rules pertaining to the class 1.1.1

## Input and Configuration

The required JSON-format for the compounds data is a list with elements containing at least the following key-value pairs:
1. `"id"`: unique compound identifier, in the given data: MetaNetX-ID
2. `"smiles"`: SMILES string of the compound's structure OR `"graphDFS"`: graphDFS string as an alternative, if the compound cannot be expressed with SMILES

The format for the reaction data however requires the following pairs:
1. `"id"`: unique identifier, in the give data: again the MetaNetX-ID
2. `"equation_decomposed"`: subobject containing the keys `"lhs"` and `"rhs"`, each with lists as values, which again contain subobjects at least embodying the identifiers of the involved compounds in the `"id"` field. These compound ids need to be consistent with the one used in the file with the compounds data.
3. `"ec":` list of EC classes with which the reaction can be classified
4. `"to_lhs"` and `"to_rhs"`: booleans indicating the direction of the reaction, bidirectional reactions are supported

Additional information in the JSON file is silently ignored, as can also be seen with the data in this repository.

Furthermore, the test can be configured to give special treatment to some compounds, which is a feature especially introduced for usage with common cofactors.
The special processing concerns the following aspects:
- cofactors are ignored during the gathering of the four categories described above
- cofactors will be added to the set of educt candidates for every reaction rule unconditionally

This is also why these special compounds are configured in two parts in the configuration JSON object:
1. `"cofactors"`: list of graphDFS strings, representing the structures of the cofactors
2. `"cofactor_ids"`: list of the cofactors ids, which need to be consistent with the ids in the file containing the compounds
  
## Output

The results of the test are written to a JSON file in a format that is consistent with categorization, which was described earlier.
At the highest level the file is split into a `"total"` part, which contains the "missing categories", and an `"individual"`  part that contains
the result for the "unexpected categories" grouped by the name of the reaction rule (as given in the `ruleID` field of the corresponding GML file).

If a compound occurs in the inputted compounds the output will contain the id that was give there otherwise the compound
will be outputted as a graphDFS string, prefixed by `graphDFS:`.