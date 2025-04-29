#include "vacuum_loop_functions.h"
#include <argos3/core/simulator/simulator.h>
#include <argos3/core/simulator/entity/controllable_entity.h>
#include <argos3/core/simulator/space/space.h>
#include <argos3/plugins/robots/foot-bot/simulator/footbot_entity.h>

CVacuumLoopFunctions::CVacuumLoopFunctions() :
   m_unMapSizeX(50),
   m_unMapSizeY(50),
   m_fCellSize(0.1f),
   m_vecVisited(m_unMapSizeX * m_unMapSizeY, false) {}

void CVacuumLoopFunctions::Init(TConfigurationNode& t_tree) {
    GetNodeAttributeOrDefault(t_tree, "map_size_x", m_unMapSizeX, m_unMapSizeX);
    GetNodeAttributeOrDefault(t_tree, "map_size_y", m_unMapSizeY, m_unMapSizeY);
    GetNodeAttributeOrDefault(t_tree, "cell_size", m_fCellSize, m_fCellSize);
    m_vecVisited.assign(m_unMapSizeX * m_unMapSizeY, false);
}

void CVacuumLoopFunctions::Reset() {
    m_vecVisited.assign(m_unMapSizeX * m_unMapSizeY, false);
}

void CVacuumLoopFunctions::PreStep() {
    /* Get robot entity */
    CSpace::TMapPerType& tFootBots = CSimulator::GetInstance().GetSpace().GetEntitiesByType("foot-bot");
    for(auto it = tFootBots.begin(); it != tFootBots.end(); ++it) {
        CFootBotEntity* pcFootBot = any_cast<CFootBotEntity*>(it->second);
        CVector3 cPosition = pcFootBot->GetEmbodiedEntity().GetOriginAnchor().Position;

        /* Convert to map coordinates */
        SInt32 nCellX = static_cast<SInt32>((cPosition.GetX() + (m_unMapSizeX * m_fCellSize / 2)) / m_fCellSize);
        SInt32 nCellY = static_cast<SInt32>((cPosition.GetY() + (m_unMapSizeY * m_fCellSize / 2)) / m_fCellSize);

        if(nCellX >= 0 && nCellX < static_cast<SInt32>(m_unMapSizeX) &&
           nCellY >= 0 && nCellY < static_cast<SInt32>(m_unMapSizeY)) {
            m_vecVisited[nCellY * m_unMapSizeX + nCellX] = true;
        }
    }
}

void CVacuumLoopFunctions::PostStep() {
    /* Nothing needed for now */
}

CColor CVacuumLoopFunctions::GetFloorColor(const CVector2& c_position_on_plane) {
    SInt32 nCellX = static_cast<SInt32>((c_position_on_plane.GetX() + (m_unMapSizeX * m_fCellSize / 2)) / m_fCellSize);
    SInt32 nCellY = static_cast<SInt32>((c_position_on_plane.GetY() + (m_unMapSizeY * m_fCellSize / 2)) / m_fCellSize);

    if(nCellX >= 0 && nCellX < static_cast<SInt32>(m_unMapSizeX) &&
       nCellY >= 0 && nCellY < static_cast<SInt32>(m_unMapSizeY)) {
        if(m_vecVisited[nCellY * m_unMapSizeX + nCellX]) {
            return CColor::WHITE; // Cleaned = White
        }
        else {
            return CColor::GRAY50; // Not cleaned = Gray
        }
    }
    return CColor::GRAY50;
}

/* Register the loop functions with ARGoS */
REGISTER_LOOP_FUNCTIONS(CVacuumLoopFunctions, "vacuum_loop_functions")
