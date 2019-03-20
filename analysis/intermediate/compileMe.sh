echo "Sourcing the setup.sh script"
source ../../setup.sh

echo "Soft-linking customised Delphes classes"
ln -s ../../delphes/classes

echo "Building package"
rm -rf build; mkdir build; cd build
cmake ..; make
cd ..
