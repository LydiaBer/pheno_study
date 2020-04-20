#!/bin/bash
#
VARLIST1=(
  "20.0"
  "10.0"
  "7.0"
  "5.0"
)
VARLIST2=(
  "3.0"
  "2.0"
  "1.0"
  "0.5"
)
VARLIST3=(
  "m0.5"
  "m1.0"
  "m2.0"
  "m5.0"
)
VARLIST4=(
  "m7.0"
  "m10.0"
  "m20.0"
)
for var in "${VARLIST1[@]}"; do
  ##  RS_G signal
  echo 'processing '${var}
  python train_lambdai_vs_bkg.py --var ${var} 2>&1 | tee logs/train_masspoint_${var}.log& 
done
wait
for var in "${VARLIST2[@]}"; do
  ##  RS_G signal
  echo 'processing '${var}
  python train_lambdai_vs_bkg.py --var ${var} 2>&1 | tee logs/train_masspoint_${var}.log& 
done
wait
for var in "${VARLIST3[@]}"; do
  ##  RS_G signal
  echo 'processing '${var}
  python train_lambdai_vs_bkg.py --var ${var} 2>&1 | tee logs/train_masspoint_${var}.log& 
done
wait
for var in "${VARLIST4[@]}"; do
  ##  RS_G signal
  echo 'processing '${var}
  python train_lambdai_vs_bkg.py --var ${var} 2>&1 | tee logs/train_masspoint_${var}.log& 
done
