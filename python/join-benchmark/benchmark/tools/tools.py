def clone(dfs):
    return {key: dfs[key].copy() for key in dfs}

def print_write(msg, out_file):
    print(msg)
    out_file.write(f'{msg}\n')
    out_file.flush()
    
def bound(low, value, high):
    return max(low, min(high, value))