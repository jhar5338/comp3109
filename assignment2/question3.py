#!/usr/bin/python

import common
import sys
import question2

value = common.load_grammar(sys.argv[1])

def parse_line(line,V,table,productions):
	index = 1
	S = ['$',question2.S] # stack storing start symbol and $
	line_index = 0
	# if line isn't empty then consider first symbol
	if line:
		input_s = line[0]
	else:
		return 'reject'
	n = 0
	while S[index]!= '$':
		if S[index] in V:
			temp = (S[index],input_s)
			# check if nterminal,terminal is in table
			if (temp) in table.keys():
				S.pop()
				index-=1
				rhs = productions[table.get(temp)].split(' ')
				if rhs[0] == 'epsilon':
					continue
				for symbol in reversed(rhs):
					S.append(symbol)
					index+=1
			else:
				return 'reject'
		else:
			if S[index] == input_s:
				if S[index] != '$':
					S.pop()
					index-=1
					line_index+=1
					# take next terminal from input stream if available
					if line_index < len(line):
						input_s = line[line_index]
					else:
						input_s = '$'
				else:
					return 'reject'
			else:
				return 'reject'
		n+=1
	if input_s != '$':
		return 'reject'
	else:
		return 'accept'

def parser():
	table = question2.M # parse table
	V = question2.V # non-terminals
	T = question2.T # terminals
	dict = value[2]
	productions = []
	for keys in dict:
		productions.extend(dict.get(keys))
	lines = input.splitlines()
	# iterate through each line from input file
	for line in lines:
		print(parse_line(line,V,table,productions))


if value != 'err':
	if question2.valid == False:
		print('Grammar is not LL(1)!')
	else:
		file = open(sys.argv[2])
		input = file.read()
		file.close()
		parser()

