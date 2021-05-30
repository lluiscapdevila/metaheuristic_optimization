import numpy as np
from src.utils.base_classes import Individual


class Problem:

    def __init__(self, gl: int = 1, gn: int = 1):
        """ Problem class that serves as super for other problems.

        :param gl: Gene Length. Defaults to one (number of bits per gene)
        :param gn: Gene number. Number of genes by individual.

        """
        self.cl = gl * gn
        self.gl = gl
        self.gn = gn
        self.fitness_counter = 0
        self.tf_known = False
        self.target_fitness = -999999.9

    def get_genel(self):
        return self.gl

    def get_genen(self):
        return self.gn

    def set_genel(self, gl):
        self.gl = gl

    def set_genen(self, gn):
        self.gn = gn

    def get_fitness_counter(self):
        return self.fitness_counter

    def get_target_fitness(self):
        return self.target_fitness

    def set_target_fitness(self, tf: float):
        self.target_fitness = tf
        self.tf_known = True

    def get_tf_known(self):
        return self.tf_known

    def evaluate_step(self, indiv: Individual):
        self.fitness_counter += 1
        return self.evaluate(indiv)

    def evaluate(self, indiv: Individual):
        pass


class ProblemOneMax(Problem):

    def __init__(self):
        """
        One Max Problem definition.
        """
        super().__init__()

    def evaluate(self, indiv: Individual):
        return self.onemax(indiv)

    def onemax(self, indiv: Individual):
        f = 0
        for i in range(indiv.get_length()):
            if indiv.get_allele(i) == 1:
                f += 1

        indiv.set_fitness(f)
        return f


class ProblemPPeaks(Problem):

    def __init__(self, w: np.array):
        """
        P-Peaks problem definition
        """
        super().__init__()
        self.w = w

    def evaluate(self, indiv: Individual, w: np.array = None):
        return self.subset_sum_problem(indiv, w=self.w)

    @staticmethod
    def subset_sum_problem(indiv: Individual, w: np.array, c: int = 300500):
        """

        :param indiv:
        :param w:
        :param c:
        :return: fitness of the input individual

        """
        fitness = 0
        cl = indiv.get_length()
        # Check the individual length
        if cl != 128:
            print(f"Length mismatch error in Subset sum function.")

        for i in range(cl):
            fitness += w[i] * indiv.get_allele(i)

        if fitness > c:
            fitness = c - fitness * 0.1
            if fitness < 0:
                fitness = 0

        indiv.set_fitness(fitness)

        return fitness
