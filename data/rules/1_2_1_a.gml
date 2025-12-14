rule [
	ruleID "1.2.1.a R04445"
	labelType "term"
	left [
		node [ id 3 label "H" ]
		node [ id 7 label "NAD+" ]
		edge [ source 1 target 3 label "-" ]
		edge [ source 4 target 6 label "-" ]
	]
	context [
		node [ id 0 label "O" ]
		node [ id 1 label "C" ]
		node [ id 2 label "_A" ]
		node [ id 4 label "O" ]
		node [ id 5 label "H" ]
		node [ id 6 label "H" ]
		edge [ source 0 target 1 label "=" ]
		edge [ source 1 target 2 label "-" ]
		edge [ source 4 target 5 label "-" ]
	]
	right [
		node [ id 3 label "H+" ]
		node [ id 7 label "NAD" ]
		edge [ source 1 target 4 label "-" ]
		edge [ source 6 target 7 label "-" ]
	]
	constrainLabelAny [
		label "_A"
		labels [ label "C" label "H" ]
	]
]