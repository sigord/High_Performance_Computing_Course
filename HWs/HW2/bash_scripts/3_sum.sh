#!/bin/bash
adefault=10
bdefault=0.5
a=${1:-$adefault}
b=${2:-$bdefault}
echo "$a + $b" | bc
