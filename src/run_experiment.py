import numpy as np
from src.agents.ant import Ant

def run_aco_experiment(nodes, demands, capacity, d_ij, heuristic, config):
    alpha = config['alpha']
    beta = config['beta']
    rho = config['evaporation_rate']
    n_ants = config['num_ants']
    n_iterations = config['num_iterations']
    Q = config['Q']
    
    pheromone = np.ones((len(nodes), len(nodes)))
    best_cost_run = float('inf')
    cost_history = []

    for iteration in range(n_iterations):
        ants = []
        for _ in range(n_ants):
            ant = Ant(len(nodes), capacity, demands)
            ant.run_tour(d_ij, pheromone, heuristic, alpha, beta)
            ants.append(ant)
            
        ants.sort(key=lambda x: x.total_cost)
        if ants[0].total_cost < best_cost_run:
            best_cost_run = ants[0].total_cost
            
        cost_history.append(best_cost_run)
            
        pheromone *= (1 - rho)
        for ant in ants:
            deposit = Q / ant.total_cost
            for i in range(len(ant.tour) - 1):
                u, v = ant.tour[i], ant.tour[i+1]
                pheromone[u][v] += deposit
                pheromone[v][u] += deposit
                
    return best_cost_run, cost_history