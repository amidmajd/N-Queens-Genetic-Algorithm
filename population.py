from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
sns.set()
from DNA import main as DNA

class main():
    def __init__(self, pop_len, mutation_rate, max_iter):
        if pop_len%2 == 0:
            self.pop_len = pop_len
        else:
            self.pop_len = pop_len + 1
        self.mut_rate = mutation_rate
        self.max_iter = max_iter
        self.pop = []
        self.score = np.zeros((self.pop_len))
        self.generation_num = 0


    def initialize(self):
        for c in range(self.pop_len):
            dna = DNA().cromosome
            self.pop.append(dna)
        self.pop = np.array(self.pop)
        # print(self.pop.shape)


    def fitness(self, cromosome):
        score = 0
        # check if any 2 element are the same in cromosome
        score += len(np.unique(cromosome))
        # print('1',cromosome, score)

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
        # print('2',cromosome, score)

        return np.power(score, 2)


    def fitness_measure(self):
        for c, cromosome in enumerate(self.pop):
            self.score[c] = self.fitness(cromosome)
        # print('min:', self.score.min())
        # print('max:', self.score.max())
        # print('avg:', np.average(self.score))


    def cross_over(self, p1, p2):
        dna = DNA().cromosome
        random_point = np.random.randint(0, len(dna))
        c1 = np.concatenate([np.array(p1[:random_point]) , np.array(p2[random_point:])])
        c2 = np.concatenate([np.array(p2[:random_point]) , np.array(p1[random_point:])])
        return c1, c2


    def mutation(self, cromosome):
        for g, gen in enumerate(cromosome):
            r = np.random.rand()
            if r < self.mut_rate:
                dna = DNA().cromosome
                cromosome[g] = np.random.choice(dna)
        return cromosome


    def selection(self):
        if self.score.max() - self.score.min() == 0:
            raise ValueError('low population')
        # print((self.score.max() - self.score.min()))
        reg_score = (self.score - self.score.min()) / (self.score.max() - self.score.min())
        self.score_pool = []
        for i, item in enumerate(reg_score):
            for j in range(int(np.floor(item * 100))):
                self.score_pool.append(self.pop[i])

        self.score_pool = np.array(self.score_pool)

        self.new_generation = []
        for i in range(self.pop_len // 2):
            r1 = np.random.randint(0, len(self.score_pool))
            r2 = np.random.randint(0, len(self.score_pool))
            parent1 = self.score_pool[r1]
            parent2 = self.score_pool[r2]

            child1, child2 = self.cross_over(parent1, parent2)
            self.new_generation.append(child1)
            self.new_generation.append(child2)

        self.new_generation = np.array(self.new_generation)
        self.pop = np.array([self.mutation(c) for c in self.new_generation])
        self.generation_num += 1


    def evaluate(self):
        dna = DNA().cromosome
        dna_len = len(dna)
        # print('maxxxxxx:', np.power(dna_len-1 + dna_len, 2))
        if self.score.max() >= np.power(dna_len-1 + dna_len, 2):
            raise ValueError('Answer!')
        elif self.max_iter == self.generation_num+1:
            raise ValueError('max iter!')


    def get_answer(self):
        max_score = self.score.argmax()
        return (self.pop[max_score], self.score[max_score])


if __name__ == '__main__':
    population = main(50, 0.05, 10000)
    population.initialize()
    population.fitness_measure()

    while True:
        try:
            population.selection()
            population.fitness_measure()
            population.evaluate()
            print('generation : {}  , average fitness : {}    {}'.format(population.generation_num, np.average(population.score), population.get_answer()[0]))
        except ValueError as e:
            if str(e) == 'low population':
                print('\n\n', e)
                break
            else:
                print(e)
                Answer = population.get_answer()
                print('\n\ngeneration : {}  , Answer fitness : {}    {}'.format(population.generation_num, Answer[1], Answer[0]))
                # print(population.fitness(Answer[0]))
                break
