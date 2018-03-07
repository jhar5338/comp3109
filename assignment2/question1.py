#!/usr/bin/python

# Assumed order of output for first and follow sets does not matter

import common
import sys

value = common.load_grammar(sys.argv[1])
if value != 'err':
	print('First:')
	for key in value[0]:
		print('   {} -> {}'.format(key,' '.join(value[0].get(key))))
	print('Follow:')
	for key in value[1]:
		print('   {} -> {}'.format(key,' '.join(value[1].get(key))))
