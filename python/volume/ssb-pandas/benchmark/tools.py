from pandas import DataFrame


def clone(dfs: dict[str, DataFrame]) -> dict[str, DataFrame]:
    return {key: dfs[key].copy() for key in dfs}

def print_write(msg, out_file):
    print(msg)
    out_file.write(f'{msg}\n')
    out_file.flush()