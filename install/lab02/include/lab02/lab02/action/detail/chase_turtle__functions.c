// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from lab02:action/ChaseTurtle.idl
// generated code does not contain a copyright notice
#include "lab02/action/detail/chase_turtle__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
lab02__action__ChaseTurtle_Goal__init(lab02__action__ChaseTurtle_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // max_time_to_travel
  return true;
}

void
lab02__action__ChaseTurtle_Goal__fini(lab02__action__ChaseTurtle_Goal * msg)
{
  if (!msg) {
    return;
  }
  // max_time_to_travel
}

bool
lab02__action__ChaseTurtle_Goal__are_equal(const lab02__action__ChaseTurtle_Goal * lhs, const lab02__action__ChaseTurtle_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // max_time_to_travel
  if (lhs->max_time_to_travel != rhs->max_time_to_travel) {
    return false;
  }
  return true;
}

bool
lab02__action__ChaseTurtle_Goal__copy(
  const lab02__action__ChaseTurtle_Goal * input,
  lab02__action__ChaseTurtle_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // max_time_to_travel
  output->max_time_to_travel = input->max_time_to_travel;
  return true;
}

lab02__action__ChaseTurtle_Goal *
lab02__action__ChaseTurtle_Goal__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_Goal * msg = (lab02__action__ChaseTurtle_Goal *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lab02__action__ChaseTurtle_Goal));
  bool success = lab02__action__ChaseTurtle_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lab02__action__ChaseTurtle_Goal__destroy(lab02__action__ChaseTurtle_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lab02__action__ChaseTurtle_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lab02__action__ChaseTurtle_Goal__Sequence__init(lab02__action__ChaseTurtle_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_Goal * data = NULL;

  if (size) {
    data = (lab02__action__ChaseTurtle_Goal *)allocator.zero_allocate(size, sizeof(lab02__action__ChaseTurtle_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lab02__action__ChaseTurtle_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lab02__action__ChaseTurtle_Goal__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
lab02__action__ChaseTurtle_Goal__Sequence__fini(lab02__action__ChaseTurtle_Goal__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      lab02__action__ChaseTurtle_Goal__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

lab02__action__ChaseTurtle_Goal__Sequence *
lab02__action__ChaseTurtle_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_Goal__Sequence * array = (lab02__action__ChaseTurtle_Goal__Sequence *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lab02__action__ChaseTurtle_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lab02__action__ChaseTurtle_Goal__Sequence__destroy(lab02__action__ChaseTurtle_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lab02__action__ChaseTurtle_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lab02__action__ChaseTurtle_Goal__Sequence__are_equal(const lab02__action__ChaseTurtle_Goal__Sequence * lhs, const lab02__action__ChaseTurtle_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lab02__action__ChaseTurtle_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lab02__action__ChaseTurtle_Goal__Sequence__copy(
  const lab02__action__ChaseTurtle_Goal__Sequence * input,
  lab02__action__ChaseTurtle_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lab02__action__ChaseTurtle_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lab02__action__ChaseTurtle_Goal * data =
      (lab02__action__ChaseTurtle_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lab02__action__ChaseTurtle_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lab02__action__ChaseTurtle_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lab02__action__ChaseTurtle_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
lab02__action__ChaseTurtle_Result__init(lab02__action__ChaseTurtle_Result * msg)
{
  if (!msg) {
    return false;
  }
  // caught
  return true;
}

void
lab02__action__ChaseTurtle_Result__fini(lab02__action__ChaseTurtle_Result * msg)
{
  if (!msg) {
    return;
  }
  // caught
}

bool
lab02__action__ChaseTurtle_Result__are_equal(const lab02__action__ChaseTurtle_Result * lhs, const lab02__action__ChaseTurtle_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // caught
  if (lhs->caught != rhs->caught) {
    return false;
  }
  return true;
}

bool
lab02__action__ChaseTurtle_Result__copy(
  const lab02__action__ChaseTurtle_Result * input,
  lab02__action__ChaseTurtle_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // caught
  output->caught = input->caught;
  return true;
}

lab02__action__ChaseTurtle_Result *
lab02__action__ChaseTurtle_Result__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_Result * msg = (lab02__action__ChaseTurtle_Result *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lab02__action__ChaseTurtle_Result));
  bool success = lab02__action__ChaseTurtle_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lab02__action__ChaseTurtle_Result__destroy(lab02__action__ChaseTurtle_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lab02__action__ChaseTurtle_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lab02__action__ChaseTurtle_Result__Sequence__init(lab02__action__ChaseTurtle_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_Result * data = NULL;

  if (size) {
    data = (lab02__action__ChaseTurtle_Result *)allocator.zero_allocate(size, sizeof(lab02__action__ChaseTurtle_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lab02__action__ChaseTurtle_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lab02__action__ChaseTurtle_Result__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
lab02__action__ChaseTurtle_Result__Sequence__fini(lab02__action__ChaseTurtle_Result__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      lab02__action__ChaseTurtle_Result__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

lab02__action__ChaseTurtle_Result__Sequence *
lab02__action__ChaseTurtle_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_Result__Sequence * array = (lab02__action__ChaseTurtle_Result__Sequence *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lab02__action__ChaseTurtle_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lab02__action__ChaseTurtle_Result__Sequence__destroy(lab02__action__ChaseTurtle_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lab02__action__ChaseTurtle_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lab02__action__ChaseTurtle_Result__Sequence__are_equal(const lab02__action__ChaseTurtle_Result__Sequence * lhs, const lab02__action__ChaseTurtle_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lab02__action__ChaseTurtle_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lab02__action__ChaseTurtle_Result__Sequence__copy(
  const lab02__action__ChaseTurtle_Result__Sequence * input,
  lab02__action__ChaseTurtle_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lab02__action__ChaseTurtle_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lab02__action__ChaseTurtle_Result * data =
      (lab02__action__ChaseTurtle_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lab02__action__ChaseTurtle_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lab02__action__ChaseTurtle_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lab02__action__ChaseTurtle_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
lab02__action__ChaseTurtle_Feedback__init(lab02__action__ChaseTurtle_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // distance_to_turtle1
  // time_travelled
  return true;
}

void
lab02__action__ChaseTurtle_Feedback__fini(lab02__action__ChaseTurtle_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // distance_to_turtle1
  // time_travelled
}

bool
lab02__action__ChaseTurtle_Feedback__are_equal(const lab02__action__ChaseTurtle_Feedback * lhs, const lab02__action__ChaseTurtle_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // distance_to_turtle1
  if (lhs->distance_to_turtle1 != rhs->distance_to_turtle1) {
    return false;
  }
  // time_travelled
  if (lhs->time_travelled != rhs->time_travelled) {
    return false;
  }
  return true;
}

bool
lab02__action__ChaseTurtle_Feedback__copy(
  const lab02__action__ChaseTurtle_Feedback * input,
  lab02__action__ChaseTurtle_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // distance_to_turtle1
  output->distance_to_turtle1 = input->distance_to_turtle1;
  // time_travelled
  output->time_travelled = input->time_travelled;
  return true;
}

lab02__action__ChaseTurtle_Feedback *
lab02__action__ChaseTurtle_Feedback__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_Feedback * msg = (lab02__action__ChaseTurtle_Feedback *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lab02__action__ChaseTurtle_Feedback));
  bool success = lab02__action__ChaseTurtle_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lab02__action__ChaseTurtle_Feedback__destroy(lab02__action__ChaseTurtle_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lab02__action__ChaseTurtle_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lab02__action__ChaseTurtle_Feedback__Sequence__init(lab02__action__ChaseTurtle_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_Feedback * data = NULL;

  if (size) {
    data = (lab02__action__ChaseTurtle_Feedback *)allocator.zero_allocate(size, sizeof(lab02__action__ChaseTurtle_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lab02__action__ChaseTurtle_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lab02__action__ChaseTurtle_Feedback__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
lab02__action__ChaseTurtle_Feedback__Sequence__fini(lab02__action__ChaseTurtle_Feedback__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      lab02__action__ChaseTurtle_Feedback__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

lab02__action__ChaseTurtle_Feedback__Sequence *
lab02__action__ChaseTurtle_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_Feedback__Sequence * array = (lab02__action__ChaseTurtle_Feedback__Sequence *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lab02__action__ChaseTurtle_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lab02__action__ChaseTurtle_Feedback__Sequence__destroy(lab02__action__ChaseTurtle_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lab02__action__ChaseTurtle_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lab02__action__ChaseTurtle_Feedback__Sequence__are_equal(const lab02__action__ChaseTurtle_Feedback__Sequence * lhs, const lab02__action__ChaseTurtle_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lab02__action__ChaseTurtle_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lab02__action__ChaseTurtle_Feedback__Sequence__copy(
  const lab02__action__ChaseTurtle_Feedback__Sequence * input,
  lab02__action__ChaseTurtle_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lab02__action__ChaseTurtle_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lab02__action__ChaseTurtle_Feedback * data =
      (lab02__action__ChaseTurtle_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lab02__action__ChaseTurtle_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lab02__action__ChaseTurtle_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lab02__action__ChaseTurtle_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "lab02/action/detail/chase_turtle__functions.h"

bool
lab02__action__ChaseTurtle_SendGoal_Request__init(lab02__action__ChaseTurtle_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    lab02__action__ChaseTurtle_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!lab02__action__ChaseTurtle_Goal__init(&msg->goal)) {
    lab02__action__ChaseTurtle_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
lab02__action__ChaseTurtle_SendGoal_Request__fini(lab02__action__ChaseTurtle_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  lab02__action__ChaseTurtle_Goal__fini(&msg->goal);
}

bool
lab02__action__ChaseTurtle_SendGoal_Request__are_equal(const lab02__action__ChaseTurtle_SendGoal_Request * lhs, const lab02__action__ChaseTurtle_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!lab02__action__ChaseTurtle_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
lab02__action__ChaseTurtle_SendGoal_Request__copy(
  const lab02__action__ChaseTurtle_SendGoal_Request * input,
  lab02__action__ChaseTurtle_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!lab02__action__ChaseTurtle_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

lab02__action__ChaseTurtle_SendGoal_Request *
lab02__action__ChaseTurtle_SendGoal_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_SendGoal_Request * msg = (lab02__action__ChaseTurtle_SendGoal_Request *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lab02__action__ChaseTurtle_SendGoal_Request));
  bool success = lab02__action__ChaseTurtle_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lab02__action__ChaseTurtle_SendGoal_Request__destroy(lab02__action__ChaseTurtle_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lab02__action__ChaseTurtle_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lab02__action__ChaseTurtle_SendGoal_Request__Sequence__init(lab02__action__ChaseTurtle_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_SendGoal_Request * data = NULL;

  if (size) {
    data = (lab02__action__ChaseTurtle_SendGoal_Request *)allocator.zero_allocate(size, sizeof(lab02__action__ChaseTurtle_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lab02__action__ChaseTurtle_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lab02__action__ChaseTurtle_SendGoal_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
lab02__action__ChaseTurtle_SendGoal_Request__Sequence__fini(lab02__action__ChaseTurtle_SendGoal_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      lab02__action__ChaseTurtle_SendGoal_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

lab02__action__ChaseTurtle_SendGoal_Request__Sequence *
lab02__action__ChaseTurtle_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_SendGoal_Request__Sequence * array = (lab02__action__ChaseTurtle_SendGoal_Request__Sequence *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lab02__action__ChaseTurtle_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lab02__action__ChaseTurtle_SendGoal_Request__Sequence__destroy(lab02__action__ChaseTurtle_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lab02__action__ChaseTurtle_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lab02__action__ChaseTurtle_SendGoal_Request__Sequence__are_equal(const lab02__action__ChaseTurtle_SendGoal_Request__Sequence * lhs, const lab02__action__ChaseTurtle_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lab02__action__ChaseTurtle_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lab02__action__ChaseTurtle_SendGoal_Request__Sequence__copy(
  const lab02__action__ChaseTurtle_SendGoal_Request__Sequence * input,
  lab02__action__ChaseTurtle_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lab02__action__ChaseTurtle_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lab02__action__ChaseTurtle_SendGoal_Request * data =
      (lab02__action__ChaseTurtle_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lab02__action__ChaseTurtle_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lab02__action__ChaseTurtle_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lab02__action__ChaseTurtle_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
lab02__action__ChaseTurtle_SendGoal_Response__init(lab02__action__ChaseTurtle_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    lab02__action__ChaseTurtle_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
lab02__action__ChaseTurtle_SendGoal_Response__fini(lab02__action__ChaseTurtle_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
lab02__action__ChaseTurtle_SendGoal_Response__are_equal(const lab02__action__ChaseTurtle_SendGoal_Response * lhs, const lab02__action__ChaseTurtle_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
lab02__action__ChaseTurtle_SendGoal_Response__copy(
  const lab02__action__ChaseTurtle_SendGoal_Response * input,
  lab02__action__ChaseTurtle_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

lab02__action__ChaseTurtle_SendGoal_Response *
lab02__action__ChaseTurtle_SendGoal_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_SendGoal_Response * msg = (lab02__action__ChaseTurtle_SendGoal_Response *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lab02__action__ChaseTurtle_SendGoal_Response));
  bool success = lab02__action__ChaseTurtle_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lab02__action__ChaseTurtle_SendGoal_Response__destroy(lab02__action__ChaseTurtle_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lab02__action__ChaseTurtle_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lab02__action__ChaseTurtle_SendGoal_Response__Sequence__init(lab02__action__ChaseTurtle_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_SendGoal_Response * data = NULL;

  if (size) {
    data = (lab02__action__ChaseTurtle_SendGoal_Response *)allocator.zero_allocate(size, sizeof(lab02__action__ChaseTurtle_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lab02__action__ChaseTurtle_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lab02__action__ChaseTurtle_SendGoal_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
lab02__action__ChaseTurtle_SendGoal_Response__Sequence__fini(lab02__action__ChaseTurtle_SendGoal_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      lab02__action__ChaseTurtle_SendGoal_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

lab02__action__ChaseTurtle_SendGoal_Response__Sequence *
lab02__action__ChaseTurtle_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_SendGoal_Response__Sequence * array = (lab02__action__ChaseTurtle_SendGoal_Response__Sequence *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lab02__action__ChaseTurtle_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lab02__action__ChaseTurtle_SendGoal_Response__Sequence__destroy(lab02__action__ChaseTurtle_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lab02__action__ChaseTurtle_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lab02__action__ChaseTurtle_SendGoal_Response__Sequence__are_equal(const lab02__action__ChaseTurtle_SendGoal_Response__Sequence * lhs, const lab02__action__ChaseTurtle_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lab02__action__ChaseTurtle_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lab02__action__ChaseTurtle_SendGoal_Response__Sequence__copy(
  const lab02__action__ChaseTurtle_SendGoal_Response__Sequence * input,
  lab02__action__ChaseTurtle_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lab02__action__ChaseTurtle_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lab02__action__ChaseTurtle_SendGoal_Response * data =
      (lab02__action__ChaseTurtle_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lab02__action__ChaseTurtle_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lab02__action__ChaseTurtle_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lab02__action__ChaseTurtle_SendGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
lab02__action__ChaseTurtle_GetResult_Request__init(lab02__action__ChaseTurtle_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    lab02__action__ChaseTurtle_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
lab02__action__ChaseTurtle_GetResult_Request__fini(lab02__action__ChaseTurtle_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
lab02__action__ChaseTurtle_GetResult_Request__are_equal(const lab02__action__ChaseTurtle_GetResult_Request * lhs, const lab02__action__ChaseTurtle_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
lab02__action__ChaseTurtle_GetResult_Request__copy(
  const lab02__action__ChaseTurtle_GetResult_Request * input,
  lab02__action__ChaseTurtle_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

lab02__action__ChaseTurtle_GetResult_Request *
lab02__action__ChaseTurtle_GetResult_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_GetResult_Request * msg = (lab02__action__ChaseTurtle_GetResult_Request *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lab02__action__ChaseTurtle_GetResult_Request));
  bool success = lab02__action__ChaseTurtle_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lab02__action__ChaseTurtle_GetResult_Request__destroy(lab02__action__ChaseTurtle_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lab02__action__ChaseTurtle_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lab02__action__ChaseTurtle_GetResult_Request__Sequence__init(lab02__action__ChaseTurtle_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_GetResult_Request * data = NULL;

  if (size) {
    data = (lab02__action__ChaseTurtle_GetResult_Request *)allocator.zero_allocate(size, sizeof(lab02__action__ChaseTurtle_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lab02__action__ChaseTurtle_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lab02__action__ChaseTurtle_GetResult_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
lab02__action__ChaseTurtle_GetResult_Request__Sequence__fini(lab02__action__ChaseTurtle_GetResult_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      lab02__action__ChaseTurtle_GetResult_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

lab02__action__ChaseTurtle_GetResult_Request__Sequence *
lab02__action__ChaseTurtle_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_GetResult_Request__Sequence * array = (lab02__action__ChaseTurtle_GetResult_Request__Sequence *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lab02__action__ChaseTurtle_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lab02__action__ChaseTurtle_GetResult_Request__Sequence__destroy(lab02__action__ChaseTurtle_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lab02__action__ChaseTurtle_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lab02__action__ChaseTurtle_GetResult_Request__Sequence__are_equal(const lab02__action__ChaseTurtle_GetResult_Request__Sequence * lhs, const lab02__action__ChaseTurtle_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lab02__action__ChaseTurtle_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lab02__action__ChaseTurtle_GetResult_Request__Sequence__copy(
  const lab02__action__ChaseTurtle_GetResult_Request__Sequence * input,
  lab02__action__ChaseTurtle_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lab02__action__ChaseTurtle_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lab02__action__ChaseTurtle_GetResult_Request * data =
      (lab02__action__ChaseTurtle_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lab02__action__ChaseTurtle_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lab02__action__ChaseTurtle_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lab02__action__ChaseTurtle_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "lab02/action/detail/chase_turtle__functions.h"

bool
lab02__action__ChaseTurtle_GetResult_Response__init(lab02__action__ChaseTurtle_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!lab02__action__ChaseTurtle_Result__init(&msg->result)) {
    lab02__action__ChaseTurtle_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
lab02__action__ChaseTurtle_GetResult_Response__fini(lab02__action__ChaseTurtle_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  lab02__action__ChaseTurtle_Result__fini(&msg->result);
}

bool
lab02__action__ChaseTurtle_GetResult_Response__are_equal(const lab02__action__ChaseTurtle_GetResult_Response * lhs, const lab02__action__ChaseTurtle_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!lab02__action__ChaseTurtle_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
lab02__action__ChaseTurtle_GetResult_Response__copy(
  const lab02__action__ChaseTurtle_GetResult_Response * input,
  lab02__action__ChaseTurtle_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!lab02__action__ChaseTurtle_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

lab02__action__ChaseTurtle_GetResult_Response *
lab02__action__ChaseTurtle_GetResult_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_GetResult_Response * msg = (lab02__action__ChaseTurtle_GetResult_Response *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lab02__action__ChaseTurtle_GetResult_Response));
  bool success = lab02__action__ChaseTurtle_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lab02__action__ChaseTurtle_GetResult_Response__destroy(lab02__action__ChaseTurtle_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lab02__action__ChaseTurtle_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lab02__action__ChaseTurtle_GetResult_Response__Sequence__init(lab02__action__ChaseTurtle_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_GetResult_Response * data = NULL;

  if (size) {
    data = (lab02__action__ChaseTurtle_GetResult_Response *)allocator.zero_allocate(size, sizeof(lab02__action__ChaseTurtle_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lab02__action__ChaseTurtle_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lab02__action__ChaseTurtle_GetResult_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
lab02__action__ChaseTurtle_GetResult_Response__Sequence__fini(lab02__action__ChaseTurtle_GetResult_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      lab02__action__ChaseTurtle_GetResult_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

lab02__action__ChaseTurtle_GetResult_Response__Sequence *
lab02__action__ChaseTurtle_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_GetResult_Response__Sequence * array = (lab02__action__ChaseTurtle_GetResult_Response__Sequence *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lab02__action__ChaseTurtle_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lab02__action__ChaseTurtle_GetResult_Response__Sequence__destroy(lab02__action__ChaseTurtle_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lab02__action__ChaseTurtle_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lab02__action__ChaseTurtle_GetResult_Response__Sequence__are_equal(const lab02__action__ChaseTurtle_GetResult_Response__Sequence * lhs, const lab02__action__ChaseTurtle_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lab02__action__ChaseTurtle_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lab02__action__ChaseTurtle_GetResult_Response__Sequence__copy(
  const lab02__action__ChaseTurtle_GetResult_Response__Sequence * input,
  lab02__action__ChaseTurtle_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lab02__action__ChaseTurtle_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lab02__action__ChaseTurtle_GetResult_Response * data =
      (lab02__action__ChaseTurtle_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lab02__action__ChaseTurtle_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lab02__action__ChaseTurtle_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lab02__action__ChaseTurtle_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "lab02/action/detail/chase_turtle__functions.h"

bool
lab02__action__ChaseTurtle_FeedbackMessage__init(lab02__action__ChaseTurtle_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    lab02__action__ChaseTurtle_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!lab02__action__ChaseTurtle_Feedback__init(&msg->feedback)) {
    lab02__action__ChaseTurtle_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
lab02__action__ChaseTurtle_FeedbackMessage__fini(lab02__action__ChaseTurtle_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  lab02__action__ChaseTurtle_Feedback__fini(&msg->feedback);
}

bool
lab02__action__ChaseTurtle_FeedbackMessage__are_equal(const lab02__action__ChaseTurtle_FeedbackMessage * lhs, const lab02__action__ChaseTurtle_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!lab02__action__ChaseTurtle_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
lab02__action__ChaseTurtle_FeedbackMessage__copy(
  const lab02__action__ChaseTurtle_FeedbackMessage * input,
  lab02__action__ChaseTurtle_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!lab02__action__ChaseTurtle_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

lab02__action__ChaseTurtle_FeedbackMessage *
lab02__action__ChaseTurtle_FeedbackMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_FeedbackMessage * msg = (lab02__action__ChaseTurtle_FeedbackMessage *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(lab02__action__ChaseTurtle_FeedbackMessage));
  bool success = lab02__action__ChaseTurtle_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
lab02__action__ChaseTurtle_FeedbackMessage__destroy(lab02__action__ChaseTurtle_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    lab02__action__ChaseTurtle_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
lab02__action__ChaseTurtle_FeedbackMessage__Sequence__init(lab02__action__ChaseTurtle_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_FeedbackMessage * data = NULL;

  if (size) {
    data = (lab02__action__ChaseTurtle_FeedbackMessage *)allocator.zero_allocate(size, sizeof(lab02__action__ChaseTurtle_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = lab02__action__ChaseTurtle_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        lab02__action__ChaseTurtle_FeedbackMessage__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
lab02__action__ChaseTurtle_FeedbackMessage__Sequence__fini(lab02__action__ChaseTurtle_FeedbackMessage__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      lab02__action__ChaseTurtle_FeedbackMessage__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

lab02__action__ChaseTurtle_FeedbackMessage__Sequence *
lab02__action__ChaseTurtle_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  lab02__action__ChaseTurtle_FeedbackMessage__Sequence * array = (lab02__action__ChaseTurtle_FeedbackMessage__Sequence *)allocator.allocate(sizeof(lab02__action__ChaseTurtle_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = lab02__action__ChaseTurtle_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
lab02__action__ChaseTurtle_FeedbackMessage__Sequence__destroy(lab02__action__ChaseTurtle_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    lab02__action__ChaseTurtle_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
lab02__action__ChaseTurtle_FeedbackMessage__Sequence__are_equal(const lab02__action__ChaseTurtle_FeedbackMessage__Sequence * lhs, const lab02__action__ChaseTurtle_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!lab02__action__ChaseTurtle_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
lab02__action__ChaseTurtle_FeedbackMessage__Sequence__copy(
  const lab02__action__ChaseTurtle_FeedbackMessage__Sequence * input,
  lab02__action__ChaseTurtle_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(lab02__action__ChaseTurtle_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    lab02__action__ChaseTurtle_FeedbackMessage * data =
      (lab02__action__ChaseTurtle_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!lab02__action__ChaseTurtle_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          lab02__action__ChaseTurtle_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!lab02__action__ChaseTurtle_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
