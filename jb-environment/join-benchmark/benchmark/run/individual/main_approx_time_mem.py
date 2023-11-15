from benchmark.operations.get_query_instructions import get_time_mem_approx_instructions

def main(db_path:str, db_set:str, query:str, perm:list[int]):
    print(f'Running {db_set}/{query} with perm {perm}')
    
    instructions = get_time_mem_approx_instructions(db_path, db_set, query)

    # Load and initialize
    data = instructions.s1_init()
    
    # Apply filters
    for instruction in instructions.s2_filters:
        instruction(data)

    t_total = 0
    m_sum = 0
    m_max = 0
    # Approximate joins
    for p in perm:
        (t_cost, m_cost) = instructions.s3_joins[p](data)
        t_total += t_cost
        m_sum += m_cost
        m_max = max(m_max, m_cost)

    # Save results 
    with open(f'results/approx_time_mem/{db_set}/{query}.csv', 'a') as file:
        formated_perm = ",".join([str(p) for p in perm])
        file.write(f'{formated_perm};{t_total};{m_sum};{m_max}\n')
