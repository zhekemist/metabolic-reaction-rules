rule [
	ruleID "5.3.2.b R04163"
	labelType "term"
	left [
		edge [ source 2 target 3 label "-" ]
		edge [ source 2 target 8 label "-" ]
		edge [ source 3 target 4 label "=" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "C" ]
		node [ id 3 label "C" ]
		node [ id 4 label "C" ]
		node [ id 5 label "_B" ]
		node [ id 6 label "_C" ]
		node [ id 7 label "_D" ]
		node [ id 8 label "H" ]
		node [ id 9 label "_E" ]
		node [ id 10 label "O" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 2 label "-" ]
		edge [ source 1 target 10 label "=" ]
		edge [ source 2 target 9 label "-" ]
		edge [ source 3 target 7 label "-" ]
		edge [ source 4 target 5 label "-" ]
		edge [ source 4 target 6 label "-" ]
	]
	right [
		edge [ source 2 target 3 label "=" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 4 target 8 label "-" ]
	]
]