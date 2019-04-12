# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Default target executed when no arguments are given to make.
default_target: all

.PHONY : default_target

# Allow only one "make -f Makefile2" at a time, but pass parallelism.
.NOTPARALLEL:


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
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/dd/Desktop/cs620/CS620-final-project

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/dd/Desktop/cs620/CS620-final-project

#=============================================================================
# Targets provided globally by CMake.

# Special rule for the target rebuild_cache
rebuild_cache:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Running CMake to regenerate build system..."
	/usr/bin/cmake -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR)
.PHONY : rebuild_cache

# Special rule for the target rebuild_cache
rebuild_cache/fast: rebuild_cache

.PHONY : rebuild_cache/fast

# Special rule for the target edit_cache
edit_cache:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "No interactive CMake dialog available..."
	/usr/bin/cmake -E echo No\ interactive\ CMake\ dialog\ available.
.PHONY : edit_cache

# Special rule for the target edit_cache
edit_cache/fast: edit_cache

.PHONY : edit_cache/fast

# The main all target
all: cmake_check_build_system
	$(CMAKE_COMMAND) -E cmake_progress_start /home/dd/Desktop/cs620/CS620-final-project/CMakeFiles /home/dd/Desktop/cs620/CS620-final-project/CMakeFiles/progress.marks
	$(MAKE) -f CMakeFiles/Makefile2 all
	$(CMAKE_COMMAND) -E cmake_progress_start /home/dd/Desktop/cs620/CS620-final-project/CMakeFiles 0
.PHONY : all

# The main clean target
clean:
	$(MAKE) -f CMakeFiles/Makefile2 clean
.PHONY : clean

# The main clean target
clean/fast: clean

.PHONY : clean/fast

# Prepare targets for installation.
preinstall: all
	$(MAKE) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall

# Prepare targets for installation.
preinstall/fast:
	$(MAKE) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall/fast

# clear depends
depend:
	$(CMAKE_COMMAND) -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 1
.PHONY : depend

#=============================================================================
# Target rules for targets named Algorand

# Build rule for target.
Algorand: cmake_check_build_system
	$(MAKE) -f CMakeFiles/Makefile2 Algorand
.PHONY : Algorand

# fast build rule for target.
Algorand/fast:
	$(MAKE) -f CMakeFiles/Algorand.dir/build.make CMakeFiles/Algorand.dir/build
.PHONY : Algorand/fast

src/event.o: src/event.cpp.o

.PHONY : src/event.o

# target to build an object file
src/event.cpp.o:
	$(MAKE) -f CMakeFiles/Algorand.dir/build.make CMakeFiles/Algorand.dir/src/event.cpp.o
.PHONY : src/event.cpp.o

src/event.i: src/event.cpp.i

.PHONY : src/event.i

# target to preprocess a source file
src/event.cpp.i:
	$(MAKE) -f CMakeFiles/Algorand.dir/build.make CMakeFiles/Algorand.dir/src/event.cpp.i
.PHONY : src/event.cpp.i

src/event.s: src/event.cpp.s

.PHONY : src/event.s

# target to generate assembly for a file
src/event.cpp.s:
	$(MAKE) -f CMakeFiles/Algorand.dir/build.make CMakeFiles/Algorand.dir/src/event.cpp.s
.PHONY : src/event.cpp.s

src/main.o: src/main.cpp.o

.PHONY : src/main.o

# target to build an object file
src/main.cpp.o:
	$(MAKE) -f CMakeFiles/Algorand.dir/build.make CMakeFiles/Algorand.dir/src/main.cpp.o
.PHONY : src/main.cpp.o

src/main.i: src/main.cpp.i

.PHONY : src/main.i

# target to preprocess a source file
src/main.cpp.i:
	$(MAKE) -f CMakeFiles/Algorand.dir/build.make CMakeFiles/Algorand.dir/src/main.cpp.i
.PHONY : src/main.cpp.i

src/main.s: src/main.cpp.s

.PHONY : src/main.s

# target to generate assembly for a file
src/main.cpp.s:
	$(MAKE) -f CMakeFiles/Algorand.dir/build.make CMakeFiles/Algorand.dir/src/main.cpp.s
.PHONY : src/main.cpp.s

src/node.o: src/node.cpp.o

.PHONY : src/node.o

# target to build an object file
src/node.cpp.o:
	$(MAKE) -f CMakeFiles/Algorand.dir/build.make CMakeFiles/Algorand.dir/src/node.cpp.o
.PHONY : src/node.cpp.o

src/node.i: src/node.cpp.i

.PHONY : src/node.i

# target to preprocess a source file
src/node.cpp.i:
	$(MAKE) -f CMakeFiles/Algorand.dir/build.make CMakeFiles/Algorand.dir/src/node.cpp.i
.PHONY : src/node.cpp.i

src/node.s: src/node.cpp.s

.PHONY : src/node.s

# target to generate assembly for a file
src/node.cpp.s:
	$(MAKE) -f CMakeFiles/Algorand.dir/build.make CMakeFiles/Algorand.dir/src/node.cpp.s
.PHONY : src/node.cpp.s

# Help Target
help:
	@echo "The following are some of the valid targets for this Makefile:"
	@echo "... all (the default if no target is provided)"
	@echo "... clean"
	@echo "... depend"
	@echo "... rebuild_cache"
	@echo "... Algorand"
	@echo "... edit_cache"
	@echo "... src/event.o"
	@echo "... src/event.i"
	@echo "... src/event.s"
	@echo "... src/main.o"
	@echo "... src/main.i"
	@echo "... src/main.s"
	@echo "... src/node.o"
	@echo "... src/node.i"
	@echo "... src/node.s"
.PHONY : help



#=============================================================================
# Special targets to cleanup operation of make.

# Special rule to run CMake to check the build system integrity.
# No rule that depends on this can have commands that come from listfiles
# because they might be regenerated.
cmake_check_build_system:
	$(CMAKE_COMMAND) -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 0
.PHONY : cmake_check_build_system
