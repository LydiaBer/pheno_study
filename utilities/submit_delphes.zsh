#!/bin/zsh

for i in `seq 0 3`; do
  qsub -N delphes_split_${i} -o /home/micheli/logs/stdout-$i.txt -e /home/micheli/logs/stderr-$i.txt \
  run_sherpa${i}.job
  echo Submitted ${i}
done 
