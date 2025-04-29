#ifndef VACUUM_LOOP_FUNCTIONS_H
#define VACUUM_LOOP_FUNCTIONS_H

#include <argos3/core/simulator/loop_functions.h>
#include <vector>

using namespace argos;

class CVacuumLoopFunctions : public CLoopFunctions {

public:
    CVacuumLoopFunctions();
    virtual ~CVacuumLoopFunctions() {}

    virtual void Init(TConfigurationNode& t_tree);
    virtual void Reset();
    virtual void Destroy() {}

    virtual void PreStep();
    virtual void PostStep();

    /* Drawing on the floor */
    virtual CColor GetFloorColor(const CVector2& c_position_on_plane);

private:
    UInt32 m_unMapSizeX;
    UInt32 m_unMapSizeY;
    Real m_fCellSize;
    std::vector<bool> m_vecVisited;
};

#endif
