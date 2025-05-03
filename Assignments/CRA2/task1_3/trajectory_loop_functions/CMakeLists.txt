include_directories(/usr/include/lua5.2)
link_directories(/usr/lib/argos3)
find_package(Qt5 REQUIRED COMPONENTS Widgets OpenGL)

include_directories(${Qt5Widgets_INCLUDE_DIRS} ${Qt5OpenGL_INCLUDE_DIRS})
add_definitions(${Qt5Widgets_DEFINITIONS} ${Qt5OpenGL_DEFINITIONS})

include_directories(${ARGOS_QTOPENGL_INCLUDE_DIRS})
add_library(trajectory_loop_functions MODULE 
  trajectory_loop_functions.h
  trajectory_qtuser_functions.h
  trajectory_loop_functions.cpp
  trajectory_qtuser_functions.cpp)

add_library(footbot_diffusion MODULE footbot_diffusion.h footbot_diffusion.cpp)
target_link_libraries(footbot_diffusion
  argos3core_simulator
  argos3plugin_simulator_footbot
  argos3plugin_simulator_genericrobot)

  target_link_libraries(trajectory_loop_functions
  argos3core_simulator
  argos3plugin_simulator_entities
  argos3plugin_simulator_footbot
  argos3plugin_simulator_qtopengl
  ${ARGOS_QTOPENGL_LIBRARIES}
  Qt5::Widgets
  Qt5::OpenGL
)
