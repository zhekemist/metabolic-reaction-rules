# GML Templates

GML Templates can be used to express some reaction rules and constraints that would otherwise be too complex to be formalized as MØD compatible GML rules. These templates can subsequently be "compiled" into a set of equivalent vanilla GML rules.

## Syntax

The grammar of the GML templates (syntax based on the MØD-Docs)
would be roughly specifiable as follows:

```
<template>       ::= <groupTemplate>* <ruleTemplate> <groupTemplate>*
<ruleTemplate>   ::= '{Template}' <ruleGML>
<groupTemplate>  ::= '{Group:' simpleString ':' <linkID> '}' <graphGML>
```

The definitions for `ruleGML` and `graphGML` are largely adopted from MØD:

```
<graphGML> ::= 'graph [' (<node> | <edge>)* ']'
<node>     ::= 'node [ id' int 'label' ( quoteEscapedString | groupLabelString ) ']'
<edge>     ::= 'edge [ source' int 'target' int 'label' quoteEscapedString ']'
```

```
<ruleGML>       ::= 'rule ['
                       [ 'ruleID' quoteEscapedString ]
                       [ 'labelType "' <labelType> '"' ]
                       [ <leftSide> ]
                       [ <context> ]
                       [ <rightSide> ]
                       <labelConstraint>*
                    ']'
<labelType>       ::= 'string' | 'term'
<leftSide>        ::= 'left [' ( <node> | <edge>)* ']'
<context>         ::= 'context [' (<node> | <edge>)* ']'
<rightSide>       ::= 'right [' (<node> | <edge>)* ']'
<labelConstraint> ::= 'constrainLabelAny ['
                        'label' firstOrderTerm
                        'labels' [ labelList ]
                      ']'
<labelList>       ::= ('label' ( quoteEscapedString | groupLabelString ))*
```

The mentioned types of strings are defined below:
```
groupLabelString ::= '"{' simpleString '}"'
quoteEscapedString ::= '"' simpleString '"'
simpleString ::= [a-zA-Z0-9_]+
```

An example for such a template can be found [here](examples/template.gml).

## Semantics

A GML template file can be seperated in two parts:
1. **specification of the reaction rule**: This part is preceded by the `{Template}` tag and simply contains the reaction rule in the usual format, which is required by MØD. The only difference is that, instead of only specifying simple atoms as label for nodes, it is additionally also possible to use symbols for functional groups as labels for nodes, including as options for constraints. A label is recognized as group symbol, when enclosed by curly braces `{<symbol>}`. In the [example](examples/template.gml) this feature is used in line 20 and 38. 
2. **definition of the group symbols**: The file can include multiple definitions of group symbols, which in turn can be used in other group definitions and of course in the reaction rule. The header of the group definition follows the following pattern: `{Group:<symbol>:<linkID>}` and is followed by the specifications of the functional groups graph in the typical syntax from MØD.

Afterward, at compile time, roughly the following actions are performed: 
- The compiler looks for group symbols directly used in the reaction rule (i.e. not as options in a constraint) and substitutes the respective pseudoatom with the graph from the group symbol definition. The node that will take the place of the former pseudoatom is the one specified via its ID (`<linkID>` in the group header).
- All the label constraints are scanned for group symbols, then all possible combinations of the various constraints are generated and for each combination a single vanilla GML rule is outputted, in which the constrained labels were substituted by the corresponding graphs as above.
- First-order terms will be renamed to include a unique number appended to the name. The purpose of this is that when inserting one and the same group several times, the terms can be unified independently of each other, which is probably the desired behavior.

Both actions are done repeatedly until no group symbol exist in the rule anymore, in order to allow the groups to contain groups symbols themselves. Consequently, if there exists a "referential cycle" the compiler will probably not terminate.

It has to be notes that the compiler currently only supports a subset of the MØD reaction rule syntax, e.g. not supported are:
1. First-order terms more complicated than simple variables, in particular no first-order functions
2. Charges, Isotopes, etc. on groups symbols

Also, the compiler barely performs any verification of correctness, therefore malformed templates will either produce nonsense output (GIGO) or sudden runtime errors.

## Compiler Usage

```bash
~$ python bin/compile_templates.py 
      -t <path/to/template.gml> 
      -o <output directory>
      -g <path/to/groups_file.gml>
```

- `-t --template`: 
  - **required**
  - specifies the path to the template file
  - if multiple paths are given, then each template is compiled independently
- `-o --out-dir`: 
  - specifies the output directory
  - default: './compiler_out'
- `-g --groups-file`:
  - specifies the path to a file containing additional group definitions, 
useful for defining a standard set of commonly used groups
  - if no path is explicitly given, the working directory and its subdirectories are scanned
for a file named 'groups.gml'


