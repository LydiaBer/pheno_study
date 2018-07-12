#script to launch resolved,intermediate & boosted analysis together.


#resolved analysis
cd resolved
rm -rf build; mkdir build; cd build;
cmake ..; make
./resolved-recon

echo 'Resolved Completed'

#moving to pheno_study folder

cd ..
cd ..

#intermediate analysis
cd intermediate
rm -rf build; mkdir build; cd build;
cmake ..; make
./intermediate-recon

echo "Intermediate Completed"

#moving to pheno_study folder

cd ..
cd ..

#boosted analysis

cd boosted
rm -rf build; mkdir build; cd build;
cmake ..; make
./boosted-recon

echo "Boosted Completed"

#moving to pheno_study folder

cd ..
cd ..

#storing data in a single folder

mkdir output 
cp /resolved/build/pheno_resolved.root output/
cp /intermediate/build/pheno_intermediate.root output/
cp /boosted/build/pheno_boosted.root output/

echo "Output Completed"
echo 'Full Analysis Completed'

