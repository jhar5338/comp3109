#!/bin/bash 

rm -rf resultsq4.out
for file in *.grammar
do
	echo +++++$file+++++ | tee --append resultsq4.out
	./../question4.py "$file" >> resultsq4.out
done
cat resultsq4.out
