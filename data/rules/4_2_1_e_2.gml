rule [
	ruleID "4.2.1.e R02376"
	labelType "term"
	left [
		edge [ source 1 target 7 label "-" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 3 target 6 label "-" ]
		edge [ source 6 target 10 label "-" ]
	]
	context [
		node [ id 0 label "C" ]
		node [ id 1 label "C" ]
		node [ id 2 label "H" ]
		node [ id 3 label "C" ]
		node [ id 4 label "H" ]
		node [ id 5 label "_B_0" ]
		node [ id 6 label "O" ]
		node [ id 7 label "O" ]
		node [ id 8 label "H" ]
		node [ id 9 label "H" ]
		node [ id 10 label "H" ]
		node [ id 11 label "H" ]
		node [ id 12 label "O" ]
		node [ id 13 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 0 target 8 label "-" ]
		edge [ source 0 target 9 label "-" ]
		edge [ source 0 target 12 label "-" ]
		edge [ source 1 target 2 label "-" ]
		edge [ source 1 target 3 label "-" ]
		edge [ source 3 target 5 label "-" ]
		edge [ source 7 target 11 label "-" ]
		edge [ source 12 target 13 label "-" ]
	]
	right [
		edge [ source 1 target 4 label "-" ]
		edge [ source 3 target 6 label "=" ]
		edge [ source 7 target 10 label "-" ]
	]
	constrainLabelAny [
		label "_B_0"
		labels [ label "H" ]
	]
]