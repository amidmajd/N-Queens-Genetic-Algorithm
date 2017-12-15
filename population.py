from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
sns.set()
from DNA import main as DNA

class main():
    def __init__(self, pop_len, mutation_rate, max_iter):
        self.pop_len = pop_len
        self.mut_rate = mutation_rate
        self.max_iter = max_iter
        self.pop = []
        self.score = np.zeros((self.pop_len))


    def initialize(self):
        for c in range(self.pop_len):
            dna = DNA().cromosome
            self.pop.append(dna)
        self.pop = np.array(self.pop)
        # print(self.pop.shape)


    def fitness(self, cromosome):
        score = 0
        # check if any 2 element are the same in cromosome
        score += (len(cromosome) + len(np.unique(cromosome))) / 2

        # check for 2 queens are in diameter hazard
        for g in range(len(cromosome)):
            try:
                if cromosome[g] != cromosome[g+1]+1 and \
                   cromosome[g] != cromosome[g+1]-1:
                       score += 1
            except IndexError as e:
                # last index error handle
                # print(e)
                pass

        return np.power(2, score)


    def fitness_measure(self):
        for c, cromosome in enumerate(self.pop):
            self.score[c] = self.fitness(cromosome)
        # print('min:', self.score.min())
        # print('max:', self.score.max())
        # print('avg:', np.average(self.score))




if __name__ == '__main__':
    population = main(100, 0.01, 10000)
    population.initialize()
    population.fitness_measure()
