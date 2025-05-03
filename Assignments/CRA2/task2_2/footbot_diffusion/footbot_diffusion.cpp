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
   
   GetNodeAttributeOrDefault(t_node, "wait_steps", m_unWaitSteps, static_cast<UInt32>(10));

   m_cGoStraightAngleRange.Set(-ToRadians(m_cAlpha), ToRadians(m_cAlpha));
}

void CFootBotDiffusion::ControlStep() {
   const CCI_FootBotProximitySensor::TReadings& tProxReads = m_pcProximity->GetReadings();

   if (m_eState == STATE_WAITING) {
      if (m_unCurrentWait < m_unWaitSteps) {
         ++m_unCurrentWait;
         // Move backward to avoid another robot
         m_pcWheels->SetLinearVelocity(-m_fWheelVelocity * 0.5f, -m_fWheelVelocity * 0.5f);
         return;
      } else {
         m_eState = STATE_MOVING;
         m_unCurrentWait = 0;
      }
   }

   // Detect robot in front
   if (IsRobotInFront()) {
      m_eState = STATE_WAITING;
      m_unCurrentWait = 0;
      return;
   }

   // Calculate direction vector
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
}

bool CFootBotDiffusion::IsRobotInFront() {
   const CCI_FootBotProximitySensor::TReadings& tProxReads = m_pcProximity->GetReadings();

   for (const auto& reading : tProxReads) {
      // Only consider proximity directly in front (e.g., -15° to +15°)
      if (Abs(reading.Angle.GetValue()) < ToRadians(CDegrees(15)).GetValue() &&
          reading.Value > m_fDelta) {
         return true;
      }
   }
   return false;
}
REGISTER_CONTROLLER(CFootBotDiffusion, "footbot_diffusion_controller")
