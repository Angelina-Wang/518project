#!/bin/bash

#rm multiple*

#for i in 10
#do
#    for j in {10..1}
#    do
#        sudo mn -c
#        sudo pkill -9 python
#        sleep 1
#        sudo python main.py --version 1 --num_clients $i
#        sleep 1
#    done
#done

for i in 2 4 6 8 10
do
    python analyze_results.py -f multiple_$i
done
