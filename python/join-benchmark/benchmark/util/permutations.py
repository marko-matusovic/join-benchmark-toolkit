import itertools
import numpy as np
from math import factorial
import sys

COUNT = 10_000

def main():
    if len(sys.argv) > 1:
        save(int(sys.argv[1]))
    else:
        for n in range(1, 21):
            save(n)

def save(n:int):
    print(f"working on {n}.")
    perms = gen_all(n) if factorial(n-1) < COUNT else gen_seq(n)
    with open(f'scripts/perms/{n}.csv', "w") as file:
        for p in perms[:COUNT]:
            file.write(",".join([str(i) for i in p])+'\n')

def gen_all(n:int):
    perms = np.array([i for i in itertools.permutations(range(n))])
    np.random.shuffle(perms)
    return perms

def gen_seq(n:int) -> list[list[int]]:
    perms:list[list[int]] = []
    while len(perms) < COUNT:
        p = np.arange(n) # type: ignore
        np.random.shuffle(p)
        while list(p) in perms:
            np.random.shuffle(p)
        perms.append(list(p))
    return perms

if __name__ == '__main__':
    main()