#!/bin/zsh

for i in `seq 0 2`; do
  qsub -N delphes_split_${i} -o /home/micheli/logs/stdout-$i.txt -e /home/micheli/logs/stderr-$i.txt \
  run${i}.job
  echo Submitted ${i}
done 
