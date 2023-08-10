import random 
import math

f = open("input4.stock", "r")
txt = (f.read()).split()
STOCK_LENGTH = int(txt[2])
CUSTOMER_DEMANDS = []
i = 4 
while (txt[i] != "Answer:"):
    CUSTOMER_DEMANDS.append(txt[i][:-1])
    i += 1
CUSTOMER_DEMANDS[len(CUSTOMER_DEMANDS)-1] = txt[i-1]
for i in range(len(CUSTOMER_DEMANDS)):
    CUSTOMER_DEMANDS[i] = int(CUSTOMER_DEMANDS[i])
INITIAL_TEMPERATURE = 100.0
COOLING_RATE = 0.003
MAX_ITERATIONS = 70

# Generate initial solution
def generate_initial_solution():
    cutting_patterns = []
    for demand in CUSTOMER_DEMANDS:
        pattern = [0] * int(math.ceil(demand / STOCK_LENGTH))
        cutting_patterns.append(pattern)
    return cutting_patterns

# Calculate waste for a solution
def calculate_waste(solution):
    total_waste = 0
    for i in range(len(CUSTOMER_DEMANDS)):
        pattern = solution[i]
        total_length = sum(pattern) * STOCK_LENGTH
        waste = total_length - CUSTOMER_DEMANDS[i]
        total_waste += waste
    return total_waste

# Generate a neighbor solution by modifying the current solution
def generate_neighbor_solution(current_solution):
    neighbor_solution = current_solution.copy()
    # Select a random cutting pattern to modify
    pattern_index = random.randint(0, len(neighbor_solution) - 1)
    pattern = neighbor_solution[pattern_index]
    # Randomly increase or decrease the number of cuts in the pattern
    cut_index = random.randint(0, len(pattern) - 1)
    pattern[cut_index] += random.choice([-1, 1])
    return neighbor_solution

# Acceptance probability based on the temperature and the difference in waste
def acceptance_probability(current_waste, neighbor_waste, temperature):
    if neighbor_waste < current_waste:
        return 1.0
    return math.exp((current_waste - neighbor_waste) / temperature)

# Simulated Annealing algorithm
def simulated_annealing():
    current_solution = generate_initial_solution()
    current_waste = calculate_waste(current_solution)
    temperature = INITIAL_TEMPERATURE

    for iteration in range(MAX_ITERATIONS):
        neighbor_solution = generate_neighbor_solution(current_solution)
        neighbor_waste = calculate_waste(neighbor_solution)
        if acceptance_probability(current_waste, neighbor_waste, temperature) > random.random():
            current_solution = neighbor_solution
            current_waste = neighbor_waste
        temperature *= 1 - COOLING_RATE

    return current_waste

# Run the algorithm
best_waste = simulated_annealing()

print("Best solution:", math.ceil(-best_waste / STOCK_LENGTH))
