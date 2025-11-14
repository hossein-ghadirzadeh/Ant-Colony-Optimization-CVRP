import sys
from pathlib import Path
import os
import json
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils.data_loader import load_vrp_file, create_heuristic_matrix
from run_experiment import run_aco_experiment
from visualization.plotter import create_comparative_plot

CONFIG_DIR = "configs"
DATA_DIR = "data"
LOG_DIR = "outputs/logs"
FIGURE_DIR = "outputs/figures"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)

def main():
    all_results = []
    
    config_files = [f for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]
    data_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.vrp')]

    print(f"Found {len(config_files)} configs and {len(data_files)} data instances.")

    for config_file in config_files:
        with open(os.path.join(CONFIG_DIR, config_file)) as f:
            config = json.load(f)
        config_name = config['name']

        for data_file in data_files:
            instance_name = data_file.split('.')[0]
            print(f"--- Running: {config_name} on {instance_name} ---")
            
            file_path = os.path.join(DATA_DIR, data_file)
            nodes, demands, capacity, d_ij, optimal_value = load_vrp_file(file_path) 
            heuristic = create_heuristic_matrix(d_ij)
            
            best_cost, cost_history = run_aco_experiment(nodes, demands, capacity, d_ij, heuristic, config)
            
            print(f"Best Cost: {best_cost:.2f} (Optimal: {optimal_value})")
            
            all_results.append({
                "config_name": config_name,
                "instance_name": instance_name,
                "best_cost": best_cost,
                "optimal_value": optimal_value,
                **config 
            })

    df_results = pd.DataFrame(all_results)
    df_results['gap_percent'] = ((df_results['best_cost'] - df_results['optimal_value']) / df_results['optimal_value']) * 100
    df_results = df_results.sort_values(by="gap_percent")
    
    log_path = os.path.join(LOG_DIR, "results_with_gap.csv")
    df_results.to_csv(log_path, index=False)
    
    print(f"\n✅ All experiments complete. Results saved to {log_path}")
    
    print("Generating final comparative plot...")
    create_comparative_plot(log_path, FIGURE_DIR)
    
    print("\nTop 5 results (by optimality gap):")
    print(df_results[['instance_name', 'config_name', 'best_cost', 'optimal_value', 'gap_percent']].head(5))

if __name__ == "__main__":
    main()