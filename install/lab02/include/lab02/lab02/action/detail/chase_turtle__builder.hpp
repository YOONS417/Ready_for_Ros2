// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from lab02:action/ChaseTurtle.idl
// generated code does not contain a copyright notice

#ifndef LAB02__ACTION__DETAIL__CHASE_TURTLE__BUILDER_HPP_
#define LAB02__ACTION__DETAIL__CHASE_TURTLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "lab02/action/detail/chase_turtle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace lab02
{

namespace action
{

namespace builder
{

class Init_ChaseTurtle_Goal_max_time_to_travel
{
public:
  Init_ChaseTurtle_Goal_max_time_to_travel()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::lab02::action::ChaseTurtle_Goal max_time_to_travel(::lab02::action::ChaseTurtle_Goal::_max_time_to_travel_type arg)
  {
    msg_.max_time_to_travel = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::lab02::action::ChaseTurtle_Goal>()
{
  return lab02::action::builder::Init_ChaseTurtle_Goal_max_time_to_travel();
}

}  // namespace lab02


namespace lab02
{

namespace action
{

namespace builder
{

class Init_ChaseTurtle_Result_caught
{
public:
  Init_ChaseTurtle_Result_caught()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::lab02::action::ChaseTurtle_Result caught(::lab02::action::ChaseTurtle_Result::_caught_type arg)
  {
    msg_.caught = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::lab02::action::ChaseTurtle_Result>()
{
  return lab02::action::builder::Init_ChaseTurtle_Result_caught();
}

}  // namespace lab02


namespace lab02
{

namespace action
{

namespace builder
{

class Init_ChaseTurtle_Feedback_time_travelled
{
public:
  explicit Init_ChaseTurtle_Feedback_time_travelled(::lab02::action::ChaseTurtle_Feedback & msg)
  : msg_(msg)
  {}
  ::lab02::action::ChaseTurtle_Feedback time_travelled(::lab02::action::ChaseTurtle_Feedback::_time_travelled_type arg)
  {
    msg_.time_travelled = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_Feedback msg_;
};

class Init_ChaseTurtle_Feedback_distance_to_turtle1
{
public:
  Init_ChaseTurtle_Feedback_distance_to_turtle1()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChaseTurtle_Feedback_time_travelled distance_to_turtle1(::lab02::action::ChaseTurtle_Feedback::_distance_to_turtle1_type arg)
  {
    msg_.distance_to_turtle1 = std::move(arg);
    return Init_ChaseTurtle_Feedback_time_travelled(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::lab02::action::ChaseTurtle_Feedback>()
{
  return lab02::action::builder::Init_ChaseTurtle_Feedback_distance_to_turtle1();
}

}  // namespace lab02


namespace lab02
{

namespace action
{

namespace builder
{

class Init_ChaseTurtle_SendGoal_Request_goal
{
public:
  explicit Init_ChaseTurtle_SendGoal_Request_goal(::lab02::action::ChaseTurtle_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::lab02::action::ChaseTurtle_SendGoal_Request goal(::lab02::action::ChaseTurtle_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_SendGoal_Request msg_;
};

class Init_ChaseTurtle_SendGoal_Request_goal_id
{
public:
  Init_ChaseTurtle_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChaseTurtle_SendGoal_Request_goal goal_id(::lab02::action::ChaseTurtle_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ChaseTurtle_SendGoal_Request_goal(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::lab02::action::ChaseTurtle_SendGoal_Request>()
{
  return lab02::action::builder::Init_ChaseTurtle_SendGoal_Request_goal_id();
}

}  // namespace lab02


namespace lab02
{

namespace action
{

namespace builder
{

class Init_ChaseTurtle_SendGoal_Response_stamp
{
public:
  explicit Init_ChaseTurtle_SendGoal_Response_stamp(::lab02::action::ChaseTurtle_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::lab02::action::ChaseTurtle_SendGoal_Response stamp(::lab02::action::ChaseTurtle_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_SendGoal_Response msg_;
};

class Init_ChaseTurtle_SendGoal_Response_accepted
{
public:
  Init_ChaseTurtle_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChaseTurtle_SendGoal_Response_stamp accepted(::lab02::action::ChaseTurtle_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_ChaseTurtle_SendGoal_Response_stamp(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::lab02::action::ChaseTurtle_SendGoal_Response>()
{
  return lab02::action::builder::Init_ChaseTurtle_SendGoal_Response_accepted();
}

}  // namespace lab02


namespace lab02
{

namespace action
{

namespace builder
{

class Init_ChaseTurtle_GetResult_Request_goal_id
{
public:
  Init_ChaseTurtle_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::lab02::action::ChaseTurtle_GetResult_Request goal_id(::lab02::action::ChaseTurtle_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::lab02::action::ChaseTurtle_GetResult_Request>()
{
  return lab02::action::builder::Init_ChaseTurtle_GetResult_Request_goal_id();
}

}  // namespace lab02


namespace lab02
{

namespace action
{

namespace builder
{

class Init_ChaseTurtle_GetResult_Response_result
{
public:
  explicit Init_ChaseTurtle_GetResult_Response_result(::lab02::action::ChaseTurtle_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::lab02::action::ChaseTurtle_GetResult_Response result(::lab02::action::ChaseTurtle_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_GetResult_Response msg_;
};

class Init_ChaseTurtle_GetResult_Response_status
{
public:
  Init_ChaseTurtle_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChaseTurtle_GetResult_Response_result status(::lab02::action::ChaseTurtle_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_ChaseTurtle_GetResult_Response_result(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::lab02::action::ChaseTurtle_GetResult_Response>()
{
  return lab02::action::builder::Init_ChaseTurtle_GetResult_Response_status();
}

}  // namespace lab02


namespace lab02
{

namespace action
{

namespace builder
{

class Init_ChaseTurtle_FeedbackMessage_feedback
{
public:
  explicit Init_ChaseTurtle_FeedbackMessage_feedback(::lab02::action::ChaseTurtle_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::lab02::action::ChaseTurtle_FeedbackMessage feedback(::lab02::action::ChaseTurtle_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_FeedbackMessage msg_;
};

class Init_ChaseTurtle_FeedbackMessage_goal_id
{
public:
  Init_ChaseTurtle_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChaseTurtle_FeedbackMessage_feedback goal_id(::lab02::action::ChaseTurtle_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ChaseTurtle_FeedbackMessage_feedback(msg_);
  }

private:
  ::lab02::action::ChaseTurtle_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::lab02::action::ChaseTurtle_FeedbackMessage>()
{
  return lab02::action::builder::Init_ChaseTurtle_FeedbackMessage_goal_id();
}

}  // namespace lab02

#endif  // LAB02__ACTION__DETAIL__CHASE_TURTLE__BUILDER_HPP_
