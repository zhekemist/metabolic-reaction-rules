rule [
	ruleID "5.4.3.b R02852"
	labelType "term"
	left [
		edge [ source 1 target 6 label "-" ]
		edge [ source 2 target 3 label "-" ]
	]
	context [
		node [ id 0 label "H" ]
		node [ id 1 label "C" ]
		node [ id 2 label "C" ]
		node [ id 3 label "H" ]
		node [ id 4 label "_A" ]
		node [ id 5 label "_B" ]
		node [ id 6 label "N" ]
		node [ id 7 label "H" ]
		node [ id 8 label "H" ]
		node [ id 9 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 2 label "-" ]
		edge [ source 1 target 7 label "-" ]
		edge [ source 2 target 4 label "-" ]
		edge [ source 2 target 5 label "-" ]
		edge [ source 6 target 8 label "-" ]
		edge [ source 6 target 9 label "-" ]
	]
	right [
		edge [ source 1 target 3 label "-" ]
		edge [ source 2 target 6 label "-" ]
	]
]