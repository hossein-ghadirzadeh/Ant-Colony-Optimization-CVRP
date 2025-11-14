import numpy as np
from scipy.spatial.distance import pdist, squareform
import re

def load_vrp_file(filepath):
    node_coords = []
    demands = []
    capacity = 0
    optimal_value = 0.0
    
    section = None
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.startswith("CAPACITY"):
            capacity = int(line.split(":")[-1].strip())
        
        elif line.startswith("COMMENT"):
            match = re.search(r'(Optimal value|Best value)\s*:\s*(\d+)', line)
            if match:
                optimal_value = float(match.group(2))

        elif line.startswith("NODE_COORD_SECTION"):
            section = "COORD"
            continue
        elif line.startswith("DEMAND_SECTION"):
            section = "DEMAND"
            continue
        elif line.startswith("DEPOT_SECTION"):
            section = "DEPOT"
            continue
        elif line.startswith("EOF"):
            break
            
        if section == "COORD":
            parts = line.split()
            if len(parts) >= 3:
                node_coords.append([float(parts[1]), float(parts[2])])
        elif section == "DEMAND":
            parts = line.split()
            if len(parts) >= 2:
                demands.append(int(parts[1]))

    nodes = np.array(node_coords)
    demands = np.array(demands)
    dist_matrix = squareform(pdist(nodes))
    
    return nodes, demands, capacity, dist_matrix, optimal_value

def create_heuristic_matrix(d_ij):
    dist_matrix_safe = d_ij.copy()
    dist_matrix_safe[dist_matrix_safe == 0] = 1e-10 
    heuristic = 1.0 / dist_matrix_safe
    return heuristic