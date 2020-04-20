#!/bin/bash
#
source ~/.bashrc
VARLIST=(
  "20.0"
  "10.0"
  "7.0"
  "5.0"
  "3.0"
  "2.0"
  "1.0"
  "0.5"
  "m0.5"
  "m1.0"
  "m2.0"
  "m5.0"
  "m7.0"
  "m10.0"
  "m20.0"
)
cd /home/paredes/pheno/testnn/pheno_study/analysis/neuralnet/train_lambdai_vs_bkg
for var in "${VARLIST[@]}"; do
  ##  RS_G signal
  echo 'processing '${var}
  python train_lambdai_vs_bkg.py --var ${var} 2>&1 | tee logs/train_masspoint_${var}.log 
done
