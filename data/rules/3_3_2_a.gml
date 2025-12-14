rule [
	ruleID "3.3.2.a R04609"
	labelType "term"
	left [
		edge [ source 0 target 2 label "-" ]
		edge [ source 4 target 9 label "-" ]
	]
	context [
		node [ id 0 label "O" ]
		node [ id 1 label "H" ]
		node [ id 2 label "H" ]
		node [ id 3 label "C" ]
		node [ id 4 label "C" ]
		node [ id 5 label "_A" ]
		node [ id 6 label "_B" ]
		node [ id 7 label "_C" ]
		node [ id 8 label "_D" ]
		node [ id 9 label "O" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 3 target 5 label "-" ]
		edge [ source 3 target 6 label "-" ]
		edge [ source 3 target 9 label "-" ]
		edge [ source 4 target 7 label "-" ]
		edge [ source 4 target 8 label "-" ]
	]
	right [
		edge [ source 0 target 4 label "-" ]
		edge [ source 2 target 9 label "-" ]
	]
]