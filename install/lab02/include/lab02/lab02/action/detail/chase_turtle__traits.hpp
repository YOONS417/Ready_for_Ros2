// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from lab02:action/ChaseTurtle.idl
// generated code does not contain a copyright notice

#ifndef LAB02__ACTION__DETAIL__CHASE_TURTLE__TRAITS_HPP_
#define LAB02__ACTION__DETAIL__CHASE_TURTLE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "lab02/action/detail/chase_turtle__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace lab02
{

namespace action
{

inline void to_flow_style_yaml(
  const ChaseTurtle_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: max_time_to_travel
  {
    out << "max_time_to_travel: ";
    rosidl_generator_traits::value_to_yaml(msg.max_time_to_travel, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChaseTurtle_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: max_time_to_travel
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "max_time_to_travel: ";
    rosidl_generator_traits::value_to_yaml(msg.max_time_to_travel, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChaseTurtle_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace lab02

namespace rosidl_generator_traits
{

[[deprecated("use lab02::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lab02::action::ChaseTurtle_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  lab02::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lab02::action::to_yaml() instead")]]
inline std::string to_yaml(const lab02::action::ChaseTurtle_Goal & msg)
{
  return lab02::action::to_yaml(msg);
}

template<>
inline const char * data_type<lab02::action::ChaseTurtle_Goal>()
{
  return "lab02::action::ChaseTurtle_Goal";
}

template<>
inline const char * name<lab02::action::ChaseTurtle_Goal>()
{
  return "lab02/action/ChaseTurtle_Goal";
}

template<>
struct has_fixed_size<lab02::action::ChaseTurtle_Goal>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<lab02::action::ChaseTurtle_Goal>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<lab02::action::ChaseTurtle_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace lab02
{

namespace action
{

inline void to_flow_style_yaml(
  const ChaseTurtle_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: caught
  {
    out << "caught: ";
    rosidl_generator_traits::value_to_yaml(msg.caught, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChaseTurtle_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: caught
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "caught: ";
    rosidl_generator_traits::value_to_yaml(msg.caught, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChaseTurtle_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace lab02

namespace rosidl_generator_traits
{

[[deprecated("use lab02::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lab02::action::ChaseTurtle_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  lab02::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lab02::action::to_yaml() instead")]]
inline std::string to_yaml(const lab02::action::ChaseTurtle_Result & msg)
{
  return lab02::action::to_yaml(msg);
}

template<>
inline const char * data_type<lab02::action::ChaseTurtle_Result>()
{
  return "lab02::action::ChaseTurtle_Result";
}

template<>
inline const char * name<lab02::action::ChaseTurtle_Result>()
{
  return "lab02/action/ChaseTurtle_Result";
}

template<>
struct has_fixed_size<lab02::action::ChaseTurtle_Result>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<lab02::action::ChaseTurtle_Result>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<lab02::action::ChaseTurtle_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace lab02
{

namespace action
{

inline void to_flow_style_yaml(
  const ChaseTurtle_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: distance_to_turtle1
  {
    out << "distance_to_turtle1: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_to_turtle1, out);
    out << ", ";
  }

  // member: time_travelled
  {
    out << "time_travelled: ";
    rosidl_generator_traits::value_to_yaml(msg.time_travelled, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChaseTurtle_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: distance_to_turtle1
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance_to_turtle1: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_to_turtle1, out);
    out << "\n";
  }

  // member: time_travelled
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "time_travelled: ";
    rosidl_generator_traits::value_to_yaml(msg.time_travelled, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChaseTurtle_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace lab02

namespace rosidl_generator_traits
{

[[deprecated("use lab02::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lab02::action::ChaseTurtle_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  lab02::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lab02::action::to_yaml() instead")]]
inline std::string to_yaml(const lab02::action::ChaseTurtle_Feedback & msg)
{
  return lab02::action::to_yaml(msg);
}

template<>
inline const char * data_type<lab02::action::ChaseTurtle_Feedback>()
{
  return "lab02::action::ChaseTurtle_Feedback";
}

template<>
inline const char * name<lab02::action::ChaseTurtle_Feedback>()
{
  return "lab02/action/ChaseTurtle_Feedback";
}

template<>
struct has_fixed_size<lab02::action::ChaseTurtle_Feedback>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<lab02::action::ChaseTurtle_Feedback>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<lab02::action::ChaseTurtle_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "lab02/action/detail/chase_turtle__traits.hpp"

namespace lab02
{

namespace action
{

inline void to_flow_style_yaml(
  const ChaseTurtle_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChaseTurtle_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChaseTurtle_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace lab02

namespace rosidl_generator_traits
{

[[deprecated("use lab02::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lab02::action::ChaseTurtle_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  lab02::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lab02::action::to_yaml() instead")]]
inline std::string to_yaml(const lab02::action::ChaseTurtle_SendGoal_Request & msg)
{
  return lab02::action::to_yaml(msg);
}

template<>
inline const char * data_type<lab02::action::ChaseTurtle_SendGoal_Request>()
{
  return "lab02::action::ChaseTurtle_SendGoal_Request";
}

template<>
inline const char * name<lab02::action::ChaseTurtle_SendGoal_Request>()
{
  return "lab02/action/ChaseTurtle_SendGoal_Request";
}

template<>
struct has_fixed_size<lab02::action::ChaseTurtle_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<lab02::action::ChaseTurtle_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<lab02::action::ChaseTurtle_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<lab02::action::ChaseTurtle_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<lab02::action::ChaseTurtle_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace lab02
{

namespace action
{

inline void to_flow_style_yaml(
  const ChaseTurtle_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChaseTurtle_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChaseTurtle_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace lab02

namespace rosidl_generator_traits
{

[[deprecated("use lab02::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lab02::action::ChaseTurtle_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  lab02::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lab02::action::to_yaml() instead")]]
inline std::string to_yaml(const lab02::action::ChaseTurtle_SendGoal_Response & msg)
{
  return lab02::action::to_yaml(msg);
}

template<>
inline const char * data_type<lab02::action::ChaseTurtle_SendGoal_Response>()
{
  return "lab02::action::ChaseTurtle_SendGoal_Response";
}

template<>
inline const char * name<lab02::action::ChaseTurtle_SendGoal_Response>()
{
  return "lab02/action/ChaseTurtle_SendGoal_Response";
}

template<>
struct has_fixed_size<lab02::action::ChaseTurtle_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<lab02::action::ChaseTurtle_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<lab02::action::ChaseTurtle_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<lab02::action::ChaseTurtle_SendGoal>()
{
  return "lab02::action::ChaseTurtle_SendGoal";
}

template<>
inline const char * name<lab02::action::ChaseTurtle_SendGoal>()
{
  return "lab02/action/ChaseTurtle_SendGoal";
}

template<>
struct has_fixed_size<lab02::action::ChaseTurtle_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<lab02::action::ChaseTurtle_SendGoal_Request>::value &&
    has_fixed_size<lab02::action::ChaseTurtle_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<lab02::action::ChaseTurtle_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<lab02::action::ChaseTurtle_SendGoal_Request>::value &&
    has_bounded_size<lab02::action::ChaseTurtle_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<lab02::action::ChaseTurtle_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<lab02::action::ChaseTurtle_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<lab02::action::ChaseTurtle_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace lab02
{

namespace action
{

inline void to_flow_style_yaml(
  const ChaseTurtle_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChaseTurtle_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChaseTurtle_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace lab02

namespace rosidl_generator_traits
{

[[deprecated("use lab02::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lab02::action::ChaseTurtle_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  lab02::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lab02::action::to_yaml() instead")]]
inline std::string to_yaml(const lab02::action::ChaseTurtle_GetResult_Request & msg)
{
  return lab02::action::to_yaml(msg);
}

template<>
inline const char * data_type<lab02::action::ChaseTurtle_GetResult_Request>()
{
  return "lab02::action::ChaseTurtle_GetResult_Request";
}

template<>
inline const char * name<lab02::action::ChaseTurtle_GetResult_Request>()
{
  return "lab02/action/ChaseTurtle_GetResult_Request";
}

template<>
struct has_fixed_size<lab02::action::ChaseTurtle_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<lab02::action::ChaseTurtle_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<lab02::action::ChaseTurtle_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "lab02/action/detail/chase_turtle__traits.hpp"

namespace lab02
{

namespace action
{

inline void to_flow_style_yaml(
  const ChaseTurtle_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChaseTurtle_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChaseTurtle_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace lab02

namespace rosidl_generator_traits
{

[[deprecated("use lab02::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lab02::action::ChaseTurtle_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  lab02::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lab02::action::to_yaml() instead")]]
inline std::string to_yaml(const lab02::action::ChaseTurtle_GetResult_Response & msg)
{
  return lab02::action::to_yaml(msg);
}

template<>
inline const char * data_type<lab02::action::ChaseTurtle_GetResult_Response>()
{
  return "lab02::action::ChaseTurtle_GetResult_Response";
}

template<>
inline const char * name<lab02::action::ChaseTurtle_GetResult_Response>()
{
  return "lab02/action/ChaseTurtle_GetResult_Response";
}

template<>
struct has_fixed_size<lab02::action::ChaseTurtle_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<lab02::action::ChaseTurtle_Result>::value> {};

template<>
struct has_bounded_size<lab02::action::ChaseTurtle_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<lab02::action::ChaseTurtle_Result>::value> {};

template<>
struct is_message<lab02::action::ChaseTurtle_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<lab02::action::ChaseTurtle_GetResult>()
{
  return "lab02::action::ChaseTurtle_GetResult";
}

template<>
inline const char * name<lab02::action::ChaseTurtle_GetResult>()
{
  return "lab02/action/ChaseTurtle_GetResult";
}

template<>
struct has_fixed_size<lab02::action::ChaseTurtle_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<lab02::action::ChaseTurtle_GetResult_Request>::value &&
    has_fixed_size<lab02::action::ChaseTurtle_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<lab02::action::ChaseTurtle_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<lab02::action::ChaseTurtle_GetResult_Request>::value &&
    has_bounded_size<lab02::action::ChaseTurtle_GetResult_Response>::value
  >
{
};

template<>
struct is_service<lab02::action::ChaseTurtle_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<lab02::action::ChaseTurtle_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<lab02::action::ChaseTurtle_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "lab02/action/detail/chase_turtle__traits.hpp"

namespace lab02
{

namespace action
{

inline void to_flow_style_yaml(
  const ChaseTurtle_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChaseTurtle_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChaseTurtle_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace lab02

namespace rosidl_generator_traits
{

[[deprecated("use lab02::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const lab02::action::ChaseTurtle_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  lab02::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use lab02::action::to_yaml() instead")]]
inline std::string to_yaml(const lab02::action::ChaseTurtle_FeedbackMessage & msg)
{
  return lab02::action::to_yaml(msg);
}

template<>
inline const char * data_type<lab02::action::ChaseTurtle_FeedbackMessage>()
{
  return "lab02::action::ChaseTurtle_FeedbackMessage";
}

template<>
inline const char * name<lab02::action::ChaseTurtle_FeedbackMessage>()
{
  return "lab02/action/ChaseTurtle_FeedbackMessage";
}

template<>
struct has_fixed_size<lab02::action::ChaseTurtle_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<lab02::action::ChaseTurtle_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<lab02::action::ChaseTurtle_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<lab02::action::ChaseTurtle_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<lab02::action::ChaseTurtle_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<lab02::action::ChaseTurtle>
  : std::true_type
{
};

template<>
struct is_action_goal<lab02::action::ChaseTurtle_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<lab02::action::ChaseTurtle_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<lab02::action::ChaseTurtle_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // LAB02__ACTION__DETAIL__CHASE_TURTLE__TRAITS_HPP_
