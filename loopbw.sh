#!/bin/bash

#rm c1_bw$1
#rm c2_bw$1
#
#for i in .001 .01 .1 1 10
#do
#    echo $i
#    for j in {10..1}
#    do
#        sudo mn -c
#        sudo pkill -9 python
#        sudo python main.py --bw $i
#    done
#done

for i in 0.001 0.01 0.1 1 10.0
do
    python analyze_results.py -f "c1_bw$i"
    python analyze_results.py -f "c2_bw$i"
done
