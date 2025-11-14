import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

LOG_FILE = "outputs/logs/tuning_results_full.csv"
FIGURE_DIR = "outputs/figures"
os.makedirs(FIGURE_DIR, exist_ok=True)

def create_heatmap():
    try:
        df = pd.read_csv(LOG_FILE)
    except FileNotFoundError:
        print(f"Error: Log file not found at {LOG_FILE}")
        print("Please run 'run_tuning.py' first.")
        return

    best_config = df.loc[df['Cost'].idxmin()]
    best_rho = best_config['Rho']
    best_ants = best_config['Ants']
    
    print(f"Found best overall parameters: Rho={best_rho}, Ants={best_ants}")
    print("Generating Heatmap for Alpha vs Beta based on these values...")

    df_filtered = df[
        (df['Rho'] == best_rho) & 
        (df['Ants'] == best_ants)
    ]

    if df_filtered.empty:
        print("Error: No data found for the best combination. Cannot generate heatmap.")
        return
        
    heatmap_data = df_filtered.pivot(index="Alpha", columns="Beta", values="Cost")
    
    plt.figure(figsize=(10, 7))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="viridis_r")
    plt.title(f"Heatmap: Alpha vs Beta (Fixed Rho={best_rho}, Ants={best_ants})")
    plt.xlabel("Beta (Heuristic Importance)")
    plt.ylabel("Alpha (Pheromone Importance)")
    
    save_path = os.path.join(FIGURE_DIR, "tuning_heatmap_alpha_beta.png")
    plt.savefig(save_path)
    print(f"\nHeatmap saved to {save_path}")

if __name__ == "__main__":
    create_heatmap()