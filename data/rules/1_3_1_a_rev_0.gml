rule [
	ruleID "1.3.1.a_rev R01462"
	labelType "term"
	left [
		node [ id 4 label "H+" ]
		node [ id 10 label "NAD" ]
		edge [ source 3 target 6 label "=" ]
		edge [ source 8 target 10 label "-" ]
	]
	context [
		node [ id 0 label "_A_0" ]
		node [ id 1 label "C" ]
		node [ id 2 label "_X_0" ]
		node [ id 3 label "C" ]
		node [ id 5 label "_B_0" ]
		node [ id 6 label "C" ]
		node [ id 7 label "_C_0" ]
		node [ id 8 label "H" ]
		node [ id 9 label "_D_0" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 2 label "=" ]
		edge [ source 1 target 3 label "-" ]
		edge [ source 3 target 5 label "-" ]
		edge [ source 6 target 7 label "-" ]
		edge [ source 6 target 9 label "-" ]
	]
	right [
		node [ id 4 label "H" ]
		node [ id 10 label "NAD+" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 3 target 6 label "-" ]
		edge [ source 6 target 8 label "-" ]
	]
	constrainLabelAny [
		label "_X_0"
		labels [ label "O" ]
	]
]