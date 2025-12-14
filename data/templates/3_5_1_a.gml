{Template}

rule [
	ruleID "3.5.1.a R03250"
	labelType "term"
	left [
		edge [ source 0 target 2 label "-" ]
		edge [ source 3 target 4 label "-" ]
	]
	context [
		node [ id 0 label "C" ]
		node [ id 1 label "_A" ]
		node [ id 2 label "_B" ]
		node [ id 3 label "O" ]
		node [ id 4 label "H" ]
		node [ id 5 label "H" ]
		node [ id 6 label "O" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 0 target 6 label "=" ]
		edge [ source 3 target 5 label "-" ]
	]
	right [
		edge [ source 0 target 3 label "-" ]
		edge [ source 2 target 4 label "-" ]
	]
	constrainLabelAny [
		label "_B"
		labels [ label "{DB}" label "{SB}" ]
	]
]

{Group:SB:0}

graph [
  node [ id 0 label "N" ]
  node [ id 1 label "_C" ]
  node [ id 2 label "_D" ]
  edge [ source 0 target 1 label "-" ]
  edge [ source 0 target 2 label "-" ]  
]

{Group:DB:0}

graph [
  node [ id 0 label "N" ]
  node [ id 1 label "_C" ]
  edge [ source 0 target 1 label "=" ]
]
