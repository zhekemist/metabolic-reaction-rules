rule [
	ruleID "4.3.1.d R00221"
	labelType "term"
	left [
		edge [ source 1 target 2 label "-" ]
		edge [ source 1 target 3 label "-" ]
		edge [ source 4 target 7 label "-" ]
		edge [ source 7 target 10 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "H" ]
		node [ id 3 label "N" ]
		node [ id 4 label "C" ]
		node [ id 5 label "_B" ]
		node [ id 6 label "H" ]
		node [ id 7 label "O" ]
		node [ id 8 label "H" ]
		node [ id 9 label "H" ]
		node [ id 10 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 4 label "-" ]
		edge [ source 3 target 8 label "-" ]
		edge [ source 3 target 9 label "-" ]
		edge [ source 4 target 5 label "-" ]
		edge [ source 4 target 6 label "-" ]
	]
	right [
		edge [ source 1 target 7 label "=" ]
		edge [ source 2 target 3 label "-" ]
		edge [ source 4 target 10 label "-" ]
	]
	constrainLabelAny [
		label "_A"
		labels [ label "C" label "H" ]
	]
]