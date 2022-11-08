#!/bin/bash
h=$1
w=$2
for ((i=0; i<=255; i++))
do
   mpiexec -n 4 python3 cellular_automaton.py --epochs $h --size $w  --rule $i --verbose
done