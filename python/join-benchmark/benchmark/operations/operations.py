from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeAlias, TypeVar

I = TypeVar('I')
O = TypeVar('O')

TVal: TypeAlias = str | int | float | bool


class Operations(ABC, Generic[I, O]):

    @abstractmethod
    def from_tables(self, db_name: str, tables: list[str], aliases: list[str] = []) -> Callable[[], I]:
        ...

    @abstractmethod
    def join_fields(self, field_name_1: str, field_name_2: str) -> Callable[[I], O]:
        ...

    @abstractmethod
    def filter_field_eq(self, field_name: str, values: TVal | list[TVal]) -> Callable[[I], O]:
        ...

    @abstractmethod
    def filter_field_ne(self, field_name: str, value: TVal) -> Callable[[I], O]:
        ...

    @abstractmethod
    def filter_field_ge(self, field_name: str, value: TVal) -> Callable[[I], O]:
        ...

    @abstractmethod
    def filter_field_gt(self, field_name: str, value: TVal) -> Callable[[I], O]:
        ...

    @abstractmethod
    def filter_field_le(self, field_name: str, value: TVal) -> Callable[[I], O]:
        ...

    @abstractmethod
    def filter_field_lt(self, field_name: str, value: TVal) -> Callable[[I], O]:
        ...

    @abstractmethod
    def filter_field_like(self, field_name: str, values: list[str]) -> Callable[[I], O]:
        ...

    @abstractmethod
    def filter_field_not_like(self, field_name: str, value: str) -> Callable[[I], O]:
        ...

    def get_filter(self, op:str):
        ops = {
            'NOT LIKE': self.filter_field_not_like,
            'LIKE': self.filter_field_like,
            'IN': self.filter_field_eq,
            '=': self.filter_field_eq,
            '!=': self.filter_field_ne,
            '<=': self.filter_field_le,
            '<': self.filter_field_lt,
            '>': self.filter_field_gt,
            '>=': self.filter_field_ge,
        }
        if op not in ops:
            print(f"ERROR: Unknown operator '{op}' found!")
            exit(1)
        return ops[op]