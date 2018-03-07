#!/bin/bash 

rm -rf resultsq1.out
for file in *.grammar
do
	echo +++++$file+++++ | tee --append resultsq1.out
	./../question1.py "$file" >> resultsq1.out
done
cat resultsq1.out
