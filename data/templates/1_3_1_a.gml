{Template}

rule [
	ruleID "1.3.1.a R01251"
	labelType "term"
	left [
		node [ id 4 label "H" ]
		node [ id 10 label "NAD+" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 3 target 6 label "-" ]
		edge [ source 6 target 8 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "_X" ]
		node [ id 3 label "C" ]
		node [ id 5 label "_B" ]
		node [ id 6 label "C" ]
		node [ id 7 label "_C" ]
		node [ id 8 label "H" ]
		node [ id 9 label "_D" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 2 label "=" ]
		edge [ source 1 target 3 label "-" ]
		edge [ source 3 target 5 label "-" ]
		edge [ source 6 target 7 label "-" ]
		edge [ source 6 target 9 label "-" ]
	]
	right [
		node [ id 4 label "H+" ]
		node [ id 10 label "NAD" ]
		edge [ source 3 target 6 label "=" ]
		edge [ source 8 target 10 label "-" ]
	]
	constrainLabelAny [
		label "_X"
		labels [ label "O" label "{CGr}" label "{NGr}" ]
	]
]

{Group:CGr:0}

graph [
  node [ id 0 label "C" ]
  node [ id 1 label "_E" ]
  node [ id 2 label "_F" ]
  edge [ source 0 target 1 label "-" ]
  edge [ source 0 target 2 label "-" ]
]

{Group:NGr:0}

graph [
  node [ id 0 label "N" ]
  node [ id 1 label "_G" ]
  edge [ source 0 target 1 label "-" ]
]
