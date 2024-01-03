import random
import numpy as np
import string
import pandas as pd
import time

RANDOM_SEED = 2454359


def main():
    print("Generating Tables")

    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    for sz, size in [("sm", 1_000), ("md", 100_000), ("lg", 10_000_000)]:
        print(f"Working on scale {sz}")
        ts = time.time()
        print(f"Generating keys")
        primary_keys = list(range(size))
        keys_a = shuffle(primary_keys)
        keys_b = shuffle(primary_keys)

        refs_a = shuffle(primary_keys)[: size // 10]
        refs_b = shuffle(
            refs_a[: size // 100 * 3] + shuffle(primary_keys)[: size // 100 * 7]
        )

        # keys_a x keys_b = 1 to 1
        # keys_a x refs_b = 1 to n
        # refs_a x keys_b = n to 1
        # refs_a x refs_b = n to n

        print("Constructing DataFrames")
        df_a = pd.DataFrame(
            {
                "key": keys_a,
                "value": generate_random_strings(size),
                "ref": np.random.choice(refs_a, size),
            }
        )

        df_b = pd.DataFrame(
            {
                "key": keys_b,
                "value": generate_random_strings(size),
                "ref": np.random.choice(refs_b, size),
            }
        )

        print("Saving to CSV")
        df_a.to_csv(f"tables/table_a_{sz}.csv", index=False, header=False)
        df_b.to_csv(f"tables/table_b_{sz}.csv", index=False, header=False)

        print(f"Took {time.time() - ts}s")

    print("Finished")


def shuffle(lst: list[int]) -> list[int]:
    cln = lst.copy()
    random.shuffle(cln)
    return cln


def generate_random_strings(length, str_len=64):
    letters = np.array(list(string.ascii_letters + string.digits))
    return ["".join(np.random.choice(letters, str_len)) for _ in range(length)]


if __name__ == "__main__":
    main()
