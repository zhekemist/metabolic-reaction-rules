rule [
	ruleID "3.13.1.a R05420"
	labelType "term"
	left [
		edge [ source 0 target 2 label "-" ]
		edge [ source 5 target 7 label "=" ]
		edge [ source 5 target 8 label "-" ]
	]
	context [
		node [ id 0 label "O" ]
		node [ id 1 label "H" ]
		node [ id 2 label "H" ]
		node [ id 3 label "_A" ]
		node [ id 4 label "O" ]
		node [ id 5 label "S" ]
		node [ id 6 label "O" ]
		node [ id 7 label "O" ]
		node [ id 8 label "_B" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 4 target 5 label "-" ]
		edge [ source 5 target 6 label "=" ]
	]
	right [
		edge [ source 0 target 8 label "-" ]
		edge [ source 2 target 7 label "-" ]
		edge [ source 5 target 7 label "-" ]
	]
	constrainLabelAny [
		label "_B"
		labels [ label "C" ]
	]
]