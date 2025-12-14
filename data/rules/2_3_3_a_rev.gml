rule [
	ruleID "2.3.3.a_rev R00351"
	labelType "term"
	left [
		edge [ source 1 target 2 label "-" ]
		edge [ source 1 target 4 label "-" ]
		edge [ source 2 target 10 label "-" ]
		edge [ source 5 target 11 label "-" ]
		edge [ source 7 target 12 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "O" ]
		node [ id 3 label "_B" ]
		node [ id 4 label "C" ]
		node [ id 5 label "C" ]
		node [ id 6 label "O" ]
		node [ id 7 label "S" ]
		node [ id 8 label "H" ]
		node [ id 9 label "H" ]
		node [ id 10 label "H" ]
		node [ id 11 label "O" ]
		node [ id 12 label "H" ]
		node [ id 13 label "H" ]
		node [ id 14 label "CoA" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 3 label "-" ]
		edge [ source 4 target 5 label "-" ]
		edge [ source 4 target 8 label "-" ]
		edge [ source 4 target 9 label "-" ]
		edge [ source 5 target 6 label "=" ]
		edge [ source 7 target 14 label "-" ]
		edge [ source 11 target 13 label "-" ]
	]
	right [
		edge [ source 1 target 2 label "=" ]
		edge [ source 4 target 10 label "-" ]
		edge [ source 5 target 7 label "-" ]
		edge [ source 11 target 12 label "-" ]
	]
	constrainLabelAny [
		label "_A"
		labels [ label "C" label "H" ]
	]
	constrainLabelAny [
		label "_B"
		labels [ label "C" label "H" ]
	]
]