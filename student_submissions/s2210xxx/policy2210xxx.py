import numpy as np
from policy import Policy
from math import floor, ceil
from copy import deepcopy
from random import randint, shuffle, random, choice, choices
import time

class Policy2310139_2310090_2310191_2310242_2310423(Policy):
    def __init__(self, populationSize=300, penalty=2, mutationRate=0.1):
        self.MAX_ITERATIONS = 2000
        self.POPULATION_SIZE = populationSize
        self.stockLength = 0
        self.stockWidth = 0
        self.lengthArr = np.array([])
        self.widthArr = np.array([])
        self.demandArr = np.array([])
        self.N = None
        self.penalty = penalty
        self.mutationRate = mutationRate

    def generate_efficient_patterns(self):
        result = []
        availableArr = np.array([
            min(
                floor(self.stockLength / self.lengthArr[0]),
                floor(self.stockWidth / self.widthArr[0]),
                self.demandArr[0]
            )
        ])
        for n in range(1, self.N):
            s = np.sum(availableArr[:n] * self.lengthArr[:n])
            availableArr = np.append(availableArr, min(
                floor((self.stockLength - s) / self.lengthArr[n]),
                floor((self.stockWidth - s) / self.widthArr[n]),
                self.demandArr[n]
            ))
        while True:
            if np.sum(availableArr) == 0:
                break
            result.append(availableArr.copy())
            for j in range(len(availableArr) - 1, -1, -1):
                if availableArr[j] > 0:
                    availableArr[j] -= 1
                    for k in range(j + 1, self.N):
                        s = np.sum(availableArr[:k] * self.lengthArr[:k])
                        availableArr[k] = min(
                            floor((self.stockLength - s) / self.lengthArr[k]),
                            floor((self.stockWidth - s) / self.widthArr[k]),
                            self.demandArr[k]
                        )
                    break
            else:
                break
        return result

    def calculate_max_pattern_repetition(self, patternsArr):
        result = []
        for pattern in patternsArr:
            maxRep = 0
            for i in range(len(pattern)):
                if pattern[i] > 0:
                    neededRep = ceil(self.demandArr[i] / pattern[i])
                    if neededRep > maxRep:
                        maxRep = neededRep
            result.append(maxRep)
        return result

    def initialize_population(self, maxRepeatArr):
        initPopulation = []
        for _ in range(self.POPULATION_SIZE):
            chromosome = []
            indices = list(range(len(maxRepeatArr)))
            shuffle(indices)
            for idx in indices:
                chromosome.append(idx)
                chromosome.append(max(1, maxRepeatArr[idx]))
            initPopulation.append(chromosome)
        return initPopulation

    def evaluate_fitness(self, chromosome, patterns_arr):
        P = self.penalty
        unsupplied_sum = 0
        provided = np.zeros(self.N)
        total_unused_area = 0

        if self.stockLength == 0 or self.stockWidth == 0:
            raise ValueError("Stock dimensions (length or width) are not properly initialized.")

        stock_area = self.stockLength * self.stockWidth
        if stock_area == 0:
            stock_area = 1

        for i in range(0, len(chromosome), 2):
            pattern_index = chromosome[i]
            repetition = chromosome[i + 1]
            pattern = patterns_arr[pattern_index]

            provided += np.array(pattern) * repetition

            pattern_area = np.sum(np.array(pattern) * self.lengthArr * self.widthArr)
            total_unused_area += stock_area - pattern_area * repetition

        unsupplied = np.maximum(0, self.demandArr - provided)
        unsupplied_sum = np.sum(unsupplied * self.lengthArr * self.widthArr)

        fitness = (
            0.7 * (1 - total_unused_area / stock_area)
            - 0.3 * (P * unsupplied_sum / np.sum(self.demandArr))
        )

        return fitness

    def run(self, population, patterns_arr, max_repeat_arr, queue=None):
        start_time = time.time()
        best_results = []
        num_iters_same_result = 0
        last_result = float('inf')

        for count in range(self.MAX_ITERATIONS):
            fitness_pairs = [(ch, self.evaluate_fitness(ch, patterns_arr)) for ch in population]
            fitness_pairs.sort(key=lambda x: x[1], reverse=True)

            best_solution, best_fitness = fitness_pairs[0]
            best_results.append(best_fitness)

            if abs(best_fitness - last_result) < 1e-5:
                num_iters_same_result += 1
            else:
                num_iters_same_result = 0
            last_result = best_fitness

            if num_iters_same_result >= 100 or best_fitness == 1:
                break

            next_generation = [fitness_pairs[i][0] for i in range(3)]

            while len(next_generation) < self.POPULATION_SIZE:
                parent1 = None
                parent2 = None

                try:
                    if random() < 0.5:
                        parent1 = self.select_parents1([fp[0] for fp in fitness_pairs], [fp[1] for fp in fitness_pairs])
                        parent2 = self.select_parents1([fp[0] for fp in fitness_pairs], [fp[1] for fp in fitness_pairs])
                    else:
                        parent1 = self.select_parents2([fp[0] for fp in fitness_pairs], [fp[1] for fp in fitness_pairs])
                        parent2 = self.select_parents2([fp[0] for fp in fitness_pairs], [fp[1] for fp in fitness_pairs])
                except ValueError:
                    parent1 = choice([fp[0] for fp in fitness_pairs])
                    parent2 = choice([fp[0] for fp in fitness_pairs])

                if parent1 and parent2:
                    child1 = self.mutate(self.crossover(parent1, parent2), self.mutationRate, max_repeat_arr)
                    child2 = self.mutate(self.crossover(parent2, parent1), self.mutationRate, max_repeat_arr)
                    next_generation.extend([child1, child2])

            population = deepcopy(next_generation[:self.POPULATION_SIZE])

            if queue is not None:
                queue.put((count, best_solution, best_fitness, time.time() - start_time))

        end_time = time.time()

        return best_solution, best_fitness, best_results, end_time - start_time

    @staticmethod
    def select_parents1(population, fitness_scores):
        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            return choice(population)

        probabilities = [fitness / total_fitness for fitness in fitness_scores]
        return choices(population, probabilities)[0]

    @staticmethod
    def select_parents2(population, fitness_scores, tournament_size=5):
        indices = choices(range(len(population)), k=tournament_size)
        tournament = [population[i] for i in indices]
        tournament_scores = [fitness_scores[i] for i in indices]

        best_index = tournament_scores.index(max(tournament_scores))
        return tournament[best_index]

    @staticmethod
    def crossover(parent1, parent2):
        if parent1 is None or parent2 is None:
            raise ValueError("Parents must not be None")

        child = []
        for i in range(len(parent1)):
            if random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    @staticmethod
    def mutate(chromosome, mutation_rate, max_repeat_arr):
        mutated_chromosome = chromosome[:]
        for i in range(0, len(chromosome), 2):
            if random() < mutation_rate and i + 1 < len(chromosome):
                pattern_index = mutated_chromosome[i]
                mutated_chromosome[i + 1] = randint(1, max_repeat_arr[pattern_index])
        return mutated_chromosome

    def select_new_population(self, population, fitness_scores, mutation_rate, max_repeat_arr, selection_type="tournament"):
        new_population = []
        for _ in range(len(population) // 2):
            if selection_type == "tournament":
                parent1 = self.select_parents1(population, fitness_scores)
                parent2 = self.select_parents1(population, fitness_scores)
            elif selection_type == "roulette":
                parent1 = self.select_parents2(population, fitness_scores)
                parent2 = self.select_parents2(population, fitness_scores)

            child1 = self.crossover(parent1, parent2)
            child2 = self.crossover(parent2, parent1)

            child1 = self.mutate(child1, mutation_rate, max_repeat_arr)
            child2 = self.mutate(child2, mutation_rate, max_repeat_arr)

            new_population.extend([child1, child2])

        return new_population

    def get_action(self, observation, info):
        list_prods = observation["products"]
        stocks = observation["stocks"]

        if not stocks or not list_prods:
            return {"stock_idx": -1, "size": [0, 0], "position": (0, 0)}

        self.lengthArr = np.array([prod["size"][0] for prod in list_prods if prod["quantity"] > 0])
        self.widthArr = np.array([prod["size"][1] for prod in list_prods if prod["quantity"] > 0])
        self.demandArr = np.array([prod["quantity"] for prod in list_prods if prod["quantity"] > 0])
        self.N = len(self.lengthArr)

        if self.N == 0:
            return {"stock_idx": -1, "size": [0, 0], "position": (0, 0)}

        first_stock = stocks[0]
        self.stockLength, self.stockWidth = self._get_stock_size_(first_stock)

        patterns_arr = self.generate_efficient_patterns()
        max_repeat_arr = self.calculate_max_pattern_repetition(patterns_arr)
        population = self.initialize_population(max_repeat_arr)

        best_solution, _, _, _ = self.run(population, patterns_arr, max_repeat_arr, None)

        for i in range(0, len(best_solution), 2):
            pattern_index = best_solution[i]
            repetition = best_solution[i + 1]

            for stock_idx, stock in enumerate(stocks):
                stock_w, stock_h = self._get_stock_size_(stock)
                for x in range(stock_w):
                    for y in range(stock_h):
                        if pattern_index >= len(self.lengthArr):
                            continue
                        prod_size = (self.lengthArr[pattern_index], self.widthArr[pattern_index])

                        if self._can_place_(stock, (x, y), prod_size):
                            return {
                                "stock_idx": stock_idx,
                                "size": prod_size,
                                "position": (x, y)
                            }

        return {"stock_idx": -1, "size": [0, 0], "position": (0, 0)}
