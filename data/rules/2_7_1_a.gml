rule [
	ruleID "2.7.1.a R02705"
	labelType "term"
	left [
		edge [ source 0 target 1 label "-" ]
		edge [ source 6 target 10 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "O" ]
		node [ id 2 label "H" ]
		node [ id 3 label "P" ]
		node [ id 4 label "O" ]
		node [ id 5 label "O" ]
		node [ id 6 label "O" ]
		node [ id 7 label "O" ]
		node [ id 8 label "H" ]
		node [ id 9 label "H" ]
		node [ id 10 label "ADP" ]
		edge [ source 1 target 2 label "-" ]
		edge [ source 3 target 4 label "=" ]
		edge [ source 3 target 5 label "-" ]
		edge [ source 3 target 6 label "-" ]
		edge [ source 3 target 7 label "-" ]
		edge [ source 5 target 9 label "-" ]
		edge [ source 7 target 8 label "-" ]
	]
	right [
		edge [ source 0 target 6 label "-" ]
		edge [ source 1 target 10 label "-" ]
	]
]