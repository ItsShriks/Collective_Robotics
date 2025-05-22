# Collective Robotics – Task Sheet 4

**Course:** Collective Robotics – Summer Semester 2025  
**Instructor:** Prof. Dr. Javad Ghofrani  
**Student:** [Your Name]  
**Submission:** Task Sheet 4 – Dimension Reduction and Rate Equations

---

## 📄 Overview

This repository contains solutions to **Task Sheet 4**, focusing on **dimension reduction** and **rate equations** in swarm robotics using a locust simulation model and differential equations.

---

## 📁 File Structure

```

task-sheet-4/
├── task\_1\_a.py       # Full simulation of locust behavior
├── task\_1\_b.py       # Transition histogram construction using 1000 runs
├── task\_1\_c.py       # Markov-based model simulation using transition probabilities
├── task\_1\_compare.py # Visualization comparing Task 1a and 1c
├── task\_2\_a.py       # Delay differential equation solution for avoidance model
├── task\_2\_b.py       # Extended model with homing state and two scenarios
├── plots/            # All output plots in PNG/PDF format
├── README.md         # You are here!
└── requirements.txt  # Python dependencies

```

---

## ✅ Task 1: Dimension Reduction and Modeling

### 🔹 Task 1a – Full Locust Simulation

- Simulates N = 20 locusts on a ring (C = 1.0) for 500 time steps.
- Each locust moves left/right and switches direction via local majority or spontaneous change (P = 0.015).
- Plots the number of left-going locusts over time.
- Saved as: `task_1_a.py`

### 🔹 Task 1b – Transition Histogram from Multiple Runs

- Runs 1000 simulations of 500 steps each.
- Builds a 2D histogram `A[i][j]` counting transitions from `Lt → Lt+1`.
- Also records occurrences `M[i]` for normalization.
- Plots a heatmap of transition frequencies.
- Saved as: `task_1_b.py`

### 🔹 Task 1c – Dimension-Reduced Markov Model

- Calculates transition probabilities `P[i][j] = A[i][j] / M[i]`.
- Simulates one trajectory of `L(t)` using the Markov model.
- Plots this trajectory and compares it to Task 1a.
- Saved as: `task_1_c.py`

### 🔹 Comparison Plot (Task 1a vs. 1c)

- Overlap graph: both trajectories plotted on one graph.
- Stacked graph: one above the other for clear visual comparison.
- Saved as: `task_1_compare.py`

---

## ✅ Task 2: Rate Equations and Delays

### 🔹 Task 2a – Searching and Avoiding Model

- Solves the delay equation:
  \[
  \frac{dns}{dt} = -α_r ns(t)(ns(t)+1) + α_r ns(t - τ_a)(ns(t - τ_a)+1)  
  \quad \frac{dm}{dt} = -α_p ns(t)m(t)
  \]
- Parameters: `α_r = 0.6`, `α_p = 0.2`, `τ_a = 2`, `ns(0) = 1`, `m(0) = 1`.
- Uses forward Euler integration with a buffer to handle delay.
- Time: 0 to 50.
- Plots `ns(t)` and `m(t)`.
- Saved as: `task_2_a.py`

### 🔹 Task 2b – Extended Model with Homing Behavior

- Adds `nh(t)` with homing delay `τ_h = 15`.
- Robots move: `searching → homing → searching`.
- Two simulations:
  1. Normal: over `t ∈ (0,160]`.
  2. Disturbed: resets `m(80) = 0.5` at time t=80.
- Plots all three states: `ns(t)`, `m(t)`, and `nh(t)`.
- Saved as: `task_2_b.py`

---

## 📊 Output Plots

All generated plots from the scripts are saved in the `plots/` folder as `.png` and `.pdf` for inclusion in reports.

---

## ▶️ How to Run

### Setup (Python ≥ 3.8 recommended)
```bash
pip install -r requirements.txt
````

### Run Tasks

```bash
python task_1_a.py         # Task 1a simulation
python task_1_b.py         # Task 1b histogram
python task_1_c.py         # Task 1c Markov model
python task_1_compare.py   # Task 1a vs 1c plots

python task_2_a.py         # Task 2a rate equations
python task_2_b.py         # Task 2b homing model
```

---

## 📝 Interpretation Guidelines

* **Task 1**:

  * Observe fluctuations and stabilization patterns in `L(t)`.
  * Compare high-dimensional swarm simulation with simplified Markov predictions.

* **Task 2**:

  * Analyze impact of delay in avoidance behavior on swarm activity.
  * Assess long-term behavior when homing and mid-simulation disturbance is introduced.

---

## 📦 Submission Instructions

* All files are zipped into a single archive as instructed.
* Includes source code, output plots, and this README file.
* Optionally includes a demo/explanation video.

---

*Thank you for reviewing my submission!*


