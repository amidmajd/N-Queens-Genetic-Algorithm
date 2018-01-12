from matplotlib import pyplot as plt
import numpy as np
import time
from DNA import main as DNA


class main():
    def __init__(self, dna_n, pop_len, mutation_rate, max_iter):
        if pop_len%2 == 0:
            self.pop_len = pop_len
        else:
            self.pop_len = pop_len + 1
        self.mut_rate = mutation_rate
        self.max_iter = max_iter
        self.pop = []
        self.score = np.zeros((self.pop_len))
        self.generation_num = 0
        self.dna_n = dna_n


    def initialize(self):
        for c in range(self.pop_len):
            dna = DNA(self.dna_n).cromosome
            self.pop.append(dna)
        self.pop = np.array(self.pop)
        # print(self.pop.shape)


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
        self.max_score = np.power(dna_len + dna_len*(dna_len-1) , 2)
        # print('maxxxxxx:', self.max_score)

        for c, cromosome in enumerate(self.pop):
            self.score[c] = self.fitness(cromosome)
        # print('min:', self.score.min())
        # print('max:', self.score.max())
        # print('avg:', np.average(self.score))


    def cross_over(self, p1, p2):
        dna = DNA(self.dna_n).cromosome
        random_point = np.random.randint(0, len(dna))
        c1 = np.concatenate([np.array(p1[:random_point]) , np.array(p2[random_point:])])
        c2 = np.concatenate([np.array(p2[:random_point]) , np.array(p1[random_point:])])
        return c1, c2


    def mutation(self, cromosome):
        for g, gen in enumerate(cromosome):
            r = np.random.rand()
            if r < self.mut_rate:
                dna = DNA(self.dna_n).cromosome
                random_g = np.random.choice(dna)
                while random_g == gen and list(cromosome).count(random_g) != 1:
                    random_g = np.random.choice(dna)
                else:
                    cromosome[g] = random_g
        return cromosome


    def selection(self):
        if self.score.max() - self.score.min() == 0:
            raise ValueError('Bad Population')
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

            while (parent1 == parent2).all():
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
        if self.score.max() >= self.max_score:
            raise ValueError('Answer!')
        elif self.max_iter == self.generation_num:
            raise ValueError('max iter!')


    def get_answer(self):
        max_score = self.score.argmax()
        return (self.pop[max_score], self.score[max_score])


if __name__ == '__main__':
    t0 = time.time()
    population = main(16, 350, 0.01, 10000)
    population.initialize()
    population.fitness_measure()

    while True:
        try:
            population.selection()
            population.fitness_measure()
            population.evaluate()
            avg_score = np.average(population.score)
            print('generation : {0:5d}  ,  average fitness : {1:.2f} == {2:.2f}%    {3}'.format(population.generation_num, avg_score, (avg_score/population.max_score)*100, population.get_answer()[0]))
        except ValueError as e:
            if str(e) == 'Bad Population':
                print('\n\n', e)
                break
            else:
                print(e)
                Answer = population.get_answer()
                print('\n\ngeneration : {0:5d}  ,  Answer fitness : {1:.2f} == {2:.2f}%    {3}'.format(population.generation_num, Answer[1], (Answer[1]/population.max_score)*100, Answer[0]))
                print('Time : {}s'.format(round(time.time() - t0, 2)))
                # print(population.fitness(Answer[0]))
                break
