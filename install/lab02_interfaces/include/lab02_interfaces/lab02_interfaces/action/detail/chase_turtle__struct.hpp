// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from lab02_interfaces:action/ChaseTurtle.idl
// generated code does not contain a copyright notice

#ifndef LAB02_INTERFACES__ACTION__DETAIL__CHASE_TURTLE__STRUCT_HPP_
#define LAB02_INTERFACES__ACTION__DETAIL__CHASE_TURTLE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_Goal __attribute__((deprecated))
#else
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_Goal __declspec(deprecated)
#endif

namespace lab02_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChaseTurtle_Goal_
{
  using Type = ChaseTurtle_Goal_<ContainerAllocator>;

  explicit ChaseTurtle_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->max_time_to_travel = 0.0f;
    }
  }

  explicit ChaseTurtle_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->max_time_to_travel = 0.0f;
    }
  }

  // field types and members
  using _max_time_to_travel_type =
    float;
  _max_time_to_travel_type max_time_to_travel;

  // setters for named parameter idiom
  Type & set__max_time_to_travel(
    const float & _arg)
  {
    this->max_time_to_travel = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_Goal
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_Goal
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChaseTurtle_Goal_ & other) const
  {
    if (this->max_time_to_travel != other.max_time_to_travel) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChaseTurtle_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChaseTurtle_Goal_

// alias to use template instance with default allocator
using ChaseTurtle_Goal =
  lab02_interfaces::action::ChaseTurtle_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace lab02_interfaces


#ifndef _WIN32
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_Result __attribute__((deprecated))
#else
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_Result __declspec(deprecated)
#endif

namespace lab02_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChaseTurtle_Result_
{
  using Type = ChaseTurtle_Result_<ContainerAllocator>;

  explicit ChaseTurtle_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->caught = false;
    }
  }

  explicit ChaseTurtle_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->caught = false;
    }
  }

  // field types and members
  using _caught_type =
    bool;
  _caught_type caught;

  // setters for named parameter idiom
  Type & set__caught(
    const bool & _arg)
  {
    this->caught = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_Result
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_Result
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChaseTurtle_Result_ & other) const
  {
    if (this->caught != other.caught) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChaseTurtle_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChaseTurtle_Result_

// alias to use template instance with default allocator
using ChaseTurtle_Result =
  lab02_interfaces::action::ChaseTurtle_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace lab02_interfaces


#ifndef _WIN32
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_Feedback __declspec(deprecated)
#endif

namespace lab02_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChaseTurtle_Feedback_
{
  using Type = ChaseTurtle_Feedback_<ContainerAllocator>;

  explicit ChaseTurtle_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->distance_to_turtle1 = 0.0f;
      this->time_travelled = 0.0f;
    }
  }

  explicit ChaseTurtle_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->distance_to_turtle1 = 0.0f;
      this->time_travelled = 0.0f;
    }
  }

  // field types and members
  using _distance_to_turtle1_type =
    float;
  _distance_to_turtle1_type distance_to_turtle1;
  using _time_travelled_type =
    float;
  _time_travelled_type time_travelled;

  // setters for named parameter idiom
  Type & set__distance_to_turtle1(
    const float & _arg)
  {
    this->distance_to_turtle1 = _arg;
    return *this;
  }
  Type & set__time_travelled(
    const float & _arg)
  {
    this->time_travelled = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_Feedback
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_Feedback
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChaseTurtle_Feedback_ & other) const
  {
    if (this->distance_to_turtle1 != other.distance_to_turtle1) {
      return false;
    }
    if (this->time_travelled != other.time_travelled) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChaseTurtle_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChaseTurtle_Feedback_

// alias to use template instance with default allocator
using ChaseTurtle_Feedback =
  lab02_interfaces::action::ChaseTurtle_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace lab02_interfaces


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "lab02_interfaces/action/detail/chase_turtle__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_SendGoal_Request __declspec(deprecated)
#endif

namespace lab02_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChaseTurtle_SendGoal_Request_
{
  using Type = ChaseTurtle_SendGoal_Request_<ContainerAllocator>;

  explicit ChaseTurtle_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit ChaseTurtle_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const lab02_interfaces::action::ChaseTurtle_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_SendGoal_Request
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_SendGoal_Request
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChaseTurtle_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChaseTurtle_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChaseTurtle_SendGoal_Request_

// alias to use template instance with default allocator
using ChaseTurtle_SendGoal_Request =
  lab02_interfaces::action::ChaseTurtle_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace lab02_interfaces


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_SendGoal_Response __declspec(deprecated)
#endif

namespace lab02_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChaseTurtle_SendGoal_Response_
{
  using Type = ChaseTurtle_SendGoal_Response_<ContainerAllocator>;

  explicit ChaseTurtle_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit ChaseTurtle_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_SendGoal_Response
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_SendGoal_Response
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChaseTurtle_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChaseTurtle_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChaseTurtle_SendGoal_Response_

// alias to use template instance with default allocator
using ChaseTurtle_SendGoal_Response =
  lab02_interfaces::action::ChaseTurtle_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace lab02_interfaces

namespace lab02_interfaces
{

namespace action
{

struct ChaseTurtle_SendGoal
{
  using Request = lab02_interfaces::action::ChaseTurtle_SendGoal_Request;
  using Response = lab02_interfaces::action::ChaseTurtle_SendGoal_Response;
};

}  // namespace action

}  // namespace lab02_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_GetResult_Request __declspec(deprecated)
#endif

namespace lab02_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChaseTurtle_GetResult_Request_
{
  using Type = ChaseTurtle_GetResult_Request_<ContainerAllocator>;

  explicit ChaseTurtle_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit ChaseTurtle_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_GetResult_Request
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_GetResult_Request
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChaseTurtle_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChaseTurtle_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChaseTurtle_GetResult_Request_

// alias to use template instance with default allocator
using ChaseTurtle_GetResult_Request =
  lab02_interfaces::action::ChaseTurtle_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace lab02_interfaces


// Include directives for member types
// Member 'result'
// already included above
// #include "lab02_interfaces/action/detail/chase_turtle__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_GetResult_Response __declspec(deprecated)
#endif

namespace lab02_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChaseTurtle_GetResult_Response_
{
  using Type = ChaseTurtle_GetResult_Response_<ContainerAllocator>;

  explicit ChaseTurtle_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit ChaseTurtle_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const lab02_interfaces::action::ChaseTurtle_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_GetResult_Response
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_GetResult_Response
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChaseTurtle_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChaseTurtle_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChaseTurtle_GetResult_Response_

// alias to use template instance with default allocator
using ChaseTurtle_GetResult_Response =
  lab02_interfaces::action::ChaseTurtle_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace lab02_interfaces

namespace lab02_interfaces
{

namespace action
{

struct ChaseTurtle_GetResult
{
  using Request = lab02_interfaces::action::ChaseTurtle_GetResult_Request;
  using Response = lab02_interfaces::action::ChaseTurtle_GetResult_Response;
};

}  // namespace action

}  // namespace lab02_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "lab02_interfaces/action/detail/chase_turtle__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__lab02_interfaces__action__ChaseTurtle_FeedbackMessage __declspec(deprecated)
#endif

namespace lab02_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ChaseTurtle_FeedbackMessage_
{
  using Type = ChaseTurtle_FeedbackMessage_<ContainerAllocator>;

  explicit ChaseTurtle_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit ChaseTurtle_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const lab02_interfaces::action::ChaseTurtle_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_FeedbackMessage
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__lab02_interfaces__action__ChaseTurtle_FeedbackMessage
    std::shared_ptr<lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChaseTurtle_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChaseTurtle_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChaseTurtle_FeedbackMessage_

// alias to use template instance with default allocator
using ChaseTurtle_FeedbackMessage =
  lab02_interfaces::action::ChaseTurtle_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace lab02_interfaces

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace lab02_interfaces
{

namespace action
{

struct ChaseTurtle
{
  /// The goal message defined in the action definition.
  using Goal = lab02_interfaces::action::ChaseTurtle_Goal;
  /// The result message defined in the action definition.
  using Result = lab02_interfaces::action::ChaseTurtle_Result;
  /// The feedback message defined in the action definition.
  using Feedback = lab02_interfaces::action::ChaseTurtle_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = lab02_interfaces::action::ChaseTurtle_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = lab02_interfaces::action::ChaseTurtle_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = lab02_interfaces::action::ChaseTurtle_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct ChaseTurtle ChaseTurtle;

}  // namespace action

}  // namespace lab02_interfaces

#endif  // LAB02_INTERFACES__ACTION__DETAIL__CHASE_TURTLE__STRUCT_HPP_
