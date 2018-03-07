#!/usr/bin/python

import common
import sys

from collections import OrderedDict

file = open(sys.argv[1])
grammar = file.read()
file.close()

rules = grammar.splitlines()
dict = OrderedDict() # dictionary of production rules, key is non terminal on left side of rule, value is right side of rule in form of a list
epsilon = 'epsilon'
# list if possible nterminal names
nterminals = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
			  'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# add each rule to dictionary
for i in range(len(rules)):
		# put each rule into list
		line = rules[i].split(' ')

		# key for rule will be non-terminal on left side, first char in line
		key = line[0]
		rhs = '' # store full right hand side of rule in this variable

		if len(line)==1:
			continue
		# add it to dictionary if unique, value is empty list
		if not key in dict:
			dict[key] = []
		
		productions = []
		for i in range(len(line)):
			if i > 1:
				productions.append(line[i])
		# fill values list with rhs of rule
		for j in range(len(productions)):
			if productions[j]==epsilon:
				dict.get(key).append(epsilon)
				continue
			# account for or production symbol
			if productions[j]=='|':
				if rhs:
					dict.get(key).append(rhs)
				rhs = ''
				continue
			if len(rhs) > 0:
				c = ' '+productions[j] # separate rhs by spaces
			else:
				c = productions[j]
			rhs+=c
		if len(rhs)>0:
			dict.get(key).append(rhs)

# function used to take an ebnf grammar and output a bnf grammar
def process_ebnf():
	for key in dict:
		rules = dict.get(key)
		for rule in rules:
			if rule == epsilon:
				continue
			symbols = rule.split(' ')
			inner_index = 0 # index for innermost bracket
			value = iterate_rule(symbols,rule,rules,inner_index)
			# if return value isn't none then stop loop to change dictionary or throw error
			if value != None:
				return value

# iterates over the rule
def iterate_rule(symbols,rule,rules,inner_index):
	inner_index = 0 # used to store the index of the innermost bracket
	for index in range(len(symbols)):
		symbol = symbols[index]
		original = '' # used to store the original rule before modification
		if symbol=='{' or symbol=='[':
			inner_index = index
		if symbol=='}' or symbol==']':
			if symbol=='}' and symbols[inner_index]!='{':
				return False
			if symbol==']' and symbols[inner_index]!='[':
				return False
			inner = get_inner(symbols,index,inner_index)
			for k in range(len(rules)):
				if rules[k]==rule:
					original = rule
					temp = rule.split(' ')
					temp2 = []
					for l in range(len(temp)):
						# creating rule to overwrite old one with brackets
						if l < inner_index or l > index:
							temp2.append(temp[l])
						if l==index:
							if symbol=='}':
								value = inner_create(k,inner,2)
							else:
								value = inner_create(k,inner,1)
							if value[0] == 'err':
								return 'err'
							# append key for new rule into position where brackets were
							temp2.append(value[0])
			return temp2,value,original
	if inner_index != 0:
		return False
	
# returns symbols in between given indices
def get_inner(symbols,index,inner_index):
	inner = []
	j = inner_index+1
	while j < index:
		inner.append(symbols[j])
		j+=1
	return inner

# create new rule for terms within brackets
def inner_create(index,inner,type):
	key = ''
	for nterminal in list(reversed(nterminals)):
		if nterminal not in dict.keys():
			key = nterminal
	if key == '': # no available key from nterminals list
		return 'err'
	# for []
	if type == 1:
		value = [inner,'epsilon']
	# for {}
	elif type == 2:
		temp = key
		for symbol in inner:
			temp = temp + ' ' + symbol
		value = [temp,'epsilon']
	return key,value

flag = '' # stores if done processing or quit when error
while flag != 'done' and flag != 'quit':
	value = process_ebnf()
	if value == None:
		flag = 'done'
	elif value == 'err':
		print('Run out of possible keys')
		flag = 'quit'
	elif value == False:
		print('Error in syntax')
		flag = 'quit'
	# else value has values of new changes to be made to dictionary
	else:
		for key in dict.keys():
			for index in range(len(dict.get(key))):
				# if original rule
				if value[2]==dict.get(key)[index]:
					j = 0
					str = ''
					for temp in value[0]:
						if j != 0:
							str = str + ' ' + temp
						else:
							str = str + temp
						j += 1
					# overwrite with new rule
					dict.get(key)[index] = str
		dict[value[1][0]] = []
		# add new rules to dictionary
		for rule in value[1][1]:
			if rule == epsilon:
				dict.get(value[1][0]).append(epsilon)
			else:
				temp = ''
				for element in rule:
					temp = temp + element
				dict.get(value[1][0]).append(temp)
		# return to loop through all rules to check for more brackets
		process_ebnf()
		
if flag != 'quit':
	for key in dict.keys():
		for i in range(len(dict.get(key))):
			print('{} ::= {}'.format(key,dict.get(key)[i]))
				
