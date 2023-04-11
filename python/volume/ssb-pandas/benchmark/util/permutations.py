import itertools
import numpy as np

if __name__ == '__main__':
    for n in range(1, 9):
        perms = np.array([i for i in itertools.permutations(range(n))])
        np.random.shuffle(perms)
        with open(f'scripts/perms/{n}.csv', "w") as file:
            for p in perms:
                file.write(",".join([str(i) for i in p])+'\n')