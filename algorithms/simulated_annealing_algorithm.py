import random
import time
import numpy as np
import copy
from src.utils.base_classes import Chromosome, Individual


class SimulatedAnnealing:

    def __init__(self, gene_length, gene_number, temp, problem, iterations: int = 10000, verbose: int = 1,
                 min_temp=10 ** -100,
                 method: str = 'mutation', alpha: float = 0.95):
        self.gene_number = gene_number
        self.gene_length = 1
        self.chrom_length = self.gene_number * self.gene_length
        self.temp = temp
        self.problem = problem
        self.iterations = iterations
        self.set_best_sol(None)
        self.verbose = verbose
        self.min_temp = min_temp
        self.method = method
        self.alpha = alpha

    def set_time_taken(self, time: float):
        self._time_taken = time

    def get_time_taken(self):
        return self._time_taken

    def set_best_sol(self, solution: Chromosome):
        self._best_sol = solution

    def get_best_sol(self):
        return self._best_sol

    def set_num_iterations(self, iter: int):
        self._num_iterations = iter

    def get_num_iterations(self):
        return self._num_iterations

    def get_sol_history(self):
        return self.sol_history

    def find_neighbour(self, ind: Individual, mutation_rate: float = 0.05, swap_alleles: int = 2):
        individual = Individual(self.chrom_length)

        # If method is mutation, mutate the current solution with a given chance
        if self.method == 'mutation':
            individual.set_chrom(ind.get_chromosome())
            for i in range(self.chrom_length):
                if random.random() <= mutation_rate:
                    if individual.get_allele(i):
                        individual.set_allele(i, False)
                    else:
                        individual.set_allele(i, True)

        # Else supposing that method is random
        else:
            individual.set_chrom(ind.get_chromosome())
            alleles_to_mutate = random.sample(range(self.chrom_length), swap_alleles)
            for i in alleles_to_mutate:
                if individual.get_allele(i):
                    individual.set_allele(i, False)
                else:
                    individual.set_allele(i, True)

        return individual

    def simulated_annealing(self):
        """
        """
        start_time = time.time()
        current_sol = Individual(self.chrom_length)
        current_sol.set_fitness(self.problem.evaluate(current_sol))
        self.set_best_sol(current_sol)
        self.sol_history = [current_sol]
        temperature = self.temp
        for i in range(self.iterations):
            if self.verbose == 1:
                print(f">>> Iteration {i}")
            # Propose a new solution
            proposed_solution = self.find_neighbour(current_sol)
            proposed_solution.set_fitness(self.problem.evaluate_step(proposed_solution))
            # Check if the new solution's score is better (higher) or if Temperature allows for a change
            diff = proposed_solution.get_fitness() - current_sol.get_fitness()
            # Set probability to 0 if temperature is too low
            substitution_proba = 1 if diff > 0 else np.exp(diff / temperature)
            if (diff > 0) or (substitution_proba > random.random()):
                current_sol = proposed_solution
                current_sol.set_fitness(self.problem.evaluate(current_sol))

            self.sol_history.append(copy.deepcopy(current_sol))
            self.set_best_sol(current_sol)
            # Update temperature
            temperature = temperature * self.alpha
            # temperature = temperature / (i + 1)
            if temperature < self.min_temp:
                temperature = self.min_temp
            if self.verbose == 1:
                print(f"- The best fit is {self.get_best_sol().get_fitness()}")
            if self.problem.get_tf_known() & (self.get_best_sol().get_fitness() >= self.problem.get_target_fitness()):
                print(f"Solution found!! After {self.problem.get_fitness_counter()} evaluations.")
                break

        self.set_num_iterations(self.problem.get_fitness_counter())
        self.set_time_taken(time.time() - start_time)

    def get_solution(self):
        return self.get_best_sol()
