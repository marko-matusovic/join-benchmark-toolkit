from abc import ABC, abstractmethod

class Operations(ABC):
    @abstractmethod
    def from_tables(self, db_name, tables, aliases=[]):
        ...

    @abstractmethod
    def join_fields(self, field_name_1, field_name_2):
        ...

    @abstractmethod
    def filter_field_eq(self, field_name, values):
        ...

    @abstractmethod
    def filter_field_ne(self, field_name, value):
        ...

    @abstractmethod
    def filter_field_ge(self, field_name, value):
        ...

    @abstractmethod
    def filter_field_gt(self, field_name, value):
        ...

    @abstractmethod
    def filter_field_le(self, field_name, value):
        ...

    @abstractmethod
    def filter_field_lt(self, field_name, value):
        ...

    @abstractmethod
    def filter_field_like(self, field_name, values):
        ...

    @abstractmethod
    def filter_field_not_like(self, field_name, value):
        ...
