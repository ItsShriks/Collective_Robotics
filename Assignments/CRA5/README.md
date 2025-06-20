# Collective Robotics – Task Sheet 5

**Course:** Collective Robotics – Summer Semester 2025
**Instructor:** Prof. Dr. Javad Ghofrani
**Students:** Trushar Ghanekar, Shrikar Nakhye
**Submission:** Task Sheet 5 – Collective Decision-Making

---

## 📄 Overview

This repository contains solutions to **Task Sheet 5**, focusing on **collective decision-making** in swarm systems using the **urn model**, **global switching dynamics**, and a **foraging controller** for robot swarms. The simulations aim to replicate behavior observed in locust swarms and analyze how density, feedback, and swarm size influence emergent behaviors.

---

## 📁 File Structure
```
/Assignments/CRA5
├── task1_simulate_dL.py         # Task 1: Empirical measurement of ΔL(L)
├── task1_fit_urn_model.py       # Task 1: Curve fitting of Δs(s) and PFB(s)
├── task2_global_switching.py    # Task 2: Global switching simulation vs swarm size
├── task3_forage_controller.py   # Task 3: Robot foraging behavior (spec template)
├── output/                      # Contains all output plots and ΔL(L) data file
│   ├── task1_1_plot.png         # ΔL(L) vs L plot
│   ├── task1_2_plot.png         # Fitted urn model Δs(s) vs s
│   ├── task1_3_plot.png         # PFB(s) vs s plot
│   ├── task2_1_plot.png         # Switch time vs swarm size
│   ├── task2_2_plot.png         # Number of switches vs swarm size
│   └── L_of_L.txt               # Raw data for ΔL(L)
├── README.md                    # You are here!
```
---

## ✅ Task 1: Urn Model for Locust Scenario

### 🔹 task1_simulate_dL.py

- Simulates a ring of \( N = 50 \) locusts over 50,000 runs.
- After a 100-timestep warm-up, it measures ΔL = \( L_t - L_{t-1} \) over 20 steps.
- Stores average ΔL as a function of L (number of left-goers).
- Output:
  - Raw data: `output/L_of_L.txt`
  - Plot: `output/task1_1_plot.png`

### 🔹 task1_fit_urn_model.py

- Fits the theoretical urn model to the ΔL data.
- Computes:
  - Fraction of left-goers \( s = L/N \)
  - Δs(s) from ΔL/N
  - Fits:
    \[
    \Delta s(s) = 4c \cdot (\phi \sin(\pi s) - 0.5)(s - 0.5)
    \]
- Extracts fitted φ and c using curve fitting.
- Outputs:
  - Δs(s) plot with fit: `task1_2_plot.png`
  - PFB(s) curve: `task1_3_plot.png`

---

## ✅ Task 2: Density-Dependent Global Switching

### 🔹 task2_global_switching.py

- Simulates global switching over swarm sizes \( N = 20 \) to \( 150 \).
- Identifies zone transitions (A → B → C or C → B → A) using thresholds:
  - Zone A: \( L > 0.7N \)
  - Zone B: \( 0.3N \leq L \leq 0.7N \)
  - Zone C: \( L < 0.3N \)
- For each N, records:
  - Number of switches
  - Average switch duration
- Outputs:
  - `task2_1_plot.png`
  - `task2_2_plot.png`

---

## ⚠️ Task 3: Foraging Behavior (Prototype)

### 🔹 task3_forage_controller.py

- Initial template controller for a swarm robot foraging task.
- Design includes:
  - Proximity + bumper + light sensor input
  - Motor commands and boolean outputs for behavior flags
- Future versions to measure performance over different swarm sizes \( N \in \{1, \dots, 10\} \).

---

## 📊 Output Plots

All plots and simulations are saved in the `/output/` folder in `.png` and `.mp4` format for inclusion in documentation or reports.

---

## ▶️ How to Run

```bash
# Task 1: Empirical ΔL and model fitting
python task1_simulate_dL.py
python task1_fit_urn_model.py

# Task 2: Global switching vs swarm size
python task2_global_switching.py
```
# Task 3: Foraging controller (in development)
<!-- python task3_forage_controller.py -->
```bash
cd Assignments/CRA5/src/task_3/src
```
For Simulation
```bash
python main.py

For Plot
```bash
python swarm_performance.py
