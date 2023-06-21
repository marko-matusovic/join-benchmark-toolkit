from typing import Any, Callable, Generic, NamedTuple, TypeVar


I = TypeVar("I")
O = TypeVar("O")


class QueryInstructions(NamedTuple, Generic[I, O]):
    s1_init: Callable[[], I]
    s2_filters: list[Callable[[I], Any]]
    s3_joins: list[Callable[[I], O]]
    s4_aggregation: list[Callable[[I], Any]]
