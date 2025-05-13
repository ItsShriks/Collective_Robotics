/* Include the controller definition */
#include "footbot_diffusion.h"

/* Function definitions for XML parsing */
#include <argos3/core/utility/configuration/argos_configuration.h>

/* 2D vector definition */
#include <argos3/core/utility/math/vector2.h>

/****************************************/
/****************************************/

CFootBotDiffusion::CFootBotDiffusion() :
   m_pcWheels(NULL),
   m_pcProximity(NULL),
   m_cAlpha(10.0f),
   m_fDelta(0.5f),
   m_fWheelVelocity(1.5f),
   m_cGoStraightAngleRange(-ToRadians(m_cAlpha),
                           ToRadians(m_cAlpha)) {}

/****************************************/
/****************************************/

void CFootBotDiffusion::Init(TConfigurationNode& t_node) {
   /*
    * Get sensor/actuator handles
    */
   m_pcWheels    = GetActuator<CCI_DifferentialSteeringActuator>("differential_steering");
   m_pcProximity = GetSensor  <CCI_FootBotProximitySensor      >("footbot_proximity");

   /*
    * Parse configuration file attributes
    */
   GetNodeAttributeOrDefault(t_node, "alpha", m_cAlpha, m_cAlpha);
   m_cGoStraightAngleRange.Set(-ToRadians(m_cAlpha), ToRadians(m_cAlpha));
   GetNodeAttributeOrDefault(t_node, "delta", m_fDelta, m_fDelta);
   GetNodeAttributeOrDefault(t_node, "velocity", m_fWheelVelocity, m_fWheelVelocity);
}

/****************************************/
/****************************************/

void CFootBotDiffusion::ControlStep() {
   /* Get proximity sensor readings */
   const CCI_FootBotProximitySensor::TReadings& tProxReads = m_pcProximity->GetReadings();

   /* Check if any reading exceeds the threshold */
   bool bObstacleDetected = false;
   for(const auto& tReading : tProxReads) {
      if(tReading.Value > m_fDelta) {
         bObstacleDetected = true;
         break;
      }
   }

   if(bObstacleDetected) {
      /* Stop if anything is detected */
      m_pcWheels->SetLinearVelocity(0.0f, 0.0f);
   }
   else {
      /* Otherwise, move forward */
      m_pcWheels->SetLinearVelocity(m_fWheelVelocity, m_fWheelVelocity);
   }
}

/****************************************/
/****************************************/

/*
 * Register the controller with ARGoS
 */
REGISTER_CONTROLLER(CFootBotDiffusion, "footbot_diffusion_controller")
