# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target action_tutorials_interfaces::action_tutorials_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${action_tutorials_interfaces_TARGETS}.
if(action_tutorials_interfaces_TARGETS AND NOT TARGET action_tutorials_interfaces::action_tutorials_interfaces)
  add_library(action_tutorials_interfaces::action_tutorials_interfaces INTERFACE IMPORTED)
  set_target_properties(action_tutorials_interfaces::action_tutorials_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${action_tutorials_interfaces_TARGETS}")
endif()
