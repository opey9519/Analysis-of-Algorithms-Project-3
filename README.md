# Analysis-of-Algorithms-Project-3

Graph Algorithms in Network Optimization. A project exploring real-world problem modeling using graphs, with implementations of **BFS/DFS**, **Bellman-Ford**, and **Kruskal**, along with complexity and performance analysis.

# Graph Algorithms in Network Optimization

## 📌 Overview

This project explores how graph algorithms can be applied to solve real-world network optimization problems. It includes graph modeling, algorithm implementation, complexity analysis, and performance comparisons across different graph structures.

Developed as part of the **Analysis of Algorithms** course.

---

## Problem Statement

How can we model a social network using graph structures and apply graph algorithms to analyze user connectivity, relationship strength (measured by mutual connections), and optimal connections?

---

### Graph Representation

- **Vertices:** Individuals
- **Edges:** Friendships between Individuals
- **Graph Type:**
  - Undirected
  - Weighted

---

## 🏗️ Graph Construction

- Graph contains **17 vertices**
- Built using:
  - Synthetic dataset designed for testing

---

## 📊 Complexity Analysis

For each algorithm, we provide in our report:

- Pseudocode
- Time Complexity
- Space Complexity
- Best-case and Worst-case scenarios

---

## 🧪 Experimental Analysis

We evaluate algorithms in our report based on:

- Execution time
- Memory usage / performance observations
- Performance on:
  - Small vs large graphs
  - Sparse vs dense graphs
  -

---

## 💡 Discussion & Insights

- Comparison of algorithm efficiency
- When to use each algorithm
- Limitations and trade-offs
- Key observations from experiments

---

## 📂 Projected Project Structure (Up for Change)

```
  Analysis-of-Algorithms-Project-3/
├── src/
│   ├── graph.py
│   └── algorithms.py
│
│
├── analysis/
│   ├── benchmark.py
│   ├── complexity.md
│   └── results.csv
│
├── data/
│   ├── benchmark_execution_time.png
│   ├── benchmark_memory_usage.png
│   ├── benchmark_results.csv
│   └── social_graph.png
│
├── docs/
│   ├── COT4400-Final-Project-Report.pdf
│   ├── Instructions-Project-3.pdf
│   └── COT440-Final-Presentation.ppt
│
├── main.py
├── .gitignore
├── LICENSE
├── requirements.txt
├── .venv/
└── README.md
```

## Set up

1. Create Python Virtual Environment
   ```
     python3 -m venv .venv
   ```
2. Activate Python Virtual Environment
   ```
     source .venv/bin/activate
   ```
3. Install Dependencies
   ```
     pip install -r requirements.txt
   ```

## Run

Run the _main.py_ Python file

```
  python3 main.py
```
