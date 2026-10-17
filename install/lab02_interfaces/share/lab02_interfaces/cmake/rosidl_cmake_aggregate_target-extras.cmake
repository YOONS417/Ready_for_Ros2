# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target lab02_interfaces::lab02_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${lab02_interfaces_TARGETS}.
if(lab02_interfaces_TARGETS AND NOT TARGET lab02_interfaces::lab02_interfaces)
  add_library(lab02_interfaces::lab02_interfaces INTERFACE IMPORTED)
  set_target_properties(lab02_interfaces::lab02_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${lab02_interfaces_TARGETS}")
endif()
