from typing import Callable, Generic

from pyparsing import TypeVar

from benchmark.operations.instructions import TDFs
from benchmark.operations.time_mem_approximations import Data, TRes

I = TypeVar("I")
O = TypeVar("O")


class QueryInstructions(Generic[I, O]):
    def __init__(
        self,
        s1_init: Callable[[], I],
        s2_filters: list[Callable[[I], O]] = [],
        s3_joins: list[Callable[[I], O]] = [],
        s4_aggregation: list[Callable[[I], O]] = [],
    ):
        self.s1_init = s1_init
        self.s2_filters = s2_filters
        self.s3_joins = s3_joins
        self.s4_aggregation = s4_aggregation
