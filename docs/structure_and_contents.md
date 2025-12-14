# Project Structure and Contents

- `bin/`: contains all the code file which can be directly executed from the command line
  - `compile_templates.py`: used to invoke the template compiler, unfortunately also includes its complete source code
  - `ruletest.py`: can be used to start the "unit test" for GML Rules
  - `utils/`: contains various other scripts with different functions and varying degrees of usefulness, as described here
- `data/`: contains the data, which was produced during the project and on which the scripts operate; additionally, it also contains some configurations files for the scripts.
  - `rules/`: all the GML rules that have been created in the course of this project are stored here, including the rules that were output during the compilation of the GML templates
  - `templates/`: the few produced, uncompiled GML templates are contained here
  - `groups.gml`: contains some functional group definitions for symbols that were used as shortcuts in the GML templates, therefore required if the templates are recompiled
  - `iAF1260b_{chems, reacs}.json`: cleaned and preprocessed reaction and compound data from the BiGG iAF1260b model as a foundation for testing the GML rules
  - `preparation_config.json`: used configuration file for the `bin/utils/prepare_ruletest_data.py` script
  - `test_config.json`: used configuration file for the GML rule test
- `docs/`: documentation and various examples
- `gmltools/`: package containing the main functionalities of the project, i.e. the rule test, part of the template compiler should be moved here too
  - `ruletest/`: the `RuleTest`class, which can be used for testing the GML rules, is contained here
  - `specialization/`: contains purely experimental and mainly useless code with the overall objective of making given GML rules more specific
  - `kegg.py`: contains a few functions to fetch data through KEGG database ids
  - `modimport.py`: helper module for loading the MØD python package
