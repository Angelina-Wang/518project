#!/bin/bash

for i in .001 .01 .1 1 10
do
    rm -f c1_bw$i
    rm -f c2_bw$i
    for j in {10..1}
    do
        sudo mn -c
        sudo pkill -9 python
        sudo python main.py --bw $i
    done
done
