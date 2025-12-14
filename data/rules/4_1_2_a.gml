rule [
	ruleID "4.1.2.a R01983"
	labelType "term"
	left [
		edge [ source 1 target 3 label "-" ]
		edge [ source 3 target 6 label "-" ]
		edge [ source 6 target 7 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "O" ]
		node [ id 3 label "C" ]
		node [ id 4 label "_B" ]
		node [ id 5 label "_C" ]
		node [ id 6 label "O" ]
		node [ id 7 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 2 label "=" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 3 target 5 label "-" ]
	]
	right [
		edge [ source 1 target 7 label "-" ]
		edge [ source 3 target 6 label "=" ]
	]
	constrainLabelAny [
		label "_A"
		labels [ label "H" label "C" ]
	]
]