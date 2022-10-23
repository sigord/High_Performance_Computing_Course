#!/bin/bash
N_ARR=(10000 100000 1000000 10000000 100000000 1000000000 10000000000)

for N in ${N_ARR[@]}
do  
    ./mc_pi_estimation $N
    echo "#########################"
done