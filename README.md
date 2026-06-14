# 🧩 SudokuAI — AI-Powered Sudoku Solver & Visualizer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?logo=pygame&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![AI](https://img.shields.io/badge/AI-CSP%20%7C%20Backtracking%20%7C%20MRV%20%7C%20AC--3-purple)

> An interactive Sudoku solver that visualizes **four distinct AI algorithms** in real time using a Pygame GUI. Built as a Constraint Satisfaction Problem (CSP) project to compare uninformed vs informed search strategies.

---

## 🎯 Features

- 🎮 **Interactive GUI** — Built with Pygame; watch the AI solve the board step by step
- 🤖 **4 AI Algorithms** — Backtracking, Forward Checking, MRV + AC-3, Simulated Annealing
- 📊 **Live Metrics** — Real-time states explored & backtrack counter
- 🧪 **Benchmark Dashboard** — Compare all algorithms side-by-side
- 🎛️ **Configurable** — Choose algorithm, difficulty, and animation speed at launch
- 🧩 **Puzzle Generator** — Generates valid Sudoku puzzles at 4 difficulty levels

---

## 🛠️ Tech Stack

| Component       | Technology              |
|----------------|-------------------------|
| Language        | Python 3.8+             |
| GUI             | Pygame 2.x              |
| AI Paradigm     | Constraint Satisfaction Problem (CSP) |
| Search Methods  | DFS, Forward Checking, MRV, Simulated Annealing |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/NaumanAhmad2005/SudokuAI_Project.git
cd SudokuAI_Project

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install pygame
```

### Run the App

```bash
python main.py
```

---

## 🧠 AI Algorithms

| # | Algorithm | Strategy | Speed | Backtracks |
|---|-----------|----------|-------|------------|
| 1 | **Backtracking** | Uninformed DFS | Slow | Many |
| 2 | **Forward Checking** | Constraint Propagation | Medium | Fewer |
| 3 | **MRV + AC-3** ⭐ | Informed Search + Arc Consistency | Fast | Very Few |
| 4 | **Simulated Annealing** | Local Search | Varies | N/A |

> ⭐ **MRV + AC-3** is the most efficient — recommended for Hard and Expert puzzles.

### How They Work

- **Backtracking** — Pure DFS. Places a number, recurses, undoes on failure. Simple but explores many states.
- **Forward Checking** — After each placement, checks if any unfilled cell has zero valid options and prunes early.
- **MRV (Minimum Remaining Values) + AC-3** — Selects the most constrained cell first (fewest options), then uses Arc Consistency to prune the search space further.
- **Simulated Annealing** — Fills the board randomly (one valid number per box), then swaps values probabilistically to reduce constraint violations — simulates a cooling process.

---

## 🎛️ Configuration Options

### Difficulty Levels
| Level | Cells Removed | Approx. Moves |
|-------|--------------|---------------|
| Easy | 30 | ~30–200 |
| Medium | 40 | ~50–500 |
| Hard | 50 | ~100–2,000 |
| Expert | 60 | ~200–10,000 |

### Animation Speeds
| Mode | Delay |
|------|-------|
| Very Slow | 0.7s / move |
| Slow | 0.25s / move |
| Normal | 0.08s / move |
| Fast | Frame skipping |
| Instant | No animation |

---

## 📁 Project Structure

```
SudokuAI_Project/
├── main.py               ← Entry point — launches the interactive GUI
├── csp_base.py           ← Core CSP formulation (constraints, board state)
├── generator.py          ← Sudoku puzzle generator (4 difficulty levels)
├── algorithms.py         ← All 4 AI solver implementations
├── ui_visualizer.py      ← Pygame GUI engine & animation logic
├── console_visualizer.py ← Terminal-based fallback visualizer
├── dashboard.py          ← Algorithm benchmarking comparison UI
└── QUICK_START.md        ← Short reference guide
```

---

## 📊 GUI Display Guide

| Element | Meaning |
|---------|---------|
| **Black numbers** | Original puzzle clues (fixed) |
| **Blue numbers** | AI-placed numbers during solving |
| **Bottom panel** | Live metrics: States Explored & Backtracks |

---

## 💡 Tips

1. Start with **Easy + MRV** for a quick, satisfying demo
2. Try **Backtracking on Hard** to see the algorithm struggle vs MRV
3. Use the **Benchmark Dashboard** to run all 4 algorithms on the same puzzle and compare results

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋 Author

**Nauman Ahmad**  
BS Computer Science  
GitHub: [@NaumanAhmad2005](https://github.com/NaumanAhmad2005)
