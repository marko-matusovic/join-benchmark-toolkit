from benchmark.operations.get import get_approx_time_instructions
from benchmark.operations.get import get_real_instructions
from benchmark.util import get_stats, print_write
from benchmark.engine.engine import get_engine

def main(query):
    in_file = open(f"results/{query}.csv", "r")
    out_file = open(f"results/{query}-approx.csv", "w")
    # print_write(f'Started running benchmark for query {query}.', out_file)
    print(f'Started running benchmark for query {query}.')
    
    stats = get_engine().read_csv(in_file, sep=";")
    
    instructions = get_real_instructions(query)
    approx_ins = get_approx_time_instructions(query)

    run_all_jobs(instructions, approx_ins, out_file, stats)
    
    print(f'Done')
    
def run_all_jobs(instructions, approx_ins, out_file, stats):
    
    dfs = instructions[0][0]()
    approx_data = {
        "stats": {key: get_stats(dfs[key]) for key in dfs},
        "times": {}
    }
    
    print_write(f'permutation;actual_time;approx_time', out_file)
    for (i, job) in enumerate(stats['permutation']):
        job = [int(j) for j in job[1:-1].split(" ")]
        
        dfs = instructions[0][0]()
        approx_data["schema"] = approx_ins[0][0]()
        
        
        ac_t = stats['actual_time'][i]
        print(f'actual={ac_t:5f}', end=", ")
        
        approx_time = 0
        for ins in job:
            t = approx_ins[1][ins](approx_data)
            print(f'ins[{ins}]={t:5f}', end=", ")
            approx_time += t
        print()

        print_write(f'{job};{ac_t};{approx_time}', out_file)
