#include "footbot_random_step_cleaner.h"
#include <argos3/core/utility/logging/argos_log.h>
#include <algorithm>

CFootBotRandomStepCleaner::CFootBotRandomStepCleaner() :
   m_pcWheels(nullptr),
   m_pcProximity(nullptr),
   m_pcRNG(nullptr),
   m_fWheelVelocity(5.0f),
   m_unTurnSteps(10),
   m_unTurnCounter(0),
   m_nTurnDirection(0) {}

void CFootBotRandomStepCleaner::Init(TConfigurationNode& t_node) {
   m_pcWheels = GetActuator<CCI_DifferentialSteeringActuator>("differential_steering");
   m_pcProximity = GetSensor<CCI_FootBotProximitySensor>("footbot_proximity");
   m_pcRNG = CRandom::CreateRNG("argos");

   GetNodeAttributeOrDefault(t_node, "velocity", m_fWheelVelocity, m_fWheelVelocity);
   GetNodeAttributeOrDefault(t_node, "turn_steps", m_unTurnSteps, m_unTurnSteps);
}

void CFootBotRandomStepCleaner::ControlStep() {
   const CCI_FootBotProximitySensor::TReadings& tReadings = m_pcProximity->GetReadings();

   Real fMaxReading = 0.0f;
   SInt8 nMaxIndex = -1;

   for (size_t i = 0; i < tReadings.size(); ++i) {
      if (tReadings[i].Value > fMaxReading) {
         fMaxReading = tReadings[i].Value;
         nMaxIndex = i;
      }
   }

   if (fMaxReading > 0.2f && m_unTurnCounter == 0) {
      // Determine turn direction based on sensor position
      Real fAngle = tReadings[nMaxIndex].Angle.GetValue();
      m_nTurnDirection = (fAngle > 0) ? -1 : 1; // Turn opposite to obstacle

      m_unTurnCounter = m_unTurnSteps;

      // Set turning velocity: rotate in place
      m_pcWheels->SetLinearVelocity(
         m_nTurnDirection * m_fWheelVelocity,
        -m_nTurnDirection * m_fWheelVelocity
      );
   }
   else if (m_unTurnCounter > 0) {
      // Keep turning
      --m_unTurnCounter;
      m_pcWheels->SetLinearVelocity(
         m_nTurnDirection * m_fWheelVelocity,
        -m_nTurnDirection * m_fWheelVelocity
      );
   }
   else {
      // Move forward
      m_pcWheels->SetLinearVelocity(m_fWheelVelocity, m_fWheelVelocity);
   }
}
