# 🔍 Depth-First Branch-and-Bound (DFBnB) Anomaly Detection

## Overview

This project implements the Depth-First Branch-and-Bound (DFBnB) algorithm in Python, designed to explore paths in a tree or graph to find the least costly path. The primary goal of this project is to detect and study an anomaly in the DFBnB algorithm under specific conditions, where it performs unexpectedly efficiently—running in polynomial time rather than the anticipated exponential time.

### 🧩 Anomaly Background

The anomaly occurs when using the DFBnB algorithm on a tree with:
- **🌳 Uniform branching factor**: Each node has a consistent number of children.
- **🎲 Random edge costs**: Edges have costs that are either 0 or 1, with equal probability.
- **🧮 Node ordering by cost**: Children of each node are explored in the order of increasing edge cost.

Under these conditions, the algorithm can find a path with a cost of 0 early in the search, setting the bound to 0 and pruning all other paths. This causes the algorithm to run in polynomial time, which is surprising given the usual exponential complexity of depth-first searches. The anomaly is particularly relevant when the expected number of zero-cost children of a node is greater than one.

For more detailed information on this anomaly, refer to the provided slides "SAI-3-4.ppt."

## 🗂️ Project Structure

```plaintext
.
├── README.md
├── dfbnb.py          # Implementation of the DFBnB algorithm
├── experiment_utils.py         # Utilities for running experiments
├── main.py                     # Main script to execute experiments
├── databases/                  # Directory where SQLite databases are stored
└── results/                    # Directory where experiment results are stored
```

### 📁 Files and Directories

- **`dfbnb.py`**: Contains the implementation of the DFBnB algorithm, including tree creation and the depth-first search with pruning logic.
- **`experiment_utils.py`**: Contains utility functions to run experiments across different configurations, save results, and manage databases.
- **`main.py`**: The entry point for running experiments. It sets up parameters and calls the experiment utilities.
- **`databases/`**: Directory where the SQLite database files are generated and stored during the experiments.
- **`results/`**: Directory where the CSV files with experiment results are saved.

## 🚀 Getting Started

### 📋 Prerequisites

To run the project, ensure you have Python installed along with the following libraries:

- `sqlite3`
- `pandas`
- `random`

### ▶️ Running the Experiments

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/dfbnb-anomaly-detection.git
   cd dfbnb-anomaly-detection
   ```

2. **Run the experiments**:
   Execute the `main.py` script to run the experiments with default settings:
   ```bash
   python main.py
   ```

   This will generate databases in the `databases/` directory and save the experiment results in the `results/` directory.

3. **Modify Parameters**:
   - You can change the branching factors, depths, number of repetitions, and file handling configurations directly in the `main.py` script by modifying the parameters passed to the `run_experiments` function.

### 📊 Understanding the Results

The results are saved as CSV files in the `results/` directory. Each CSV file contains the average number of nodes expanded for different combinations of branching factors and depths. These results can be analyzed to detect the anomaly where the DFBnB algorithm runs in polynomial time.

### Example Output

After running the experiments, you might find that under certain conditions (specific branching factors and depths with random edge costs), the algorithm expands significantly fewer nodes than expected, indicating the presence of the anomaly.

---

### 📚 References

- **"SAI-3-4.ppt"**: A presentation providing insights into the anomaly detected in the DFBnB algorithm. This file contains theoretical background and experimental evidence supporting the anomaly.



