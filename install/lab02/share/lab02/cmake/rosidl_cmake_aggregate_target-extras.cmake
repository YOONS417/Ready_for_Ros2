# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target lab02::lab02
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${lab02_TARGETS}.
if(lab02_TARGETS AND NOT TARGET lab02::lab02)
  add_library(lab02::lab02 INTERFACE IMPORTED)
  set_target_properties(lab02::lab02 PROPERTIES
    INTERFACE_LINK_LIBRARIES "${lab02_TARGETS}")
endif()
