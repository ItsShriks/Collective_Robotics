#include "footbot_diffusion.h"
#include <argos3/core/utility/math/vector2.h>
#include <argos3/core/utility/configuration/argos_configuration.h>

CFootBotDiffusion::CFootBotDiffusion() :
   m_pcWheels(nullptr),
   m_pcProximity(nullptr),
   m_fWheelVelocity(5.0),
   m_unWaitSteps(10),
   m_unCurrentWait(0),
   m_eState(STATE_MOVING) {}

void CFootBotDiffusion::Init(TConfigurationNode& t_node) {
   m_pcWheels = GetActuator<CCI_DifferentialSteeringActuator>("differential_steering");
   m_pcProximity = GetSensor<CCI_FootBotProximitySensor>("footbot_proximity");

   GetNodeAttributeOrDefault(t_node, "alpha", m_cAlpha, CDegrees(10.0));
   GetNodeAttributeOrDefault(t_node, "delta", m_fDelta, 0.1);
   GetNodeAttributeOrDefault(t_node, "velocity", m_fWheelVelocity, 5.0);
   GetNodeAttributeOrDefault(t_node, "wait_steps", m_unWaitSteps, static_cast<UInt32>(20));

   m_cGoStraightAngleRange.Set(-ToRadians(m_cAlpha), ToRadians(m_cAlpha));
}

void CFootBotDiffusion::ControlStep() {
   const CCI_FootBotProximitySensor::TReadings& tProxReads = m_pcProximity->GetReadings();

   switch (m_eState) {
      case STATE_WAITING:
         if (m_unCurrentWait < m_unWaitSteps) {
            ++m_unCurrentWait;
            m_pcWheels->SetLinearVelocity(0.0f, 0.0f);
         } else {
            m_eState = STATE_TURNING;
            m_unCurrentWait = 0;
         }
         return;

      case STATE_TURNING:
         if (m_unCurrentWait < m_unWaitSteps) {
            ++m_unCurrentWait;
            m_pcWheels->SetLinearVelocity(m_fWheelVelocity, -m_fWheelVelocity);
         } else {
            m_eState = STATE_ESCAPE_FORWARD;
            m_unCurrentWait = 0;
         }
         return;

      case STATE_ESCAPE_FORWARD:
         if (m_unCurrentWait < m_unWaitSteps) {
            ++m_unCurrentWait;
            m_pcWheels->SetLinearVelocity(m_fWheelVelocity, m_fWheelVelocity);
         } else {
            m_eState = STATE_MOVING;
            m_unCurrentWait = 0;
         }
         return;

      case STATE_MOVING: {
         if (IsObstacleDetected()) {
            m_eState = STATE_WAITING;
            m_unCurrentWait = 0;
            return;
         }

         // Diffusion behavior
         CVector2 cAccumulator;
         for (const auto& reading : tProxReads) {
            cAccumulator += CVector2(reading.Value, reading.Angle);
         }

         CRadians cAngle = cAccumulator.Angle();

         if (m_cGoStraightAngleRange.WithinMinBoundIncludedMaxBoundIncluded(cAngle) &&
             cAccumulator.Length() < m_fDelta) {
            m_pcWheels->SetLinearVelocity(m_fWheelVelocity, m_fWheelVelocity);
         } else {
            if (cAngle.GetValue() > 0.0f) {
               m_pcWheels->SetLinearVelocity(m_fWheelVelocity, -m_fWheelVelocity);
            } else {
               m_pcWheels->SetLinearVelocity(-m_fWheelVelocity, m_fWheelVelocity);
            }
         }
         break;
      }
   }
}



bool CFootBotDiffusion::IsObstacleDetected() {
   const CCI_FootBotProximitySensor::TReadings& tProxReads = m_pcProximity->GetReadings();
   for (const auto& reading : tProxReads) {
      if (reading.Value > m_fDelta) {
         return true;
      }
   }
   return false;
}

REGISTER_CONTROLLER(CFootBotDiffusion, "footbot_diffusion_controller")
