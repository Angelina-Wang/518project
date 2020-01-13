#!/bin/bash

for i in {1..10}
do
    rm -f c1_d$i
    rm -f c2_d$i
    for j in {10..1}
    do
	sudo mn -c
	sudo pkill -9 python
	sudo python main.py --delay $(echo $i)
    done
done
