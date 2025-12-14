rule [
	ruleID "3.5.4.a R04374"
	labelType "term"
	left [
		edge [ source 0 target 1 label "=" ]
		edge [ source 1 target 5 label "-" ]
		edge [ source 5 target 6 label "-" ]
	]
	context [
		node [ id 0 label "C" ]
		node [ id 1 label "C" ]
		node [ id 2 label "_A" ]
		node [ id 3 label "_B" ]
		node [ id 4 label "_C" ]
		node [ id 5 label "N" ]
		node [ id 6 label "H" ]
		node [ id 7 label "_D" ]
		edge [ source 0 target 2 label "-" ]
		edge [ source 0 target 3 label "-" ]
		edge [ source 1 target 4 label "-" ]
		edge [ source 5 target 7 label "-" ]
	]
	right [
		edge [ source 0 target 1 label "-" ]
		edge [ source 0 target 6 label "-" ]
		edge [ source 1 target 5 label "=" ]
	]
]