rule [
	ruleID "4.2.1.f R03593"
	labelType "term"
	left [
		edge [ source 1 target 2 label "#" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 3 target 5 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "N" ]
		node [ id 3 label "O" ]
		node [ id 4 label "H" ]
		node [ id 5 label "H" ]
		edge [ source 0 target 1 label "-" ]
	]
	right [
		edge [ source 1 target 2 label "-" ]
		edge [ source 1 target 3 label "=" ]
		edge [ source 2 target 4 label "-" ]
		edge [ source 2 target 5 label "-" ]
	]
]