rule [
	ruleID "3.1.3.a R05420"
	labelType "term"
	left [
		edge [ source 1 target 2 label "-" ]
		edge [ source 8 target 10 label "-" ]
	]
	context [
		node [ id 0 label "P" ]
		node [ id 1 label "O" ]
		node [ id 2 label "_A" ]
		node [ id 3 label "O" ]
		node [ id 4 label "_B" ]
		node [ id 5 label "O" ]
		node [ id 6 label "_C" ]
		node [ id 7 label "O" ]
		node [ id 8 label "O" ]
		node [ id 9 label "H" ]
		node [ id 10 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 0 target 3 label "-" ]
		edge [ source 0 target 5 label "-" ]
		edge [ source 0 target 7 label "=" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 5 target 6 label "-" ]
		edge [ source 8 target 9 label "-" ]
	]
	right [
		edge [ source 1 target 10 label "-" ]
		edge [ source 2 target 8 label "-" ]
	]
]