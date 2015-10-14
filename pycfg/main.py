#!/usr/bin/env python
from Grammar import Grammar
from Grammar import Parser
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
rules = form['rules'].value.split('\r\n')
cmd = form['cmd'].value

g = Grammar()
p = Parser(g)
p.parse_rules(rules)

if cmd == 'generate':
	print(g.derive('S'))
elif cmd == 'cnf':
	print(g.to_cnf())
