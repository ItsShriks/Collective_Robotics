#ifndef FOOTBOT_DIFFUSION_H
#define FOOTBOT_DIFFUSION_H

/* Base controller interface */
#include <argos3/core/control_interface/ci_controller.h>

/* Actuator: differential steering for movement */
#include <argos3/plugins/robots/generic/control_interface/ci_differential_steering_actuator.h>

/* Sensor: proximity detection */
#include <argos3/plugins/robots/foot-bot/control_interface/ci_footbot_proximity_sensor.h>

using namespace argos;

/* This class implements the diffusion behavior for the foot-bot */
class CFootBotDiffusion : public CCI_Controller {

public:

   /* Constructor */
   CFootBotDiffusion();

   /* Destructor */
   virtual ~CFootBotDiffusion() {}

   /* Called once at initialization */
   virtual void Init(TConfigurationNode& t_node);

   /* Called every time step of the simulation */
   virtual void ControlStep();

   /* Reset controller state (optional) */
   virtual void Reset() {}

   /* Clean up controller (optional) */
   virtual void Destroy() {}

private:

   /* Handle to wheel actuator */
   CCI_DifferentialSteeringActuator* m_pcWheels;

   /* Handle to proximity sensor */
   CCI_FootBotProximitySensor* m_pcProximity;

   /* === Behavior Parameters (can be set in XML) === */

   /* Angle range in which robot will keep moving forward */
   CDegrees m_cAlpha;

   /* Distance threshold to consider obstacle as close */
   Real m_fDelta;

   /* Linear speed of wheels */
   Real m_fWheelVelocity;

   /* Angular range object for easy comparison */
   CRange<CRadians> m_cGoStraightAngleRange;
};

#endif
