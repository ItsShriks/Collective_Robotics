# Collaborative Robotics Sheet 3 – Ghanekar Nakhye

📌 **Overview**

This project addresses Task Sheet 3 of the **Collective Robotics** course for the Summer Semester 2025 of MAS, under the supervision of **Prof. Dr. Javad Ghofrani**.

### 🧠 Objectives:
A. Implement a **Buffon’s needle** simulator  
B. Boost a **robot swarm aggregation behavior** with so-called **anti-agents**  
C. **Measure performance** in a swarm simulation

---

## ⚙️ Requirements

Make sure the following dependencies are installed:

- Python 3.8+
- `matplotlib`
- `networkx`
- `numpy`

You can install the Python packages using pip:

```bash
pip3 install matplotlib networkx numpy
```

Or create a new conda environment using the provided environment.yml file:

```bash
conda env create -f src/environment.yml
```

---

## ▶️ Running the Code

Use the following commands to run each subtask:

### Subtask 1: Buffon's Needle (Notebook)

```bash
jupyter nb/CRA3.ipynb
```

The notebook contains the Buffon’s needle simulator and related plots.

---

### Subtask 2: Anti-Agents in Swarm Aggregation

```bash
python3 src/task2_a.py    # For Object Clustering with Anti-agents
python3 src/task2_b.py    # For Swarm Aggregation with Messaging Anti-agents
python3 src/task2_c.py    # For Testing Different Anti-agent Percentages
```

Each script will generate and save relevant plots and output statistics to:

```bash
output/
```

---

## 🧪 Tested On

### macOS 

* MacBook Air A2337 - macOS Sonoma - 14.1.1 (23B81)/15.4 (24E248)
* Memory: 8GB
* Python 3.12.0
* Xcode - xcode-select version 2403

### Linux 🐧

* ASUS Vivobook - Ubuntu 22.04.3 LTS
* Memory: 16GB
* CPU: Intel Core i7-1165G7 @ 2.80GHz
* GPU: NVIDIA GeForce 1080Ti
* Python 3.12.0

---

## 👥 Contributors

* [Trushar Ghanekar](https://github.com/Trushar2411)
* [Shrikar Nakhye](https://github.com/ItsShriks)

---

## 🙏 Acknowledgements

* [Prof. Dr. Javad Ghofrani](https://www.h-brs.de/de/inf/prof-dr-javad-ghofrani)
* [Youssef Mahmoud Youssef](https://www.h-brs.de/de/inf/youssef-mahmoud-youssef)
* [Hochschule Bonn-Rhein-Sieg](https://www.h-brs.de/de)


