rule [
	ruleID "3.1.1.b R01462"
	labelType "term"
	left [
		edge [ source 3 target 4 label "-" ]
		edge [ source 5 target 7 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "_B" ]
		node [ id 3 label "O" ]
		node [ id 4 label "_C" ]
		node [ id 5 label "O" ]
		node [ id 6 label "H" ]
		node [ id 7 label "H" ]
		edge [ source 0 target 1 label "=" ]
		edge [ source 1 target 2 label "-" ]
		edge [ source 1 target 3 label "-" ]
		edge [ source 5 target 6 label "-" ]
	]
	right [
		edge [ source 3 target 7 label "-" ]
		edge [ source 4 target 5 label "-" ]
	]
	constrainLabelAny [
		label "_A"
		labels [ label "C" ]
	]
	constrainLabelAny [
		label "_C"
		labels [ label "C" ]
	]
]