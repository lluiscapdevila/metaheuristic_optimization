import random
from src.utils.base_classes import Individual, Population, Chromosome


class GeneticAlgorithm:

    def __init__(self, gene_number, popsize, pc, pm, problem, gene_length: int = 1):
        self.gene_number = gene_number
        self.gene_length = 1
        self.chrom_length = self.gene_number * self.gene_length
        self.popsize = popsize
        self.pc = pc
        self.pm = pm
        self.problem = problem
        self.aux_indiv = Individual(self.chrom_length);
        # Create initial population
        initial_pop = Population(popsize=popsize, chrom_length=self.chrom_length)
        for i in range(popsize):
            initial_pop.set_fitness(i, problem.evaluate(initial_pop.get_ith(i)))
            initial_pop.compute_stats()
        self.pop = initial_pop


    def select_tournament(self):
        p1 = random.randint(0, self.popsize - 1)
        p2 = random.randint(0, self.popsize - 1)

        while p1 == p2:
            p2 = random.randint(0, self.popsize - 1)

        if self.pop.get_ith(p1).get_fitness() > self.pop.get_ith(p2).get_fitness():
            return self.pop.get_ith(p1)
        else:
            return self.pop.get_ith(p2)

    def spx(self, p1: Individual, p2: Individual):

        rand = random.randint(0, self.chrom_length)

        if random.random() > self.pc:
            return p1 if random.random() > 0.5 else p2

        # Copy parent 1
        for i in range(rand):
            self.aux_indiv.set_allele(i, p1.get_allele(i))

        # Copy parent 2
        for i in range(rand, self.chrom_length):
            self.aux_indiv.set_allele(i, p2.get_allele(i))

        return self.aux_indiv

    def mutate(self, p1: Individual):

        self.aux_indiv.assign(p1)

        for i in range(self.chrom_length):
            if random.random() <= self.pm:
                if self.aux_indiv.get_allele(i) == True:
                    self.aux_indiv.set_allele(i, False)
                else:
                    self.aux_indiv.set_allele(i, True)

        return self.aux_indiv

    def replace(self, new_indiv: Individual):
        self.pop.set_ith(self.pop.get_worstp(), new_indiv)
        self.pop.compute_stats()

    def evaluate_step(self, indiv: Individual):
        return self.problem.evaluate_step(indiv)

    def go_one_step(self):
        self.aux_indiv.assign(self.spx(self.select_tournament(), self.select_tournament()))
        self.aux_indiv.set_fitness(self.problem.evaluate_step(self.mutate(self.aux_indiv)))
        self.replace(self.aux_indiv)

    def get_solution(self):
        return self.pop.get_ith(self.pop.get_bestp())

    def get_worstp(self):
        return self.pop.worstp

    def get_bestp(self):
        return self.pop.bestp

    def get_worstf(self):
        return self.pop.worstf

    def get_bestf(self):
        return self.pop.bestf

    def get_avgf(self):
        return self.pop.avgf

    def get_absolute_best_f(self):
        return self.pop.absolute_best_f

    def get_ith(self, index: int):
        return self.pop.get_ith(index)

    def set_ith(self, indiv: Individual, index: int):
        self.pop.set_ith(index, indiv)