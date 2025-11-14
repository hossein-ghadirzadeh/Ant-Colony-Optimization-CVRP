import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

def create_comparative_plot(csv_path, save_dir):
    try:
        df_results = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: Could not find results file at {csv_path}")
        return

    plt.figure(figsize=(15, 8))
    
    sns.barplot(
        data=df_results,
        x='instance_name',
        y='gap_percent',
        hue='config_name'
    )
    
    plt.title('Algorithm Performance Comparison (Optimality Gap %)', fontsize=16)
    plt.xlabel('Dataset Instance', fontsize=12)
    plt.ylabel('Optimality Gap (%) - Lower is Better', fontsize=12)
    plt.legend(title='Configuration', loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    

    save_path = os.path.join(save_dir, "comparative_gap_chart.png")
    plt.savefig(save_path)
    plt.close()
    
    print(f"\nComparative plot saved to {save_path}")