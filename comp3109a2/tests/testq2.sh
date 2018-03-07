#!/bin/bash 

rm -rf resultsq2.out
for file in *.grammar
do
	echo +++++$file+++++ | tee --append resultsq2.out
	./../question2.py "$file" >> resultsq2.out
done
cat resultsq2.out
