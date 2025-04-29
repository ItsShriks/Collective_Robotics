include_directories(/usr/include/lua5.2)
link_directories(/usr/lib/argos3)

# Add vacuum loop functions
add_library(vacuum_loop_functions MODULE vacuum_loop_functions.h vacuum_loop_functions.cpp)

# Link ARGoS libraries
target_link_libraries(vacuum_loop_functions
  argos3core_simulator
  argos3plugin_simulator_footbot
  argos3plugin_simulator_genericrobot
  argos3plugin_simulator_entities)

