# Provided by Christoph Flamm
# (Theoretical Biochemistry Group, University of Vienna)

## define rule(s)
rd = ruleGMLString("""
rule [
 ruleID "match-both-kelkule-structures-of-benzene"
 labelType "term"
 left [
  edge [ source 1 target 9 label "=" ]
  edge [ source 10 target 11 label "-" ]
 ]
 context [
  node [ id 1 label "C" ]
  node [ id 2 label "C" ]
  node [ id 3 label "C" ] 
  node [ id 4 label "C" ] 
  node [ id 5 label "C" ]
  node [ id 6 label "C" ]
  node [ id 7 label "C" ]
  node [ id 9 label "O" ]
  node [ id 10 label "H" ]
  node [ id 11 label "H" ]  
  edge [ source 1 target 2 label "-" ]
  edge [ source 2 target 3 label "_X" ]
  edge [ source 3 target 4 label "_U" ]
  edge [ source 4 target 5 label "_Y" ]
  edge [ source 5 target 6 label "_V" ]
  edge [ source 6 target 7 label "_Z" ]
  edge [ source 7 target 2 label "_W" ]
 ]
 right [
  edge [ source 1 target 10 label "-" ]
  edge [ source 1 target 9 label "-" ]
  edge [ source 9 target 11 label "-" ]
 ]
 constrainLabelAny [
  label "Tauto(_X,_U,_Y,_V,_Z,_W)"
  labels [ label "Tauto(-, =, -, =, -, =)" label "Tauto(=, -, =, -, =, -)" ]
 ]
]
""")

## define input mol(s)
h2   = smiles("[H][H]")
mol1 = smiles("O=CC(=C1)C2=C(C=C1)C(C=O)=CC=C2C", "TAU-1")
mol2 = smiles("O=CC1=C2C(=CC=C1)C(C=O)=CC=C2C", "TAU-2")

# ## define strategy
strat = (addSubset(inputGraphs) >> repeat[3](inputRules))

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
