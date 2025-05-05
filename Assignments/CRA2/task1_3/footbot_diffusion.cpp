/* Include the controller definition */
#include "footbot_diffusion.h"

/* Function definitions for XML parsing */
#include <argos3/core/utility/configuration/argos_configuration.h>

/* 2D vector definition */
#include <argos3/core/utility/math/vector2.h>

/****************************************/
/****************************************/

/* Constructor: initialize default values */
CFootBotDiffusion::CFootBotDiffusion() :
   m_pcWheels(NULL),
   m_pcProximity(NULL),
   m_cAlpha(10.0f),
   m_fDelta(0.5f),
   m_fWheelVelocity(20.0f),
   m_cGoStraightAngleRange(-ToRadians(m_cAlpha), ToRadians(m_cAlpha)) {}

/****************************************/
/****************************************/

/* Initialization function: called once at the beginning */
void CFootBotDiffusion::Init(TConfigurationNode& t_node) {
   /*
    * Get actuator and sensor handles from ARGoS using identifiers from XML
    */
   m_pcWheels    = GetActuator<CCI_DifferentialSteeringActuator>("differential_steering");
   m_pcProximity = GetSensor  <CCI_FootBotProximitySensor      >("footbot_proximity");

   /*
    * Read parameters from XML, or use defaults
    * - alpha: angle tolerance to go straight
    * - delta: distance threshold to go straight
    * - velocity: wheel speed
    */
   GetNodeAttributeOrDefault(t_node, "alpha", m_cAlpha, m_cAlpha);
   m_cGoStraightAngleRange.Set(-ToRadians(m_cAlpha), ToRadians(m_cAlpha));
   GetNodeAttributeOrDefault(t_node, "delta", m_fDelta, m_fDelta);
   GetNodeAttributeOrDefault(t_node, "velocity", m_fWheelVelocity, m_fWheelVelocity);
}

/****************************************/
/****************************************/

/* This function is called at every simulation step */
void CFootBotDiffusion::ControlStep() {
   /* Get proximity sensor readings */
   const CCI_FootBotProximitySensor::TReadings& tProxReads = m_pcProximity->GetReadings();

   /* Sum all readings to create an average direction vector */
   CVector2 cAccumulator;
   for(size_t i = 0; i < tProxReads.size(); ++i) {
      cAccumulator += CVector2(tProxReads[i].Value, tProxReads[i].Angle);
   }
   cAccumulator /= tProxReads.size();  // Normalize vector by total readings

   /* Get the direction (angle) of the accumulated vector */
   CRadians cAngle = cAccumulator.Angle();

   /*
    * Decision making:
    * If the vector is within the tolerance angle AND obstacle is far,
    * keep going straight.
    * Else, turn in the opposite direction of the obstacle.
    */
   if(m_cGoStraightAngleRange.WithinMinBoundIncludedMaxBoundIncluded(cAngle) &&
      cAccumulator.Length() < m_fDelta ) {
      /* Move forward */
      m_pcWheels->SetLinearVelocity(m_fWheelVelocity, m_fWheelVelocity);
   }
   else {
      /* Turn in place to avoid obstacle */
      if(cAngle.GetValue() > 0.0f) {
         m_pcWheels->SetLinearVelocity(m_fWheelVelocity, 0.0f); // Turn left
      }
      else {
         m_pcWheels->SetLinearVelocity(0.0f, m_fWheelVelocity); // Turn right
      }
   }
}

/****************************************/
/****************************************/

/* Register this controller with ARGoS under the given tag */
REGISTER_CONTROLLER(CFootBotDiffusion, "footbot_diffusion_controller")
