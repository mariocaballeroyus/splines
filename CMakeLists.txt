cmake_minimum_required(VERSION 3.15)
project(splines CXX)

set(CMAKE_CXX_STANDARD 14)

# Flags for g++ compiler
if(CMAKE_COMPILER_IS_GNUCXX)
    set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pedantic -Wall -Werror -fPIC -Wno-error=deprecated-declarations" )
endif(CMAKE_COMPILER_IS_GNUCXX)


# Add Eigen library
set(EIGEN3_INCLUDE_DIR ${CMAKE_SOURCE_DIR}/external/eigen)
include_directories(${EIGEN3_INCLUDE_DIR})


# Set install paths
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set (CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/install" CACHE PATH "default install path" FORCE)
endif()
SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}")


# Define splinekernel C++ library
add_library(splinekernel SHARED
    splinekernel/basis.cpp
    splinekernel/surface.cpp
    splinekernel/basis.hpp
    splinekernel/curve.hpp
    splinekernel/surface.hpp
)

# Add include dependency to splinekernel directory
target_include_directories(splinekernel PUBLIC ${CMAKE_SOURCE_DIR}/splinekernel)


# Set up Python bindings
add_subdirectory(external/pybind11)

pybind11_add_module(pysplinekernel ${CMAKE_SOURCE_DIR}/splinekernel/pysplinekernel.cpp)
target_link_libraries(pysplinekernel PRIVATE splinekernel)
target_include_directories(pysplinekernel PRIVATE ${CMAKE_SOURCE_DIR}/splinekernel)

# Set RPATH so the Python module can find libsplinekernel.so
set_target_properties(pysplinekernel PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH TRUE
)

# Install both the Python module and the C++ library it depends on
install(TARGETS pysplinekernel LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX})
install(TARGETS splinekernel LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX})


# Add main executable
add_executable(main_splines main.cpp)
target_link_libraries(main_splines PRIVATE splinekernel)