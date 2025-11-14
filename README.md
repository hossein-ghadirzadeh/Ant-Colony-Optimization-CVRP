# Ant-Colony-Optimization-CVRP

Implementation of a Modified Ant Colony Optimization (ACO) algorithm to solve the Capacitated Vehicle Routing Problem (CVRP). Includes comparative analysis of parameters.

### Project Structure

The project is organized in a modular structure as follows:

```bash
Ant-Colony-Optimization-CVRP/
├── data/                # Input: Benchmark .vrp files
├── configs/              # Input: .json config files
├── outputs/             # Output: All generated logs and figures
│   ├── figures/
│   └── logs/
│
├── src/                 # Main source code
│   ├── agents/
│   │   └── ant.py
│   ├── utils/
│   │   └── data_loader.py
│   ├── visualization/
│   │   └── plotter.py
│   │
│   ├── run_tuning.py        # (Phase 1) Tuning script
│   ├── generate_heatmap.py  # Script to generate heatmap from tune logs
│   ├── run_experiment.py    # Helper function (imported by main/tuning)
│   └── main.py              # (Phase 2) Validation script
│
├── requirements.txt      # Project dependencies
└── README.md             # This file
```

---

## How to Run

The project is designed in a two-phase workflow: **Tuning** and **Validation**.

### Prerequisites

1. Install all required dependencies:

```bash
pip install -r requirements.txt
```

2.  Place your `.vrp` files (e.g., from the Augerat set) inside the `data/` folder.

### Phase 1: Hyperparameter Tuning (Optional - Already Run)

This step runs the 500-combination Grid Search on a single dataset (`A-n32-k5.vrp`) to find the best-performing parameters.

```bash
python src/run_tuning.py
python src/generate_heatmap.py
```

- Output: This generates `outputs/logs/tuning_results_full.csv` (the raw log) and `outputs/figures/tuning_heatmap.png` (a visualization of the Alpha vs. Beta landscape).

### Phase 2: Final Validation Run

This is the main script. It takes the winning configurations from Phase 1, runs them against all datasets in the `data/` folder, and generates the final log and chart for the report.

1. **Create Configs:** Based on the Top 3 Configurations printed by `run_tuning.py`, create `.json` files in the `configs/` folder (e.g., `config_winner_1.json`, `config_winner_2.json`).

2. **Run Validation:**

```bash
python src/main.py
```

---

### Results

All final outputs are saved in the `outputs/` directory.

- `outputs/logs/results_with_gap.csv:` The final data table showing the performance (Best Cost, Optimal Value, Gap %) for each configuration on each dataset.
- `outputs/figures/comparative_gap_chart.png:` The final grouped bar chart visualizing the gap_percent for easy comparison.

---

### Authors and Contact

This project was created by a team of students from Jönköping University's School of Engineering (JTH) for the third seminar of State of the Art course.

For questions, feedback, or collaborations, please feel free to reach out to any of the authors or open an issue on the project's repository.

| Name                    | Email Address            |
| ----------------------- | ------------------------ |
| **Hossein Ghadirzadeh** | `ghmo23az@student.ju.se` |
| **Martin Nilsson**      | `nima21si@student.ju.se` |

**Jönköping University, School of Engineering (JTH)**<br>
_November 2025_
