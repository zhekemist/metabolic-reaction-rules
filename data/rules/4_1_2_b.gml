rule [
	ruleID "4.1.2.b R05648"
	labelType "term"
	left [
		edge [ source 2 target 5 label "-" ]
		edge [ source 5 target 7 label "-" ]
		edge [ source 7 target 10 label "-" ]
	]
	context [
		node [ id 0 label "C" ]
		node [ id 1 label "_A" ]
		node [ id 2 label "C" ]
		node [ id 3 label "_B" ]
		node [ id 4 label "_C" ]
		node [ id 5 label "C" ]
		node [ id 6 label "_D" ]
		node [ id 7 label "O" ]
		node [ id 8 label "_E" ]
		node [ id 9 label "O" ]
		node [ id 10 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 0 target 2 label "-" ]
		edge [ source 0 target 9 label "=" ]
		edge [ source 2 target 3 label "-" ]
		edge [ source 2 target 4 label "-" ]
		edge [ source 5 target 6 label "-" ]
		edge [ source 5 target 8 label "-" ]
	]
	right [
		edge [ source 2 target 10 label "-" ]
		edge [ source 5 target 7 label "=" ]
	]
	constrainLabelAny [
		label "_A"
		labels [ label "C" label "S" label "H" ]
	]
]