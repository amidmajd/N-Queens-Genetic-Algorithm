import numpy as np

class main():
    def __init__(self):
        n = 8
        self.cromosome = np.random.randint(n-1, size=n)


if __name__ == '__main__':
    dna = main().cromosome
    print(dna)
    print('DNA len:', len(dna))
