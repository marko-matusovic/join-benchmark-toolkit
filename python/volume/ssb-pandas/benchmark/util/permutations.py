import itertools
import numpy as np
from math import factorial

COUNT = 10_000

def main():
    for n in range(1, 21):
        print(f"working on {n}.")
        perms = gen_all(n) if factorial(n-1) < COUNT else gen_seq(n)
        with open(f'scripts/perms/{n}.csv', "w") as file:
            for p in perms[:COUNT]:
                file.write(",".join([str(i) for i in p])+'\n')

def gen_all(n):
    perms = np.array([i for i in itertools.permutations(range(n))])
    np.random.shuffle(perms)
    return perms

def gen_seq(n):
    perms = []
    while len(perms) < COUNT:
        p = np.arange(n)
        np.random.shuffle(p)
        while list(p) in perms:
            np.random.shuffle(p)
        perms.append(list(p))
    return perms

if __name__ == '__main__':
    main()