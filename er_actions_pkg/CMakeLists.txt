cmake_minimum_required(VERSION 3.0.2)
project(er_actions_pkg)

find_package(catkin REQUIRED COMPONENTS
  rospy
  actionlib
  actionlib_msgs
  std_msgs
  message_generation
)

add_action_files(
  DIRECTORY action
  FILES
  DroneActionER.action
)

generate_messages(
  DEPENDENCIES
  actionlib_msgs
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy actionlib actionlib_msgs std_msgs message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  src/drone_action_server.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
