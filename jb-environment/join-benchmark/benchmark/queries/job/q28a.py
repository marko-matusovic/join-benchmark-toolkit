from typing import TypeVar
from benchmark.operations.query_instructions import QueryInstructions
from benchmark.operations.operations import Operations

# SELECT MIN(cn.name) AS movie_company,
#        MIN(mi_idx.info) AS rating,
#        MIN(t.title) AS complete_euro_dark_movie
# FROM complete_cast AS cc,
#      comp_cast_type AS cct1,
#      comp_cast_type AS cct2,
#      company_name AS cn,
#      company_type AS ct,
#      info_type AS it1,
#      info_type AS it2,
#      keyword AS k,
#      kind_type AS kt,
#      movie_companies AS mc,
#      movie_info AS mi,
#      movie_info_idx AS mi_idx,
#      movie_keyword AS mk,
#      title AS t
# WHERE cct1.kind = 'crew'
#   AND cct2.kind != 'complete+verified'
#   AND cn.country_code != '[us]'
#   AND it1.info = 'countries'
#   AND it2.info = 'rating'
#   AND k.keyword IN ('murder',
#                     'murder-in-title',
#                     'blood',
#                     'violence')
#   AND kt.kind IN ('movie',
#                   'episode')
#   AND mc.note NOT LIKE '%(USA)%'
#   AND mc.note LIKE '%(200%)%'
#   AND mi.info IN ('Sweden',
#                   'Norway',
#                   'Germany',
#                   'Denmark',
#                   'Swedish',
#                   'Danish',
#                   'Norwegian',
#                   'German',
#                   'USA',
#                   'American')
#   AND mi_idx.info < '8.5'
#   AND t.production_year > 2000
#   AND kt.id = t.kind_id
#   AND t.id = mi.movie_id
#   AND t.id = mk.movie_id
#   AND t.id = mi_idx.movie_id
#   AND t.id = mc.movie_id
#   AND t.id = cc.movie_id
#   AND mk.movie_id = mi.movie_id
#   AND mk.movie_id = mi_idx.movie_id
#   AND mk.movie_id = mc.movie_id
#   AND mk.movie_id = cc.movie_id
#   AND mi.movie_id = mi_idx.movie_id
#   AND mi.movie_id = mc.movie_id
#   AND mi.movie_id = cc.movie_id
#   AND mc.movie_id = mi_idx.movie_id
#   AND mc.movie_id = cc.movie_id
#   AND mi_idx.movie_id = cc.movie_id
#   AND k.id = mk.keyword_id
#   AND it1.id = mi.info_type_id
#   AND it2.id = mi_idx.info_type_id
#   AND ct.id = mc.company_type_id
#   AND cn.id = mc.company_id
#   AND cct1.id = cc.subject_id
#   AND cct2.id = cc.status_id;

I = TypeVar('I')
O = TypeVar('O')

def instruction_set(operation_set: Operations[I,O]) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init = operation_set.from_tables('job', ['complete_cast', 'comp_cast_type', 'comp_cast_type', 'company_name', 'company_type', 'info_type', 'info_type', 'keyword', 'kind_type','movie_companies', 'movie_info', 'movie_info_idx', 'movie_keyword', 'title',], ['cc', 'cct1', 'cct2', 'cn', 'ct', 'it1', 'it2', 'k', 'kt', 'mc', 'mi', 'mi_idx', 'mk', 't',]),
        s2_filters = [
            operation_set.filter_field_eq('cct1.kind', ['crew']),
            operation_set.filter_field_ne('cct2.kind', 'complete+verified'),
            operation_set.filter_field_ne('cn.country_code', '[us]'),
            operation_set.filter_field_eq('it1.info', ['countries']),
            operation_set.filter_field_eq('it2.info', ['rating']),
            operation_set.filter_field_eq('k.keyword', ['murder', 'murder-in-title', 'blood', 'violence']),
            operation_set.filter_field_eq('kt.kind', ['movie', 'episode']),
            operation_set.filter_field_not_like('mc.note', '%(USA)%'),
            operation_set.filter_field_like('mc.note', ['%(200%)%']),
            operation_set.filter_field_eq('mi.info', ['Sweden', 'Norway', 'Germany', 'Denmark', 'Swedish', 'Danish', 'Norwegian', 'German', 'USA', 'American']),
            operation_set.filter_field_lt('mi_idx.info', '8.5'),
            operation_set.filter_field_gt('t.production_year', 2000)
        ],
        s3_joins = [  # 0 JOINS
            operation_set.join_fields('kt.id', 't.kind_id'),
            operation_set.join_fields('t.id', 'mi.movie_id'),
            operation_set.join_fields('t.id', 'mk.movie_id'),
            operation_set.join_fields('t.id', 'mi_idx.movie_id'),
            operation_set.join_fields('t.id', 'mc.movie_id'),
            operation_set.join_fields('t.id', 'cc.movie_id'),
            operation_set.join_fields('mk.movie_id', 'mi.movie_id'),
            operation_set.join_fields('mk.movie_id', 'mi_idx.movie_id'),
            operation_set.join_fields('mk.movie_id', 'mc.movie_id'),
            operation_set.join_fields('mk.movie_id', 'cc.movie_id'),
            operation_set.join_fields('mi.movie_id', 'mi_idx.movie_id'),
            operation_set.join_fields('mi.movie_id', 'mc.movie_id'),
            operation_set.join_fields('mi.movie_id', 'cc.movie_id'),
            operation_set.join_fields('mc.movie_id', 'mi_idx.movie_id'),
            operation_set.join_fields('mc.movie_id', 'cc.movie_id'),
            operation_set.join_fields('mi_idx.movie_id', 'cc.movie_id'),
            operation_set.join_fields('k.id', 'mk.keyword_id'),
            operation_set.join_fields('it1.id', 'mi.info_type_id'),
            operation_set.join_fields('it2.id', 'mi_idx.info_type_id'),
            operation_set.join_fields('ct.id', 'mc.company_type_id'),
            operation_set.join_fields('cn.id', 'mc.company_id'),
            operation_set.join_fields('cct1.id', 'cc.subject_id'),
            operation_set.join_fields('cct2.id', 'cc.status_id'),
        ],
        s4_aggregation = [
            # select
        ]
    )
