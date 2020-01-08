#!/bin/bash

rm multiple*

for i in 2 4 6 8 10
do
    for j in {10..1}
    do
        sudo mn -c
        sudo pkill -9 python
        sudo python main.py --version 1 --num_clients $i
    done
done

for i in 2 4 6 8 10
do
    python analyze_results.py -f multiple$i
done
