# Note: code in this file has been extracted from the jupyter notebook

import random
import numpy as np

# Reproduction - tournament selection
def reproduction(population, rating):
    results = []
    for i, individual in enumerate(population):
        opponents = population.copy()
        opponents.pop(i)
        opponent = random.choice(opponents)
        if rating(individual) < rating(opponent):
            results.append(individual)
        else:
            results.append(opponent)
    return results

# One-point crossover
def crossing(population, crossover_prob):
    results = []
    parents_list = population.copy()
    for _ in range(0, len(population) - 1, 2):
        crossover_value = random.uniform(0, 1)
        parent1, parent2 = random.sample(parents_list, 2)
        parents_list.remove(parent1)
        parents_list.remove(parent2)
        if crossover_value < crossover_prob:
            crossing_point = random.randint(1, len(parent1))
            child1, child2 = [
                parent1[:crossing_point] + parent2[crossing_point:],
                parent2[:crossing_point] + parent1[crossing_point:]
            ]
            results.append(child1)
            results.append(child2)
        else:
            results.append(parent1)
            results.append(parent2)
    # If population size is odd, add single parent to the results
    if len(population) % 2 == 1:
        results.append(parents_list[0])
    return results

# Gaussian mutation
def mutation(population, mutation_strength, mutation_prob):
    results = []
    for individual in population:
        mutation_value = random.uniform(0, 1)
        if mutation_value < mutation_prob:
            results.append((individual + mutation_strength * np.random.normal(0, 1, len(individual))).tolist())
        else:
            results.append(individual)
    return results

# ---------------------------------------------------------------
# Evolutionary algorithm implementation based on previous functions
def evolutionary(population, rating, crossover_prob, mutation_strength, mutation_prob, max_generations):
    generation = 0
    ratings = [rating(individual) for individual in population]
    best_value = min(ratings)
    best_value_index = ratings.index(best_value)
    best_individual = population[best_value_index]
    while generation < max_generations:
        reproducted = reproduction(population, rating) # Reprodukcja
        crossed = crossing(reproducted, crossover_prob) # Krzyżowanie
        mutated = mutation(crossed, mutation_strength, mutation_prob) # Mutowanie
        # New generation rating
        new_ratings = [rating(individual) for individual in mutated]
        new_best_value = min(new_ratings)
        new_best_value_index = new_ratings.index(new_best_value)
        new_best_individual = mutated[new_best_value_index]
        if new_best_value < best_value:
            best_value = new_best_value
            best_individual = new_best_individual
        # Generation update
        population = mutated
        ratings = new_ratings
        generation += 1
    return [best_individual, best_value]