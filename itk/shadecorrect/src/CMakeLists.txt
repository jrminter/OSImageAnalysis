cmake_minimum_required(VERSION 2.6)

# This project is designed to be built outside the Insight source tree.
# Modified by J. Minter for ITK libraries from v 4.0
PROJECT(shadecorrect)

# include information to allow running this in a debugger
# change "Debug" to "Release" or remove this line entirely to remove
SET(CMAKE_BUILD_TYPE Release)

# Find ITK.
FIND_PACKAGE(ITK)
IF(ITK_FOUND)
  INCLUDE(${ITK_USE_FILE})
ELSE(ITK_FOUND)
  MESSAGE(FATAL_ERROR
          "Cannot build without ITK.  Please set ITK_DIR.")
ENDIF(ITK_FOUND)

# added by jrm
if(COMMAND cmake_policy)
   cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

ADD_EXECUTABLE(shadecorrect16 shadecorrect16.cxx)

TARGET_LINK_LIBRARIES(shadecorrect16 ${ITK_LIBRARIES})
