rule [
	ruleID "4.1.1.g R04223"
	labelType "term"
	left [
		edge [ source 6 target 9 label "-" ]
		edge [ source 9 target 11 label "-" ]
		edge [ source 11 target 13 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "C" ]
		node [ id 3 label "_B" ]
		node [ id 4 label "C" ]
		node [ id 5 label "_C" ]
		node [ id 6 label "C" ]
		node [ id 7 label "_D" ]
		node [ id 8 label "_F" ]
		node [ id 9 label "C" ]
		node [ id 10 label "O" ]
		node [ id 11 label "O" ]
		node [ id 12 label "O" ]
		node [ id 13 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 2 label "-" ]
		edge [ source 1 target 12 label "=" ]
		edge [ source 2 target 3 label "-" ]
		edge [ source 2 target 4 label "=" ]
		edge [ source 4 target 5 label "-" ]
		edge [ source 4 target 6 label "-" ]
		edge [ source 6 target 7 label "-" ]
		edge [ source 6 target 8 label "-" ]
		edge [ source 9 target 10 label "=" ]
	]
	right [
		edge [ source 6 target 13 label "-" ]
		edge [ source 9 target 11 label "=" ]
	]
	constrainLabelAny [
		label "_A"
		labels [ label "O" label "S" label "C" label "H" ]
	]
]