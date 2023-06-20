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
    def filter_field_eq(self, field_name: str, values: list[TVal]) -> Callable[[I], O]:
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
