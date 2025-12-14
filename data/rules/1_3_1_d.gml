rule [
	ruleID "1.3.1.d R05398"
	labelType "term"
	left [
		node [ id 6 label "NAD" ]
		node [ id 8 label "H+" ]
		edge [ source 0 target 3 label "=" ]
		edge [ source 6 target 7 label "-" ]
	]
	context [
		node [ id 0 label "C" ]
		node [ id 1 label "_A" ]
		node [ id 2 label "_B" ]
		node [ id 3 label "C" ]
		node [ id 4 label "_C" ]
		node [ id 5 label "_D" ]
		node [ id 7 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 0 target 2 label "-" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 3 target 5 label "-" ]
	]
	right [
		node [ id 6 label "NAD+" ]
		node [ id 8 label "H" ]
		edge [ source 0 target 3 label "-" ]
		edge [ source 0 target 8 label "-" ]
		edge [ source 3 target 7 label "-" ]
	]
	constrainLabelAny [
		label "_A"
		labels [ label "C" ]
	]
	constrainLabelAny [
		label "_B"
		labels [ label "C" ]
	]
]