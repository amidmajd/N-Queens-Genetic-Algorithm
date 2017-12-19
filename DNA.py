import numpy as np

class main():
    def __init__(self, n):
        # n = 16
        self.cromosome = np.random.randint(n, size=n)


if __name__ == '__main__':
    dna = main(16).cromosome
    print(dna)
    print('DNA len:', len(dna))
