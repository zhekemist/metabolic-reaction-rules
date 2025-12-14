{Template}

rule [
	ruleID "4.2.1.e R02376"
	labelType "term"
	left [
		edge [ source 2 target 8 label "-" ]
		edge [ source 4 target 5 label "-" ]
		edge [ source 4 target 7 label "-" ]
		edge [ source 7 target 11 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "C" ]
		node [ id 3 label "H" ]
		node [ id 4 label "C" ]
		node [ id 5 label "H" ]
		node [ id 6 label "_B" ]
		node [ id 7 label "O" ]
		node [ id 8 label "O" ]
		node [ id 9 label "H" ]
		node [ id 10 label "H" ]
		node [ id 11 label "H" ]
		node [ id 12 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 2 label "-" ]
		edge [ source 1 target 9 label "-" ]
		edge [ source 1 target 10 label "-" ]
		edge [ source 2 target 3 label "-" ]
		edge [ source 2 target 4 label "-" ]
		edge [ source 4 target 6 label "-" ]
		edge [ source 8 target 12 label "-" ]
	]
	right [
		edge [ source 2 target 5 label "-" ]
		edge [ source 4 target 7 label "=" ]
		edge [ source 8 target 11 label "-" ]
	]
	constrainLabelAny [
		label "_A"
		labels [ label "H" label "{OH}" ]
	]
	constrainLabelAny [
		label "_B"
		labels [ label "H" label "{Me}" ]
	]
]

