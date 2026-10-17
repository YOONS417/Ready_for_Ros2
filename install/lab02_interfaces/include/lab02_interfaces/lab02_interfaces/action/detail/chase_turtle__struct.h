// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from lab02_interfaces:action/ChaseTurtle.idl
// generated code does not contain a copyright notice

#ifndef LAB02_INTERFACES__ACTION__DETAIL__CHASE_TURTLE__STRUCT_H_
#define LAB02_INTERFACES__ACTION__DETAIL__CHASE_TURTLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/ChaseTurtle in the package lab02_interfaces.
typedef struct lab02_interfaces__action__ChaseTurtle_Goal
{
  float max_time_to_travel;
} lab02_interfaces__action__ChaseTurtle_Goal;

// Struct for a sequence of lab02_interfaces__action__ChaseTurtle_Goal.
typedef struct lab02_interfaces__action__ChaseTurtle_Goal__Sequence
{
  lab02_interfaces__action__ChaseTurtle_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lab02_interfaces__action__ChaseTurtle_Goal__Sequence;


// Constants defined in the message

/// Struct defined in action/ChaseTurtle in the package lab02_interfaces.
typedef struct lab02_interfaces__action__ChaseTurtle_Result
{
  bool caught;
} lab02_interfaces__action__ChaseTurtle_Result;

// Struct for a sequence of lab02_interfaces__action__ChaseTurtle_Result.
typedef struct lab02_interfaces__action__ChaseTurtle_Result__Sequence
{
  lab02_interfaces__action__ChaseTurtle_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lab02_interfaces__action__ChaseTurtle_Result__Sequence;


// Constants defined in the message

/// Struct defined in action/ChaseTurtle in the package lab02_interfaces.
typedef struct lab02_interfaces__action__ChaseTurtle_Feedback
{
  float distance_to_turtle1;
  float time_travelled;
} lab02_interfaces__action__ChaseTurtle_Feedback;

// Struct for a sequence of lab02_interfaces__action__ChaseTurtle_Feedback.
typedef struct lab02_interfaces__action__ChaseTurtle_Feedback__Sequence
{
  lab02_interfaces__action__ChaseTurtle_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lab02_interfaces__action__ChaseTurtle_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "lab02_interfaces/action/detail/chase_turtle__struct.h"

/// Struct defined in action/ChaseTurtle in the package lab02_interfaces.
typedef struct lab02_interfaces__action__ChaseTurtle_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  lab02_interfaces__action__ChaseTurtle_Goal goal;
} lab02_interfaces__action__ChaseTurtle_SendGoal_Request;

// Struct for a sequence of lab02_interfaces__action__ChaseTurtle_SendGoal_Request.
typedef struct lab02_interfaces__action__ChaseTurtle_SendGoal_Request__Sequence
{
  lab02_interfaces__action__ChaseTurtle_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lab02_interfaces__action__ChaseTurtle_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/ChaseTurtle in the package lab02_interfaces.
typedef struct lab02_interfaces__action__ChaseTurtle_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} lab02_interfaces__action__ChaseTurtle_SendGoal_Response;

// Struct for a sequence of lab02_interfaces__action__ChaseTurtle_SendGoal_Response.
typedef struct lab02_interfaces__action__ChaseTurtle_SendGoal_Response__Sequence
{
  lab02_interfaces__action__ChaseTurtle_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lab02_interfaces__action__ChaseTurtle_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/ChaseTurtle in the package lab02_interfaces.
typedef struct lab02_interfaces__action__ChaseTurtle_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} lab02_interfaces__action__ChaseTurtle_GetResult_Request;

// Struct for a sequence of lab02_interfaces__action__ChaseTurtle_GetResult_Request.
typedef struct lab02_interfaces__action__ChaseTurtle_GetResult_Request__Sequence
{
  lab02_interfaces__action__ChaseTurtle_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lab02_interfaces__action__ChaseTurtle_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "lab02_interfaces/action/detail/chase_turtle__struct.h"

/// Struct defined in action/ChaseTurtle in the package lab02_interfaces.
typedef struct lab02_interfaces__action__ChaseTurtle_GetResult_Response
{
  int8_t status;
  lab02_interfaces__action__ChaseTurtle_Result result;
} lab02_interfaces__action__ChaseTurtle_GetResult_Response;

// Struct for a sequence of lab02_interfaces__action__ChaseTurtle_GetResult_Response.
typedef struct lab02_interfaces__action__ChaseTurtle_GetResult_Response__Sequence
{
  lab02_interfaces__action__ChaseTurtle_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lab02_interfaces__action__ChaseTurtle_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "lab02_interfaces/action/detail/chase_turtle__struct.h"

/// Struct defined in action/ChaseTurtle in the package lab02_interfaces.
typedef struct lab02_interfaces__action__ChaseTurtle_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  lab02_interfaces__action__ChaseTurtle_Feedback feedback;
} lab02_interfaces__action__ChaseTurtle_FeedbackMessage;

// Struct for a sequence of lab02_interfaces__action__ChaseTurtle_FeedbackMessage.
typedef struct lab02_interfaces__action__ChaseTurtle_FeedbackMessage__Sequence
{
  lab02_interfaces__action__ChaseTurtle_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} lab02_interfaces__action__ChaseTurtle_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // LAB02_INTERFACES__ACTION__DETAIL__CHASE_TURTLE__STRUCT_H_
