def clone(dfs):
    return {key: dfs[key].copy() for key in dfs}

def print_write(msg, out_file):
    print(msg)
    out_file.write(f'{msg}\n')
    out_file.flush()
    
def get_stats(df):
    return {
        "length": len(df.index),
        "unique": dict(df.nunique())
    }