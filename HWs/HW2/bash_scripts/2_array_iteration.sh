#!/bin/bash
lendefault=15
len=$((${1:-$lendefault} - 1))

for i in $(seq 0 $len - 1)
do
   arr[$i]=$i
done
echo "${arr[@]}"