rule [
	ruleID "4.1.2.c R00478"
	labelType "term"
	left [
		edge [ source 0 target 3 label "-" ]
		edge [ source 0 target 7 label "-" ]
		edge [ source 7 target 10 label "-" ]
	]
	context [
		node [ id 0 label "C" ]
		node [ id 1 label "_A" ]
		node [ id 2 label "_C" ]
		node [ id 3 label "C" ]
		node [ id 4 label "N" ]
		node [ id 5 label "_D" ]
		node [ id 6 label "_E" ]
		node [ id 7 label "O" ]
		node [ id 8 label "H" ]
		node [ id 9 label "H" ]
		node [ id 10 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 0 target 2 label "-" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 3 target 5 label "-" ]
		edge [ source 3 target 6 label "-" ]
		edge [ source 4 target 8 label "-" ]
		edge [ source 4 target 9 label "-" ]
	]
	right [
		edge [ source 0 target 7 label "=" ]
		edge [ source 3 target 10 label "-" ]
	]
]