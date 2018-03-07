#!/usr/bin/python

import common
import sys

value = common.load_grammar(sys.argv[1])
if value != 'err':
	dict = value[2]
	T = value[3]
	first = value[4]
	follow = value[5]
	M = {}
	V = dict.keys()
	S = value[6]
	# determine the first of the rhs of a production rule
	def first_rhs(rhs):
		result = []
		for symbol in rhs:
			for first_symbol in first.get(symbol):
				if first_symbol != 'epsilon':
					result.append(first_symbol)
			if 'epsilon' not in first.get(symbol):
				break
		return result

	def create_table():
		index = 0
		for key in dict:
			for productions in dict.get(key):
				symbols = productions.split(' ')
				result = []
				if symbols[0]!='epsilon':
					# for all terminals in first of first symbol, add rule to table
					result = first_rhs(symbols)
					for firsts in result:
						if firsts in T:
							if (key,firsts) in M.keys():
								return False
							M[key,firsts] = index
				if 'epsilon' in result or symbols[0]=='epsilon':
					#for all terminals in follow of first symbol, add rule to table
					for follows in follow.get(key):
						if follows in T:
							if (key,follows) in M.keys():
								return False
							M[key,follows] = index
					if '$' in follow.get(key):
						if (key,follows) in M.keys():
							return False
						M[key,'$'] = index
				index+=1
		return True
	
	valid = create_table()
	
	def is_valid():
		if valid:
			return True
		else:
			return False
	if __name__ == "__main__":
		if valid:
			for key in M:
				print('R[{}, {}] = {}'.format(key[0],key[1],M.get(key)))
		else:
			print('Grammar is not LL(1)!')
