rule [
	ruleID "5.3.2.a R03671"
	labelType "term"
	left [
		edge [ source 1 target 2 label "=" ]
		edge [ source 2 target 4 label "-" ]
		edge [ source 4 target 6 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "C" ]
		node [ id 3 label "_B" ]
		node [ id 4 label "O" ]
		node [ id 5 label "_C" ]
		node [ id 6 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 5 label "-" ]
		edge [ source 2 target 3 label "-" ]
	]
	right [
		edge [ source 1 target 2 label "-" ]
		edge [ source 1 target 6 label "-" ]
		edge [ source 2 target 4 label "=" ]
	]
]