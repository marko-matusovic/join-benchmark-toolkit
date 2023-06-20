from typing import TypeVar
from benchmark.operations.get import QueryInstructions
from benchmark.operations.operations import Operations

# SELECT MIN(t.title) AS complete_downey_ironman_movie
# FROM complete_cast AS cc,
#      comp_cast_type AS cct1,
#      comp_cast_type AS cct2,
#      char_name AS chn,
#      cast_info AS ci,
#      keyword AS k,
#      kind_type AS kt,
#      movie_keyword AS mk,
#      name AS n,
#      title AS t
# WHERE cct1.kind = 'cast'
#   AND cct2.kind LIKE '%complete%'
#   AND chn.name NOT LIKE '%Sherlock%'
#   AND (chn.name LIKE '%Tony%Stark%'
#        OR chn.name LIKE '%Iron%Man%')
#   AND k.keyword IN ('superhero',
#                     'sequel',
#                     'second-part',
#                     'marvel-comics',
#                     'based-on-comic',
#                     'tv-special',
#                     'fight',
#                     'violence')
#   AND kt.kind = 'movie'
#   AND t.production_year > 1950
#   AND kt.id = t.kind_id
#   AND t.id = mk.movie_id
#   AND t.id = ci.movie_id
#   AND t.id = cc.movie_id
#   AND mk.movie_id = ci.movie_id
#   AND mk.movie_id = cc.movie_id
#   AND ci.movie_id = cc.movie_id
#   AND chn.id = ci.person_role_id
#   AND n.id = ci.person_id
#   AND k.id = mk.keyword_id
#   AND cct1.id = cc.subject_id
#   AND cct2.id = cc.status_id;

I = TypeVar('I')
O = TypeVar('O')

def instruction_set(operation_set: Operations[I,O]) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init = operation_set.from_tables('job', ['complete_cast','comp_cast_type','comp_cast_type','char_name','cast_info','keyword','kind_type','movie_keyword','name','title'], ['cc','cct1','cct2','chn','ci','k','kt','mk','n','t']),
        s2_filters = [
            operation_set.filter_field_eq('cct1.kind', ['cast']),
            operation_set.filter_field_like('cct2.kind', ['%complete%']),
            operation_set.filter_field_not_like('chn.name', '%Sherlock%'),
            operation_set.filter_field_like('chn.name', ['%Tony%Stark%', '%Iron%Man%']),
            operation_set.filter_field_eq('k.keyword', ['superhero','sequel','second-part','marvel-comics','based-on-comic','tv-special','fight','violence']),
            operation_set.filter_field_eq('kt.kind', ['movie']),
            operation_set.filter_field_gt('t.production_year', 1950)
        ],
        s3_joins = [ # 12 JOINS
            operation_set.join_fields('kt.id', 't.kind_id'),
            operation_set.join_fields('t.id', 'mk.movie_id'),
            operation_set.join_fields('t.id', 'ci.movie_id'),
            operation_set.join_fields('t.id', 'cc.movie_id'),
            operation_set.join_fields('mk.movie_id', 'ci.movie_id'),
            operation_set.join_fields('mk.movie_id', 'cc.movie_id'),
            operation_set.join_fields('ci.movie_id', 'cc.movie_id'),
            operation_set.join_fields('chn.id', 'ci.person_role_id'),
            operation_set.join_fields('n.id', 'ci.person_id'),
            operation_set.join_fields('k.id', 'mk.keyword_id'),
            operation_set.join_fields('cct1.id', 'cc.subject_id'),
            operation_set.join_fields('cct2.id', 'cc.status_id'),
        ],
        s4_aggregation = [
            # select
        ]
    )
