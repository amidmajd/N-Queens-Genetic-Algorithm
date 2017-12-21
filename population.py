from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import time
sns.set()
from DNA import main as DNA


class main():
    def __init__(self, dna_n, pop_len, mutation_rate, max_iter):
        if pop_len%2 == 0:
            self.pop_len = pop_len
        else:
            self.pop_len = pop_len - 1
        self.mut_rate = mutation_rate
        self.max_iter = max_iter
        self.pop = []
        self.score = np.zeros((self.pop_len))
        self.generation_num = 0
        self.dna_n = dna_n
        self.max_score = np.power(self.dna_n + self.dna_n*(self.dna_n-1) , 2)



    def sort(self):
        self.pop = np.array(sorted(list(self.pop), key=self.fitness, reverse=True))


    def initialize(self):
        for c in range(self.pop_len):
            dna = DNA(self.dna_n).cromosome
            self.pop.append(dna)
        self.pop = np.array(self.pop)
        self.sort()


    def fitness(self, cromosome):
        score = 0
        # row or col check
        score += len(np.unique(cromosome))

        # diagonal check
        for i in range(len(cromosome)):
            for j in range(len(cromosome)):
                if i != j:
                    dx = abs(i - j)
                    dy = abs(cromosome[i] - cromosome[j])
                    if dx != dy:
                        score += 1

        return np.power(score, 2)


    def fitness_measure(self):
        dna_len = len(DNA(self.dna_n).cromosome)
        # print('maxxxxxx:', self.max_score)

        for c, cromosome in enumerate(self.pop):
            self.score[c] = self.fitness(cromosome)
        # print('min:', self.score.min())
        # print('max:', self.score.max())
        # print('avg:', np.average(self.score))


    def cross_over(self, p1, p2):
        if (p1 == p2).all():
            p2 = DNA(self.dna_n).cromosome

        possible = [x for x in range(self.dna_n)]
        c = [-1] * self.dna_n

        for i in range(self.dna_n):
            if p1[i] == p2[i]:
                try:
                    possible.remove(c[i])
                    c[i] = p1[i]
                except:
                    pass

        for i in range(self.dna_n):
            if c[i] == -1:
                c[i] = np.random.choice(possible)
                try:
                    possible.remove(c[i])
                except:
                    pass

        return np.array(c)


    def mutation(self, cromosome):
        r = np.random.random()
        if r < self.mut_rate:
            indx1 = np.random.randint(0, self.dna_n)
            indx2 = np.random.randint(0, self.dna_n)
            cromosome[indx1], cromosome[indx2] = cromosome[indx2], cromosome[indx1]
        return cromosome


    def selection(self):
<<<<<<< HEAD
        self.new_generation = []
=======
        if self.score.max() - self.score.min() == 0:
            raise ValueError('low population')
        # print((self.score.max() - self.score.min()))
        reg_score = (self.score - self.score.min()) / (self.score.max() - self.score.min())
        self.score_pool = []
        for i, item in enumerate(reg_score):
            for j in range(int(np.floor(item * 100))):
                self.score_pool.append(self.pop[i])
>>>>>>> parent of 5065615... plot completed succesfully :+1:

        for i in range(self.pop_len):
            ppc = np.random.randint(0, self.pop_len, size=3)
            ppc.sort()

            p1 = self.pop[ppc[0]]
            p2 = self.pop[ppc[1]]
            old_c = ppc[2]

            new_c = self.cross_over(p1, p2)
            new_c = self.mutation(new_c)

            self.pop[old_c] = new_c
            self.sort()
        self.generation_num += 1

        #
        # p = np.divide(self.score, self.score.sum())
        #
        # for i in range(self.pop_len // 2):
        #     parent1 = self.pop[np.random.choice(range(self.pop_len), p=p)]
        #     parent2 = self.pop[np.random.choice(range(self.pop_len), p=p)]
        #
        #     while (parent1 == parent2).all():
        #         parent1 = self.pop[np.random.choice(range(self.pop_len), p=p)]
        #         parent2 = self.pop[np.random.choice(range(self.pop_len), p=p)]
        #
        #     child1, child2 = self.cross_over(parent1, parent2)
        #     # child1, child2 = self.mutation(child1), self.mutation(child2)
        #     self.new_generation.append(child1)
        #     self.new_generation.append(child2)

        # # for i in range(self.pop_len - len(self.new_generation)):
        # #     r = np.random.randint(0, self.pop_len)
        # #     self.new_generation.append(self.pop[r])
        #
        # self.new_generation = np.array(self.new_generation)
        # self.generation_num += 1
        # self.pop = np.array([self.mutation(c) for c in self.new_generation])
        # self.pop = np.array(self.new_generation)


    def evaluate(self):
        if self.fitness(self.pop[0]) >= self.max_score:
            raise ValueError('Answer!')
        elif self.max_iter == self.generation_num:
            raise ValueError('max iter!')


    def get_answer(self):
        return (self.pop[0], self.fitness(self.pop[0]))


if __name__ == '__main__':
    t0 = time.time()
    population = main(16, 10, 0.001, 100000)
    population.initialize()

    while True:
        try:
            population.selection()
            # population.fitness_measure()
            population.evaluate()
            avg_score = population.fitness(population.pop[0])
            if population.generation_num % 100 == 0:
                print('generation : {0:5d}  , fitness : {1:.2f} == {2:.2f}%    {3}'.format(population.generation_num, avg_score, (avg_score/population.max_score)*100, population.get_answer()[0]))
        except ValueError as e:
            if str(e) == 'low population':
                print('\n\n', e)
                break
            else:
                print(e)
                Answer = population.get_answer()
                print('\n\ngeneration : {0:5d}  ,  Answer fitness : {1:.2f} == {2:.2f}%    {3}'.format(population.generation_num, Answer[1], (Answer[1]/population.max_score)*100, Answer[0]))
                print('Time : {}s'.format(round(time.time() - t0, 2)))
                # print(population.fitness(Answer[0]))
                break
