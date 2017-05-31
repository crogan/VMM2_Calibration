#!/bin/bash
DATE1=7April
DATE2=28May
FILE=LostMay.txt
boards=( 102 105 106 107 116 117 118 119 )

for i in "${boards[@]}"
do
    echo $i
    python lost_channels.py -o Board${i}_${DATE1}.root -n Board${i}_${DATE2}.root >> $FILE

done
    
