import random


class Chromosome:

    def __init__(self, length: int = 128):
        # Initialize allele vector with random alleles (either 0 or 1).
        alleles = [bool(random.getrandbits(1)) for allele in range(length)]
        self.alleles = alleles
        self.length = length

    def set_allele(self, index: int, value: bool):
        self.alleles[index] = value

    def get_allele(self, index: int):
        return self.alleles[index]

    def print_chromosome(self):
        return self.alleles


class Individual:

    def __init__(self, length: int = 128):
        self.chrom = Chromosome(length)
        self.fitness = 0
        self.length = length

    def get_length(self):
        return self.length

    def set_fitness(self, fit):
        self.fitness = fit

    def get_fitness(self):
        return self.fitness

    def set_allele(self, index: int, value: bool):
        self.chrom.set_allele(index, value)

    def get_allele(self, index: int):
        return self.chrom.get_allele(index)

    def set_chrom(self, ch: Chromosome):
        self.chrom = ch

    def get_chromosome(self):
        return self.chrom

    @staticmethod
    def copy(source: Chromosome, destination: Chromosome):
        print(f"Still not implemented.")

    def assign(self, ind):
        self.chrom = ind.get_chromosome()
        self.fitness = ind.get_fitness()
        self.length = ind.get_length()


class Population:

    def __init__(self, popsize: int, chrom_length: int):
        # Create initial population
        population = [Individual(chrom_length) for i in range(popsize)]
        self.popsize = popsize
        self.chrom_length = chrom_length
        self.population = population
        # Initialize statistics
        self.bestp = 0
        self.worstp = 0
        self.bestf = 0
        self.worstf = 0
        self.avgf = 0
        self.absolute_best_f = 0
        self.compute_stats()

    def get_popsize(self):
        return self.popsize

    def worst_pos(self):
        return self.worstp

    def get_ith(self, index: int):
        try:
            return self.population[index]
        except:
            raise IndexError("Index out of range when getting a copy of an individual")

    def set_ith(self, index: int, indiv: Individual):
        try:
            self.population[index].assign(indiv)
        except:
            raise IndexError("Index out of range when inserting an individual")
        self.compute_stats()

    def set_fitness(self, index: int, fitness: float):
        self.population[index].set_fitness(fitness)

    def compute_stats(self):
        # Initialize values
        total = 0
        worstf = self.population[0].get_fitness()
        bestf = self.population[0].get_fitness()
        worstp, bestp = 0, 0
        BESTF = 0

        for i in range(self.popsize):
            f = self.population[i].get_fitness()
            if (f <= worstf):
                self.worstf, self.worstp = f, i
            if (f > bestf):
                self.bestf, self.bestp = f, i
            if (f > BESTF):
                self.absolute_best_f = f
            total += f

        self.avgf = total / self.popsize

    def get_worstp(self):
        return self.worstp

    def get_bestp(self):
        return self.bestp

    def get_worstf(self):
        return self.worstf

    def get_bestf(self):
        return self.bestf

    def get_avgf(self):
        return self.avgf

    def get_absolute_best_f(self):
        return self.absolute_best_f

    def print_stats(self):
        print(f">>>>>>> The stats for this population are:")
        print(f"- Worst P: {self.worstp}")
        print(f"- Best P: {self.bestp}")
        print(f"- Worst F: {self.worstf}")
        print(f"- Best F: {self.bestf}")
        print(f"- Avg F: {self.avgf}")
