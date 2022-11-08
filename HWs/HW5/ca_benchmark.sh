#!/bin/bash
epochs=100
arr_len=2882880
rule=110
repeat_times=5
for ((processors=1; processors<=16; processors++))
do
    mpiexec -n $processors python3 cellular_automaton.py --epochs $epochs --size $arr_len --rule $rule --stat
    echo $processors out of 16
done
mpiexec -n 1 python3 cellular_automaton.py --epochs 10 --size 100 --rule 110 --stat --verbose