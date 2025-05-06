#include "footbot_wall_following.h"
#include <argos3/core/utility/configuration/argos_configuration.h>
#include <argos3/core/utility/math/vector2.h>

CFootBotWallFollowing::CFootBotWallFollowing() :
   m_pcWheels(NULL),
   m_pcProximity(NULL),
   m_cAlpha(5.0f),
   m_fDelta(0.03f),
   m_fWheelVelocity(20.0f),
   m_cGoStraightAngleRange(-ToRadians(m_cAlpha),
                           ToRadians(m_cAlpha)),
   m_fDesiredDistance(0.2f) {  // Desired distance from the wall (e.g., 10 cm)
}

/****************************************/
/****************************************/

void CFootBotWallFollowing::Init(TConfigurationNode& t_node) {
   /*
    * Get sensor/actuator handles
    */
   m_pcWheels    = GetActuator<CCI_DifferentialSteeringActuator>("differential_steering");
   m_pcProximity = GetSensor  <CCI_FootBotProximitySensor      >("footbot_proximity");
   /*
    * Parse the configuration file for parameters
    */
   GetNodeAttributeOrDefault(t_node, "alpha", m_cAlpha, m_cAlpha);
   m_cGoStraightAngleRange.Set(-ToRadians(m_cAlpha), ToRadians(m_cAlpha));
   GetNodeAttributeOrDefault(t_node, "delta", m_fDelta, m_fDelta);
   GetNodeAttributeOrDefault(t_node, "velocity", m_fWheelVelocity, m_fWheelVelocity);
   GetNodeAttributeOrDefault(t_node, "desired_distance", m_fDesiredDistance, m_fDesiredDistance);
}

/****************************************/
/****************************************/

void CFootBotWallFollowing::ControlStep() {
   /* Get readings from proximity sensor */
   const CCI_FootBotProximitySensor::TReadings& tProxReads = m_pcProximity->GetReadings();

   /* Sum readings and find maximum proximity reading */
   CVector2 cAccumulator;
   Real fMaxReading = 0.0f;
   CRadians cMaxAngle = CRadians::ZERO;

   for(size_t i = 0; i < tProxReads.size(); ++i) {
      cAccumulator += CVector2(tProxReads[i].Value, tProxReads[i].Angle);
      if(tProxReads[i].Value > fMaxReading) {
         fMaxReading = tProxReads[i].Value;
         cMaxAngle = tProxReads[i].Angle;
      }
   }
   cAccumulator /= tProxReads.size();

   /* If no wall detected, go straight */
   if(fMaxReading < 0.1f) {  // Threshold to detect wall
      m_pcWheels->SetLinearVelocity(m_fWheelVelocity, m_fWheelVelocity);
      return;
   }

   /* Wall detected: follow it */

   /* Use only side-facing sensors (e.g., front-right and right) to compute distance to wall */
   Real fDistanceToWall = 0.0f;
   size_t unCount = 0;

   for(const auto& tReading : tProxReads) {
      if(tReading.Angle.GetValue() > -ARGOS_PI / 2 && tReading.Angle.GetValue() < ARGOS_PI / 2) {
         fDistanceToWall += tReading.Value;
         ++unCount;
      }
   }

   if(unCount > 0) {
      fDistanceToWall /= unCount;
   } else {
      fDistanceToWall = 0.0f; // fallback
   }


   /* Calculate the error (difference from desired distance) */
   float fError = fDistanceToWall - m_fDesiredDistance;

   /* Proportional controller */
   float fKp = 10.0f;  // proportional gain
   float fCorrection = fKp * fError;

   /* Adjust wheel speeds based on correction */
   float fLeftWheelSpeed  = m_fWheelVelocity - fCorrection;
   float fRightWheelSpeed = m_fWheelVelocity + fCorrection;

   /* Make sure wheel speeds are non-negative */
   if(fLeftWheelSpeed < 0.0f) fLeftWheelSpeed = 0.0f;
   if(fRightWheelSpeed < 0.0f) fRightWheelSpeed = 0.0f;

   /* Set wheel speeds */
   m_pcWheels->SetLinearVelocity(fLeftWheelSpeed, fRightWheelSpeed);
}

/****************************************/
/****************************************/

/*
 * This statement notifies ARGoS of the existence of the controller.
 */
REGISTER_CONTROLLER(CFootBotWallFollowing, "footbot_wall_following_controller")
