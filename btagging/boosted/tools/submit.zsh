#!/bin/zsh
data=$1
f=$2
i=0
find -O2 $ADATA/Exotics/HH4b/Ntuples/${data} -type f -name '*.root' -exec du -m {} \; \
    | sort -n -r -k 1,1 \
    | awk -f fix.awk \
    | while read -r files
do
    qsub -N HH4b-res-recon-${i} -o logs/stdout-$i.txt -e logs/stderr-$i.txt \
         -v data=${data},f=${f},inum=${i},files=${files} run.job
    echo Submitted $((i++))
done
