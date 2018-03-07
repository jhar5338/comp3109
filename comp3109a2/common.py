#!/usr/bin/python

'''
Justin Harding 450221916

This program is used to load a grammar from a file and store it.
It also calculates first and follow sets and stores them.
'''

from collections import OrderedDict

def load_grammar(file_name):

	file = open(file_name)
	grammar = file.read()
	file.close()

	if grammar=='\n' or grammar =='' or grammar==' ':
		print("Grammar file empty")
		return 'err'

	S = grammar[0] # start symbol
	V = [S] # finite set of non-terminals, start symbol assumed to be non-terminal
	T = [] # finite set of terminals
	dict = OrderedDict() # dictionary of production rules, key is non terminal on left side of rule, value is right side of rule in form of a list
	rules = grammar.splitlines() # each rule is a line in the grammar
	epsilon = 'epsilon'

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

		# fill values list with rhs of rule
		for i in range(len(line)):
			if line[i] == epsilon:
				dict.get(key).append(epsilon)
				break
			elif i > 1:
				if i > 2:
					c = ' '+line[i] # separate rhs by spaces
				else:
					c = line[i]
				rhs+=c
		if len(rhs)>0:
			dict.get(key).append(rhs)

		# every key must be non-terminal so add to V if unique
		if not key in V:
			V.append(key)

	# iterate through all symbols to find terminals, if not epsilon or nonterminal/key then it must be terminal
	for key in dict:
		for i in range(len(dict.get(key))):
			val = dict.get(key)[i].split()
			for symbol in val:
				if not symbol in dict and symbol not in T and symbol != epsilon:
					T.append(symbol)

	first = {} # dictionary for first set

	# function to recursively find first for non-terminals
	def find_first(nterminal):

		# if nterminal is already in first then return its first
		if nterminal in first:
			return first.get(nterminal)

		productions = dict[nterminal]
		first[nterminal] = []

		# iterate through each possible production set
		for i in range(len(productions)):
			set = productions[i]
			if set==epsilon:
				first.get(nterminal).append(epsilon)
				continue
			symbols = set.split(' ')

			index = 0
			# iterate through each symbol in this possible production set
			for symbol in symbols:
				# continue if the symbol is just repeating itself
				if symbol == nterminal:
					continue

				# find first of symbol being looked at
				find_first(symbol)
				temp = first.get(symbol)

				# append each symbol apart from epsilon to first of this nterminal
				for i in range(len(temp)):
					if temp[i]!=epsilon and temp[i] not in first.get(nterminal):
						first.get(nterminal).append(temp[i])

				# no need to go to next symbol if epsilon not in first of this one or first of this one is terminal
				if epsilon not in first.get(symbol) or first.get(symbol) in T:
					break

				index+=1

				# append epsilon if reached end of symbols without breaking
				if index == len(symbols):
					first.get(nterminal).append(epsilon)

	for terminal in T:
		first[terminal] = terminal

	for nterminal in V:
		find_first(nterminal)

	follow = {} # dictionary for follow set

	def find_follow(nterminal):
		if nterminal in follow.keys():
			return follow.get(nterminal)

		# if starting symbol put $ in first
		elif nterminal == S:
			follow[nterminal] = ['$']
		else:
			follow[nterminal] = []

		# iterate through every rule to find follow set for nterminal
		for key in dict:
			productions = dict.get(key)
			for i in range(len(productions)):
				production = productions[i]
				symbols = production.split(' ')
				for i in range(len(symbols)):
					if symbols[i] == nterminal:
						j = i
						# loop through all symbols after the nterminal in rule
						while j != len(symbols):
							if (j != len(symbols)-1):
								# if not final symbol then add the first of next symbol
								add_first(symbols[j+1],nterminal)
								# if epsilon is not in that first set then break
								if epsilon not in first.get(symbols[j+1]):
									break
							# if reached final symbol then include follow of LHS nterminal
							if j == len(symbols)-1:
								find_follow(key)
								add_follow(key,nterminal)
								break
							j+=1

	# used to add first of A to B (excludes epsilon)
	def add_first(A,B):
		for symbol in first.get(A):
			if symbol != epsilon:
				if symbol not in follow.get(B):
					follow[B].append(symbol)

	# used to add follow of A to B (excludes epsilon)
	def add_follow(A,B):
		for symbol in follow.get(A):
			if symbol != epsilon:
				if symbol not in follow.get(B):
					follow[B].append(symbol)

	for terminal in T:
		find_follow(terminal)

	for nterminal in V:
		find_follow(nterminal)

	# first set without terminals
	set = {}
	for key in first:
		if key not in T:
			set[key]=first.get(key)

	# follow set without terminals
	set2 = {}
	for key in follow:
		if key not in T:
			set2[key]=follow.get(key)
	return set,set2,dict,T,first,follow,S

