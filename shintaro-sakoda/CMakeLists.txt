cmake_minimum_required(VERSION 3.10)
project(Practice)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "-march=native")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

file(GLOB SRCS base_converter.cc converter_A.cc converter_B.cc main.cc)

add_executable(a.out ${SRCS})
