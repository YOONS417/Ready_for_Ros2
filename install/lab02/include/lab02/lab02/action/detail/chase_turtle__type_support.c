// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from lab02:action/ChaseTurtle.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"
#include "lab02/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "lab02/action/detail/chase_turtle__functions.h"
#include "lab02/action/detail/chase_turtle__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lab02__action__ChaseTurtle_Goal__init(message_memory);
}

void lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_fini_function(void * message_memory)
{
  lab02__action__ChaseTurtle_Goal__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_message_member_array[1] = {
  {
    "max_time_to_travel",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_Goal, max_time_to_travel),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_message_members = {
  "lab02__action",  // message namespace
  "ChaseTurtle_Goal",  // message name
  1,  // number of fields
  sizeof(lab02__action__ChaseTurtle_Goal),
  lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_message_member_array,  // message members
  lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_init_function,  // function to initialize message memory (memory has to be allocated)
  lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_message_type_support_handle = {
  0,
  &lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lab02
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_Goal)() {
  if (!lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_message_type_support_handle.typesupport_identifier) {
    lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lab02__action__ChaseTurtle_Goal__rosidl_typesupport_introspection_c__ChaseTurtle_Goal_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "lab02/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "lab02/action/detail/chase_turtle__functions.h"
// already included above
// #include "lab02/action/detail/chase_turtle__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lab02__action__ChaseTurtle_Result__init(message_memory);
}

void lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_fini_function(void * message_memory)
{
  lab02__action__ChaseTurtle_Result__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_message_member_array[1] = {
  {
    "caught",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_Result, caught),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_message_members = {
  "lab02__action",  // message namespace
  "ChaseTurtle_Result",  // message name
  1,  // number of fields
  sizeof(lab02__action__ChaseTurtle_Result),
  lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_message_member_array,  // message members
  lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_init_function,  // function to initialize message memory (memory has to be allocated)
  lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_message_type_support_handle = {
  0,
  &lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lab02
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_Result)() {
  if (!lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_message_type_support_handle.typesupport_identifier) {
    lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lab02__action__ChaseTurtle_Result__rosidl_typesupport_introspection_c__ChaseTurtle_Result_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "lab02/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "lab02/action/detail/chase_turtle__functions.h"
// already included above
// #include "lab02/action/detail/chase_turtle__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lab02__action__ChaseTurtle_Feedback__init(message_memory);
}

void lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_fini_function(void * message_memory)
{
  lab02__action__ChaseTurtle_Feedback__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_message_member_array[2] = {
  {
    "distance_to_turtle1",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_Feedback, distance_to_turtle1),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "time_travelled",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_Feedback, time_travelled),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_message_members = {
  "lab02__action",  // message namespace
  "ChaseTurtle_Feedback",  // message name
  2,  // number of fields
  sizeof(lab02__action__ChaseTurtle_Feedback),
  lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_message_member_array,  // message members
  lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_init_function,  // function to initialize message memory (memory has to be allocated)
  lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_message_type_support_handle = {
  0,
  &lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lab02
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_Feedback)() {
  if (!lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_message_type_support_handle.typesupport_identifier) {
    lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lab02__action__ChaseTurtle_Feedback__rosidl_typesupport_introspection_c__ChaseTurtle_Feedback_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "lab02/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "lab02/action/detail/chase_turtle__functions.h"
// already included above
// #include "lab02/action/detail/chase_turtle__struct.h"


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"
// Member `goal`
#include "lab02/action/chase_turtle.h"
// Member `goal`
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lab02__action__ChaseTurtle_SendGoal_Request__init(message_memory);
}

void lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_fini_function(void * message_memory)
{
  lab02__action__ChaseTurtle_SendGoal_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_member_array[2] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_SendGoal_Request, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "goal",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_SendGoal_Request, goal),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_members = {
  "lab02__action",  // message namespace
  "ChaseTurtle_SendGoal_Request",  // message name
  2,  // number of fields
  sizeof(lab02__action__ChaseTurtle_SendGoal_Request),
  lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_member_array,  // message members
  lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_type_support_handle = {
  0,
  &lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lab02
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_SendGoal_Request)() {
  lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_Goal)();
  if (!lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_type_support_handle.typesupport_identifier) {
    lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lab02__action__ChaseTurtle_SendGoal_Request__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "lab02/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "lab02/action/detail/chase_turtle__functions.h"
// already included above
// #include "lab02/action/detail/chase_turtle__struct.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lab02__action__ChaseTurtle_SendGoal_Response__init(message_memory);
}

void lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_fini_function(void * message_memory)
{
  lab02__action__ChaseTurtle_SendGoal_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_message_member_array[2] = {
  {
    "accepted",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_SendGoal_Response, accepted),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_SendGoal_Response, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_message_members = {
  "lab02__action",  // message namespace
  "ChaseTurtle_SendGoal_Response",  // message name
  2,  // number of fields
  sizeof(lab02__action__ChaseTurtle_SendGoal_Response),
  lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_message_member_array,  // message members
  lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_message_type_support_handle = {
  0,
  &lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lab02
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_SendGoal_Response)() {
  lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_message_type_support_handle.typesupport_identifier) {
    lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lab02__action__ChaseTurtle_SendGoal_Response__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "lab02/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_service_members = {
  "lab02__action",  // service namespace
  "ChaseTurtle_SendGoal",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Request_message_type_support_handle,
  NULL  // response message
  // lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_Response_message_type_support_handle
};

static rosidl_service_type_support_t lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_service_type_support_handle = {
  0,
  &lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_SendGoal_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_SendGoal_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lab02
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_SendGoal)() {
  if (!lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_service_type_support_handle.typesupport_identifier) {
    lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_SendGoal_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_SendGoal_Response)()->data;
  }

  return &lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_SendGoal_service_type_support_handle;
}

// already included above
// #include <stddef.h>
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "lab02/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "lab02/action/detail/chase_turtle__functions.h"
// already included above
// #include "lab02/action/detail/chase_turtle__struct.h"


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lab02__action__ChaseTurtle_GetResult_Request__init(message_memory);
}

void lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_fini_function(void * message_memory)
{
  lab02__action__ChaseTurtle_GetResult_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_message_member_array[1] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_GetResult_Request, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_message_members = {
  "lab02__action",  // message namespace
  "ChaseTurtle_GetResult_Request",  // message name
  1,  // number of fields
  sizeof(lab02__action__ChaseTurtle_GetResult_Request),
  lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_message_member_array,  // message members
  lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_message_type_support_handle = {
  0,
  &lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lab02
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_GetResult_Request)() {
  lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  if (!lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_message_type_support_handle.typesupport_identifier) {
    lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lab02__action__ChaseTurtle_GetResult_Request__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "lab02/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "lab02/action/detail/chase_turtle__functions.h"
// already included above
// #include "lab02/action/detail/chase_turtle__struct.h"


// Include directives for member types
// Member `result`
// already included above
// #include "lab02/action/chase_turtle.h"
// Member `result`
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lab02__action__ChaseTurtle_GetResult_Response__init(message_memory);
}

void lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_fini_function(void * message_memory)
{
  lab02__action__ChaseTurtle_GetResult_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_message_member_array[2] = {
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_GetResult_Response, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "result",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_GetResult_Response, result),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_message_members = {
  "lab02__action",  // message namespace
  "ChaseTurtle_GetResult_Response",  // message name
  2,  // number of fields
  sizeof(lab02__action__ChaseTurtle_GetResult_Response),
  lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_message_member_array,  // message members
  lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_message_type_support_handle = {
  0,
  &lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lab02
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_GetResult_Response)() {
  lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_Result)();
  if (!lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_message_type_support_handle.typesupport_identifier) {
    lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lab02__action__ChaseTurtle_GetResult_Response__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "lab02/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_service_members = {
  "lab02__action",  // service namespace
  "ChaseTurtle_GetResult",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Request_message_type_support_handle,
  NULL  // response message
  // lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_Response_message_type_support_handle
};

static rosidl_service_type_support_t lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_service_type_support_handle = {
  0,
  &lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_GetResult_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_GetResult_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lab02
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_GetResult)() {
  if (!lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_service_type_support_handle.typesupport_identifier) {
    lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_GetResult_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_GetResult_Response)()->data;
  }

  return &lab02__action__detail__chase_turtle__rosidl_typesupport_introspection_c__ChaseTurtle_GetResult_service_type_support_handle;
}

// already included above
// #include <stddef.h>
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"
// already included above
// #include "lab02/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "lab02/action/detail/chase_turtle__functions.h"
// already included above
// #include "lab02/action/detail/chase_turtle__struct.h"


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"
// Member `feedback`
// already included above
// #include "lab02/action/chase_turtle.h"
// Member `feedback`
// already included above
// #include "lab02/action/detail/chase_turtle__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  lab02__action__ChaseTurtle_FeedbackMessage__init(message_memory);
}

void lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_fini_function(void * message_memory)
{
  lab02__action__ChaseTurtle_FeedbackMessage__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_message_member_array[2] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_FeedbackMessage, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "feedback",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(lab02__action__ChaseTurtle_FeedbackMessage, feedback),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_message_members = {
  "lab02__action",  // message namespace
  "ChaseTurtle_FeedbackMessage",  // message name
  2,  // number of fields
  sizeof(lab02__action__ChaseTurtle_FeedbackMessage),
  lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_message_member_array,  // message members
  lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_init_function,  // function to initialize message memory (memory has to be allocated)
  lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_message_type_support_handle = {
  0,
  &lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_lab02
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_FeedbackMessage)() {
  lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, lab02, action, ChaseTurtle_Feedback)();
  if (!lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_message_type_support_handle.typesupport_identifier) {
    lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &lab02__action__ChaseTurtle_FeedbackMessage__rosidl_typesupport_introspection_c__ChaseTurtle_FeedbackMessage_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
