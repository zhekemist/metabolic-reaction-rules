{Template}

rule [
	ruleID "1.3.1.a R01251"
	labelType "term"
	left [
		node [ id 4 label "H" ]
		node [ id 10 label "NAD+" ]
		edge [ source 3 target 4 label "-" ]
		edge [ source 3 target 6 label "-" ]
		edge [ source 6 target 8 label "-" ]
	]
	context [
		node [ id 0 label "_A" ]
		node [ id 1 label "C" ]
		node [ id 2 label "_Z" ]
		node [ id 3 label "C" ]
		node [ id 5 label "H" ]
		node [ id 6 label "C" ]
		node [ id 7 label "{Hy}" ]
		node [ id 8 label "H" ]
		node [ id 9 label "H" ]
		edge [ source 0 target 1 label "-" ]
		edge [ source 1 target 2 label "=" ]
		edge [ source 1 target 3 label "-" ]
		edge [ source 3 target 5 label "-" ]
		edge [ source 6 target 7 label "-" ]
		edge [ source 6 target 9 label "-" ]
	]
	right [
		node [ id 4 label "H+" ]
		node [ id 10 label "NAD" ]
		edge [ source 3 target 6 label "=" ]
		edge [ source 8 target 10 label "-" ]
	]
	constrainLabelAny [
		label "_Z"
		labels [ label "{O}" label "{C}" label "{N}" ]
	]
	constrainLabelAny [
		label "_A"
		labels [ label "C" label "H" ]
	]
	constrainLabelAny [
		label "_X"
		labels [ label "C" label "H" ]
	]
	constrainLabelAny [
		label "_W"
		labels [ label "C" label "H" ]
	]
]

{Group:Hy:1}
graph [
	node [ id 1 label "O" ]
	node [ id 2 label "H" ]
	edge [ source 1 target 2 label "-" ]
]

{Group:O:1}
graph [
	node [ id 1 label "O" ]
]

{Group:C:1}

graph [
	node [ id 1 label "C" ]
	node [ id 2 label "H" ]
	node [ id 3 label "_X" ]
	edge [ source 1 target 2 label "-" ]
	edge [ source 1 target 3 label "-" ]
]

{Group:N:1}

graph [
	node [ id 1 label "N" ]
	node [ id 2 label "_W"]
	edge [ source 1 target 2 label "-" ]
]
