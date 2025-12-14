rule [
	ruleID "3.5.3.b R03250"
	labelType "term"
	left [
		edge [ source 0 target 2 label "-" ]
		edge [ source 3 target 9 label "-" ]
	]
	context [
		node [ id 0 label "O" ]
		node [ id 1 label "H" ]
		node [ id 2 label "H" ]
		node [ id 3 label "C" ]
		node [ id 4 label "N" ]
		node [ id 5 label "_A" ]
		node [ id 6 label "_B" ]
		node [ id 7 label "_C" ]
		node [ id 8 label "_D" ]
		node [ id 9 label "N" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 3 target 4 label "=" ]
		edge [ source 3 target 6 label "-" ]
		edge [ source 4 target 5 label "-" ]
		edge [ source 7 target 9 label "-" ]
		edge [ source 8 target 9 label "-" ]
	]
	right [
		edge [ source 0 target 3 label "-" ]
		edge [ source 2 target 9 label "-" ]
	]
]