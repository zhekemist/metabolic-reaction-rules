{Template}

rule [
	ruleID "1.1.1.d R05071"
	labelType "term"
	left [
		node [ id 11 label "NAD" ]
		edge [ source 1 target 8 label "=" ]
		edge [ source 1 target 13 label "-" ]
		edge [ source 2 target 4 label "-" ]
		edge [ source 11 target 12 label "-" ]
	]
	context [
		node [ id 0 label "C" ]
		node [ id 1 label "C" ]
		node [ id 2 label "C" ]
		node [ id 3 label "O" ]
		node [ id 4 label "_B" ]
		node [ id 5 label "C" ]
		node [ id 6 label "O" ]
		node [ id 7 label "O" ]
		node [ id 8 label "O" ]
		node [ id 9 label "H" ]
		node [ id 10 label "H" ]
		node [ id 12 label "H" ]
		node [ id 13 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 2 label "-" ]
		edge [ source 2 target 3 label "-" ]
		edge [ source 2 target 5 label "-" ]
		edge [ source 3 target 9 label "-" ]
		edge [ source 5 target 6 label "-" ]
		edge [ source 5 target 7 label "=" ]
		edge [ source 6 target 10 label "-" ]
	]
	right [
		node [ id 11 label "NAD+" ]
		edge [ source 1 target 4 label "-" ]
		edge [ source 1 target 8 label "-" ]
		edge [ source 2 target 13 label "-" ]
		edge [ source 8 target 12 label "-" ]
	]
	constrainLabelAny [
		label "_B"
		labels [ label "{Me}" label "{Et}" ]
	]
]

