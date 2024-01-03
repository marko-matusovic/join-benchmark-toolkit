from typing import TypeVar
from benchmark.operations.query_instructions import QueryInstructions
from benchmark.operations.operations import Operations

# SELECT MIN(mc.note) AS production_note,
#        MIN(t.title) AS movie_title,
#        MIN(t.production_year) AS movie_year
# FROM company_type AS ct,
#      info_type AS it,
#      movie_companies AS mc,
#      movie_info_idx AS mi_idx,
#      title AS t
# WHERE ct.kind = 'production companies'
#   AND it.info = 'bottom 10 rank'
#   AND mc.note NOT LIKE '%(as Metro-Goldwyn-Mayer Pictures)%'
#   AND t.production_year BETWEEN 2005 AND 2010
#   AND ct.id = mc.company_type_id
#   AND t.id = mc.movie_id
#   AND t.id = mi_idx.movie_id
#   AND mc.movie_id = mi_idx.movie_id
#   AND it.id = mi_idx.info_type_id;

I = TypeVar("I")
O = TypeVar("O")


def instruction_set(
    db_path: str, operation_set: Operations[I, O]
) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init=operation_set.from_tables(
            db_path,
            "job",
            ["company_type", "info_type", "movie_companies", "movie_info_idx", "title"],
            ["ct", "it", "mc", "mi_idx", "t"],
        ),
        s2_filters=[
            operation_set.filter_field_eq("ct.kind", ["production companies"]),
            operation_set.filter_field_eq("it.info", ["bottom 10 rank"]),
            operation_set.filter_field_not_like(
                "mc.note", "%(as Metro-Goldwyn-Mayer Pictures)%"
            ),
            operation_set.filter_field_ge("t.production_year", 2005),
            operation_set.filter_field_le("t.production_year", 2010),
        ],
        s3_joins=[  # 5 JOINS
            operation_set.join_fields("ct.id", "mc.company_type_id"),
            operation_set.join_fields("t.id", "mc.movie_id"),
            operation_set.join_fields("t.id", "mi_idx.movie_id"),
            operation_set.join_fields("mc.movie_id", "mi_idx.movie_id"),
            operation_set.join_fields("it.id", "mi_idx.info_type_id"),
        ],
        s4_aggregation=[
            # select
        ],
    )
