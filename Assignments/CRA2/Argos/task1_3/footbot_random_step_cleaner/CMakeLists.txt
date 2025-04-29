cmake_minimum_required(VERSION 3.5)
project(footbot_random_cleaner)

# Optional but good practice
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include ARGoS core and plugins
include_directories(
  /usr/include/lua5.2
  ${CMAKE_SOURCE_DIR}
)

link_directories(
  /usr/lib/argos3
)

add_library(footbot_random_step_cleaner MODULE
  footbot_random_step_cleaner.cpp)

target_link_libraries(footbot_random_step_cleaner
  argos3core_simulator
  argos3plugin_simulator_footbot
  argos3plugin_simulator_genericrobot
  argos3plugin_simulator_entities)

