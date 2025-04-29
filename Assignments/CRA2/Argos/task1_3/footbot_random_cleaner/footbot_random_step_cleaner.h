#ifndef FOOTBOT_RANDOM_STEP_CLEANER_H
#define FOOTBOT_RANDOM_STEP_CLEANER_H

#include <argos3/core/control_interface/ci_controller.h>
#include <argos3/plugins/robots/generic/control_interface/ci_differential_steering_actuator.h>
#include <argos3/plugins/robots/foot-bot/control_interface/ci_footbot_proximity_sensor.h>
#include <argos3/core/utility/math/rng.h>

using namespace argos;

class CFootBotRandomStepCleaner : public CCI_Controller {

public:
    CFootBotRandomStepCleaner();
    virtual ~CFootBotRandomStepCleaner() {}

    virtual void Init(TConfigurationNode& t_node);
    virtual void ControlStep();
    virtual void Reset() {}
    virtual void Destroy() {}

private:
    CCI_DifferentialSteeringActuator* m_pcWheels;
    CCI_FootBotProximitySensor* m_pcProximity;
    CRandom::CRNG* m_pcRNG;

    Real m_fWheelVelocity;
    UInt32 m_unTurnSteps;
    UInt32 m_unTurnCounter;
    SInt8 m_nTurnDirection; // -1 = left, 1 = right
};

#endif
