#!/bin/bash


for i in .001 .01 .1 0.25 0.3
do
    rm -f busy$(echo $i)_c1
    rm -f busy$(echo $i)_c2
    for j in {10..1}
    do
        sudo mn -c
        sudo pkill -9 python
        sudo python main.py --cpu_frac $i --version 2
    done
done
