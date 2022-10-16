#!/bin/bash
FLAGS=("-g" "-O3")
N_ARR=(500 512 1000 1024 2000 2048)

for flag in ${FLAGS[@]}
do
    echo "Flag: $flag"
    make -s OPTIMIZER=$flag
    for N in ${N_ARR[@]}
    do
        make -s run N=$N
    done
done