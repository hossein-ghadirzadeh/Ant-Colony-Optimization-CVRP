import numpy as np
import random

class Ant:
    def __init__(self, num_nodes, capacity, demands):
        # 1. The Rules
        self.num_nodes = num_nodes      # Number: How many customers exist?
        self.capacity = capacity        # Number: How big is my truck? (e.g., 100 units)
        self.demands = demands          # List: How much does each customer want?
        # 2. The Logbook (Memory)
        self.tour = []                  # An empty list to write down the path I take.
        self.total_cost = 0.0           # My odometer (starts at 0 km).
        self.visited_customers = set()  # A checklist of who I have already served.

    def select_next_node(self, current_node, feasible_nodes, pheromone, heuristic, alpha, beta  ):
        probabilities = []
        denominator = 0.0

        for node in feasible_nodes:
            # A. Pheromone (Tau): How many ants liked this path before?
            tau = pheromone[current_node][node] ** alpha

            # B. Heuristic (Eta): How close is this customer? (1 / distance)
            eta = heuristic[current_node][node] ** beta

            # C. Final Score: Combine them
            prob_value = tau * eta

            # Add to the list of scores
            probabilities.append(prob_value)
            denominator += prob_value

        if denominator == 0:
            return random.choice(feasible_nodes)
        
        probabilities = np.array(probabilities) / denominator
        
        next_node = np.random.choice(feasible_nodes, p=probabilities)
        return next_node
    
    def calculate_cost(self, dist_matrix):
        self.total_cost = 0.0
        for i in range(len(self.tour) - 1):
            from_node = self.tour[i]
            to_node = self.tour[i+1]
            self.total_cost += dist_matrix[from_node][to_node]

    def run_tour(self, dist_matrix, pheromone, heuristic, alpha, beta):
        current_node = 0
        self.tour = [0]
        self.visited_customers = set()
        current_load = 0
        
        while len(self.visited_customers) < (self.num_nodes - 1):
            
            feasible_nodes = []
            
            for node in range(1, self.num_nodes):
                if node not in self.visited_customers:
                    if current_load + self.demands[node] <= self.capacity:
                        feasible_nodes.append(node)
            
            if not feasible_nodes:
                if current_node != 0:
                    self.tour.append(0)
                    current_node = 0
                    current_load = 0
                    continue
                else:
                    break

            next_node = self.select_next_node(current_node, feasible_nodes, pheromone, heuristic, alpha, beta)
            
            self.tour.append(next_node)
            self.visited_customers.add(next_node)
            current_load += self.demands[next_node]
            current_node = next_node
        
        if self.tour[-1] != 0:
            self.tour.append(0)
            
        self.calculate_cost(dist_matrix)