Here's the `README.md` content formatted properly in Markdown. You can copy and paste this into a file named `README.md`:

````markdown
# Behavior-Based Robotics and Collective Behaviors – Simulation Tasks

This project contains a series of robotics tasks implemented using the **ARGoS** simulator, focusing on behavior-based control for both **individual robots** and **robot swarms**.

---

## 📁 Directory Structure & Tasks Mapping

| Folder       | Task Description                                                                 |
|--------------|----------------------------------------------------------------------------------|
| `task1_1`    | **(2.A)** Collision avoidance for a single robot                                 |
| `task1_2`    | **(2.B)** Wall-following robot behavior                                           |
| `task1_3`    | **(2.C)** Vacuum cleaning strategy behavior                                       |
| `task2_1`    | **(3.A)** Robots stop upon close contact with another robot                       |
| `task2_2`    | **(3.B & 3.C)** Robots resume after delay, forming dynamic aggregates             |

> _Each folder contains its own ARGoS simulation with its own build instructions._

---

## 🔧 Build & Run Instructions (For Every Task Folder)

Each task is self-contained in its own directory. To build and run a task, follow these steps from inside the specific task folder (e.g., `cd task1_1`):

```bash
mkdir build
cd build
cmake ..
make
````

Then, to run the ARGoS simulation:

```bash
argos3 -c task1_1\task1_1.argos
```



---

## 🎯 Task Objectives

### Task 1: Single-Robot Behaviors

These tasks use a single robot in a rectangular, wall-bounded environment.

* **Task 1\_1 (2.A)**: Collision Avoidance
  A robot roams around while avoiding obstacles and walls using sensors.

* **Task 1\_2 (2.B)**: Wall-Following
  Robot follows the wall boundaries without making physical contact.

* **Task 1\_3 (2.C)**: Vacuum Cleaner Strategy
  Designed to cover most of the arena space efficiently, simulating a cleaning robot.

---

### Task 2: Multi-Robot Swarm Behaviors

All robots share the same control logic and are randomly distributed at simulation start.

* **Task 2\_1 (3.A)**: Proximity Stop
  Robots stop when another robot is too close. This uses simulated inter-robot distance sensing.

* **Task 2\_2 (3.B & 3.C)**: Aggregation Behavior
  Adds a timeout before robots resume movement, encouraging swarm clustering with occasional movement to avoid stagnation.

---

## 🧰 Simulator

All tasks are built using the [ARGoS simulator](http://www.argos-sim.info/). Make sure ARGoS is properly installed on your system before building or running these tasks.

---

## ✅ Status Tracker

| Task Folder | Status |
| ----------- | ------ |
| task1\_1    | ✅ Done |
| task1\_2    | ✅ Done |
| task1\_3    | ✅ Done |
| task2\_1    | ✅ Done |
| task2\_2    | ✅ Done |

---

## 📌 Notes

* Each behavior was implemented with modular and clean design in mind.
* Parameters such as distance thresholds and waiting time can be tuned in the source code or `.argos` files for better performance or experimentation.

```

Let me know if you'd like me to save this as a downloadable file or generate separate README files for each task folder.
```
