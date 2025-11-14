import sys
from pathlib import Path
import pandas as pd
import itertools
import os
import time

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.data_loader import load_vrp_file, create_heuristic_matrix
from run_experiment import run_aco_experiment

TUNING_DATA_FILE = "data/A-n32-k5.vrp" 
LOG_DIR = "outputs/logs"
os.makedirs(LOG_DIR, exist_ok=True)

alpha_values  = [1.0, 2.0, 3.0, 4.0, 5.0]
beta_values   = [1.0, 2.0, 3.0, 4.0, 5.0]
rho_values    = [0.1, 0.2, 0.3, 0.4, 0.5]
n_ants_values = [30, 50, 70, 100]

fixed_config = {
    "num_iterations": 50,
    "Q": 100
}

def main_tuning():
    start_time = time.time()
    
    print(f"Loading tuning dataset: {TUNING_DATA_FILE}")
    nodes, demands, capacity, d_ij = load_vrp_file(TUNING_DATA_FILE)
    heuristic = create_heuristic_matrix(d_ij)
    
    combinations = list(itertools.product(alpha_values, beta_values, rho_values, n_ants_values))
    print(f"Starting 4D Grid Search with {len(combinations)} combinations...")
    
    results = []

    for i, (a, b, r, n) in enumerate(combinations):
        print(f"[{i+1}/{len(combinations)}] Testing: Alpha={a}, Beta={b}, Rho={r}, Ants={n}...", end="")
        
        current_config = fixed_config.copy()
        current_config['alpha'] = a
        current_config['beta'] = b
        current_config['evaporation_rate'] = r
        current_config['num_ants'] = n
        
        cost, _ = run_aco_experiment(nodes, demands, capacity, d_ij, heuristic, current_config)
        
        print(f" -> Cost: {cost:.2f}")
        results.append({
            "Alpha": a,
            "Beta": b,
            "Rho": r,
            "Ants": n,
            "Cost": cost
        })

    df_results = pd.DataFrame(results)
    
    log_path = os.path.join(LOG_DIR, "tuning_results_full.csv")
    df_results.to_csv(log_path, index=False)
    
    end_time = time.time()
    print("\n--- TUNING COMPLETE ---")
    print(f"Total time: {(end_time - start_time) / 60:.2f} minutes")
    print(f"Full log saved to {log_path}")
    
    print("\nTop 3 Configurations found:")
    print(df_results.sort_values(by="Cost").head(3))

if __name__ == "__main__":
    main_tuning()