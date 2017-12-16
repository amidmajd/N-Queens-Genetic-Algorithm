from matplotlib import pyplot as plt
import numpy as np
import time
from DNA import main as DNA
from population import main as Population


pop_len  = 200
mut_rate = 0.02
max_iter = 1000

t0 = time.time()
population = Population(pop_len=pop_len, mutation_rate=mut_rate, max_iter=max_iter)
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
        if str(e) == 'low population':
            print('\n\n', e)
            break
        else:
            print(e)
            Answer = population.get_answer()
            print('\n\ngeneration : {0:5d}  ,  Answer fitness : {1:.2f} == {2:.2f}%    {3}'.format(population.generation_num, Answer[1], (Answer[1]/population.max_score)*100, Answer[0]))
            print('Time : {}s'.format(round(time.time() - t0, 2)))
            # print(population.fitness(Answer[0]))

            dna = DNA().cromosome
            plot_ans = np.zeros((len(dna), len(dna)), dtype=np.int)
            for g, gen in enumerate(Answer[0]):
                plot_ans[gen, g] = 1
            # print(plot_ans)

            plt.imshow(plot_ans,cmap='gray')
            plt.title('{} Queens'.format(len(dna)))
            # plt.grid(False)
            plt.xticks(range(len(dna)), range(len(dna)))
            plt.yticks(range(len(dna)), range(len(dna)))
            plt.tight_layout()
            plt.show()

            break
