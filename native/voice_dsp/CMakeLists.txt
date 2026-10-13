cmake_minimum_required(VERSION 3.24)
project(voice_dsp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(voice_dsp src/voice_dsp.cpp)
target_compile_options(voice_dsp PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/O2 /fp:fast>)