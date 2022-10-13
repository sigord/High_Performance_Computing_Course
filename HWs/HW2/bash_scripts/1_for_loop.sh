#!/bin/bash
startdefault=100
enddefault=1000
stepdefault=2
start=${1:-$startdefault}
end=${2:-$enddefault}
step=${3:-$stepdefault}

# echo "Runnig loop from $start to $end with $step step"
# echo "USE ATTR 1 is start 2 is end 3 is step"

for (( i=start; i<=end; i+=step))
do
   echo $i
done
