# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.11

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /cvmfs/sft.cern.ch/lcg/releases/CMake/3.11.1-daf3a/x86_64-slc6-gcc7-opt/bin/cmake

# The command to remove a file.
RM = /cvmfs/sft.cern.ch/lcg/releases/CMake/3.11.1-daf3a/x86_64-slc6-gcc7-opt/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build

# Include any dependencies generated for this target.
include test/CMakeFiles/gmock.dir/depend.make

# Include the progress variables for this target.
include test/CMakeFiles/gmock.dir/progress.make

# Include the compile flags for this target's objects.
include test/CMakeFiles/gmock.dir/flags.make

test/CMakeFiles/gmock.dir/gmock-gtest-all.cc.o: test/CMakeFiles/gmock.dir/flags.make
test/CMakeFiles/gmock.dir/gmock-gtest-all.cc.o: ../test/gmock-gtest-all.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object test/CMakeFiles/gmock.dir/gmock-gtest-all.cc.o"
	cd /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build/test && /cvmfs/sft-nightlies.cern.ch/lcg/contrib/gcc/7binutils/x86_64-slc6/bin/g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/gmock.dir/gmock-gtest-all.cc.o -c /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/test/gmock-gtest-all.cc

test/CMakeFiles/gmock.dir/gmock-gtest-all.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/gmock.dir/gmock-gtest-all.cc.i"
	cd /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build/test && /cvmfs/sft-nightlies.cern.ch/lcg/contrib/gcc/7binutils/x86_64-slc6/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/test/gmock-gtest-all.cc > CMakeFiles/gmock.dir/gmock-gtest-all.cc.i

test/CMakeFiles/gmock.dir/gmock-gtest-all.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/gmock.dir/gmock-gtest-all.cc.s"
	cd /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build/test && /cvmfs/sft-nightlies.cern.ch/lcg/contrib/gcc/7binutils/x86_64-slc6/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/test/gmock-gtest-all.cc -o CMakeFiles/gmock.dir/gmock-gtest-all.cc.s

# Object files for target gmock
gmock_OBJECTS = \
"CMakeFiles/gmock.dir/gmock-gtest-all.cc.o"

# External object files for target gmock
gmock_EXTERNAL_OBJECTS =

test/libgmock.a: test/CMakeFiles/gmock.dir/gmock-gtest-all.cc.o
test/libgmock.a: test/CMakeFiles/gmock.dir/build.make
test/libgmock.a: test/CMakeFiles/gmock.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libgmock.a"
	cd /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build/test && $(CMAKE_COMMAND) -P CMakeFiles/gmock.dir/cmake_clean_target.cmake
	cd /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/gmock.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/CMakeFiles/gmock.dir/build: test/libgmock.a

.PHONY : test/CMakeFiles/gmock.dir/build

test/CMakeFiles/gmock.dir/clean:
	cd /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build/test && $(CMAKE_COMMAND) -P CMakeFiles/gmock.dir/cmake_clean.cmake
.PHONY : test/CMakeFiles/gmock.dir/clean

test/CMakeFiles/gmock.dir/depend:
	cd /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0 /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/test /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build/test /data/atlas/atlasdata/micheli/validation/histos/histo_all/fmt-5.1.0/build/test/CMakeFiles/gmock.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/CMakeFiles/gmock.dir/depend

