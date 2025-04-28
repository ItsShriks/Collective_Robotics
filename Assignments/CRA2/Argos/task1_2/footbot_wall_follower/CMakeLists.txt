include_directories(/usr/include/lua5.2)
link_directories(/usr/lib/argos3)

# Add the new wall-following robot library
add_library(footbot_wall_following MODULE footbot_wall_following.h footbot_wall_following.cpp)

# Link the necessary ARGoS libraries for the wall-following robot
target_link_libraries(footbot_wall_following
  argos3core_simulator
  argos3plugin_simulator_footbot
  argos3plugin_simulator_genericrobot)
