# type: ignore
# ignoring types, because pymoo doesn't support them
import time
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.operators.sampling.rnd import PermutationRandomSampling
from pymoo.operators.crossover.ox import OrderCrossover
from pymoo.operators.mutation.inversion import InversionMutation
from pymoo.termination.default import DefaultMultiObjectiveTermination

from benchmark.operations.query_instructions_service import get_instruction_set


class Join_Order_Cost_Model:
    def __init__(self, db_path: str, db_name: str, query_name: str):
        instructions = get_time_mem_approx_instructions(db_path, db_name, query_name)

        # Load and initialize
        data = instructions.s1_init()

        # Filters
        for instruction in instructions.s2_filters:
            instruction(data)

        self.data = data
        self.joins = instructions.s3_joins

    def evaluate(self, join_order: list[int]):
        # assert len(join_order) == len(self.joins)

        orig_schema = self.data.schema.copy()

        t_total = 0
        m_total = 0
        for j in join_order:
            (t_cost, m_cost) = self.joins[j](self.data)
            t_total += t_cost
            m_total += m_cost

        self.data = self.data._replace(schema=orig_schema)
        self.data = self.data._replace(history=[])

        return (t_total, m_total)


class Join_Order_Problem(ElementwiseProblem):
    def __init__(self, db_path: str, db_name: str, query_name: str):
        self.cost_model = Join_Order_Cost_Model(db_path, db_name, query_name)
        n_joins = len(self.cost_model.joins)
        xl = np.zeros(n_joins)
        xu = np.ones(n_joins) * (n_joins - 1)
        super().__init__(
            elementwise=True,
            n_var=n_joins,
            n_obj=2,
            n_ieq_constr=0,
            n_eq_constr=0,
            xl=xl,
            xu=xu,
        )

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = self.cost_model.evaluate(x)


def main(db_path: str, db_name: str, query_name: str):
    problem = Join_Order_Problem(db_path, db_name, query_name)

    algorithm = NSGA2(
        pop_size=20,
        sampling=PermutationRandomSampling(),
        mutation=InversionMutation(),
        crossover=OrderCrossover(),
        eliminate_duplicates=True,
    )

    result = minimize(problem, algorithm, verbose=False)

    # plot = Scatter()
    # plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
    # plot.add(result.F, facecolor="none", edgecolor="red")
    # plot.show()

    with open(f"results/optimization/{db_name}/{query_name}.csv", "a") as file:
        file.write(f"\\\\Timestamp {time.ctime()}\n")
        file.write("permutation;time_cost;memory_sum_cost\n")
        for perm, [t, m] in zip(result.X, result.F):
            file.write(f'{",".join([p.__str__() for p in perm])};{t};{m}\n')
