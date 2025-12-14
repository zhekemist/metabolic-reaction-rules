# Provided by Christoph Flamm
# (Theoretical Biochemistry Group, University of Vienna)

## define rule(s)
rd = ruleGMLString("""
rule [
 ruleID "reduction of aldehyde-not-ketone"
 labelType "term"
 left [
  edge [ source 1 target 2 label "=" ]
  edge [ source 5 target 6 label "-" ]
 ]
 context [
  node [ id 1 label "C" ] 
  node [ id 2 label "_X" ] 
  node [ id 3 label "_Y" ] 
  node [ id 4 label "_Z" ] 
  node [ id 5 label "H" ]
  node [ id 6 label "H" ]
  edge [ source 1 target 3 label "-" ]
  edge [ source 1 target 4 label "-" ]
 ]
 right [
  edge [ source 1 target 2 label "-" ]
  edge [ source 1 target 6 label "-" ]
  edge [ source 2 target 5 label "-" ]
 ]
 constrainLabelAny [
  label "Ald(_X,_Y,_Z)"
  labels [ label "Ald(O, H, C)" label "Ald(S, H, C)" ]
 ]
]
""")

## define input mol(s)
h2   = smiles("[H][H]")
mol1 = smiles("O=CC=S")
mol2 = smiles("CC(=O)C(=S)")
mol3 = smiles("O=CC(=S)C")
mol4 = smiles("CC(=O)C(=S)C")

# ## define strategy
strat = (addSubset(inputGraphs) >> repeat[2](inputRules))

# ## switch to term rewite
ls = LabelSettings(LabelType.Term, LabelRelation.Unification)

# ## build derivation graph
dg = DG(graphDatabase=inputGraphs, labelSettings=ls)
dg.build().execute(strat)

# ## print results
# print derivation graph
dg.print()

# print input rule(s)
for r in inputRules:
    p = GraphPrinter()
    p.setReactionDefault()
    p.withIndex = True
    r.print(p)

# print input mol(s)
for m in inputGraphs:
    m.print()
