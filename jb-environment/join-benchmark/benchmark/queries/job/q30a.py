from typing import TypeVar
from benchmark.operations.query_instructions import QueryInstructions
from benchmark.operations.operations import Operations

# SELECT MIN(mi.info) AS movie_budget,
#        MIN(mi_idx.info) AS movie_votes,
#        MIN(n.name) AS writer,
#        MIN(t.title) AS complete_violent_movie
# FROM complete_cast AS cc,
#      comp_cast_type AS cct1,
#      comp_cast_type AS cct2,
#      cast_info AS ci,
#      info_type AS it1,
#      info_type AS it2,
#      keyword AS k,
#      movie_info AS mi,
#      movie_info_idx AS mi_idx,
#      movie_keyword AS mk,
#      name AS n,
#      title AS t
# WHERE cct1.kind IN ('cast',
#                     'crew')
#   AND cct2.kind ='complete+verified'
#   AND ci.note IN ('(writer)',
#                   '(head writer)',
#                   '(written by)',
#                   '(story)',
#                   '(story editor)')
#   AND it1.info = 'genres'
#   AND it2.info = 'votes'
#   AND k.keyword IN ('murder',
#                     'violence',
#                     'blood',
#                     'gore',
#                     'death',
#                     'female-nudity',
#                     'hospital')
#   AND mi.info IN ('Horror',
#                   'Thriller')
#   AND n.gender = 'm'
#   AND t.production_year > 2000
#   AND t.id = mi.movie_id
#   AND t.id = mi_idx.movie_id
#   AND t.id = ci.movie_id
#   AND t.id = mk.movie_id
#   AND t.id = cc.movie_id
#   AND ci.movie_id = mi.movie_id
#   AND ci.movie_id = mi_idx.movie_id
#   AND ci.movie_id = mk.movie_id
#   AND ci.movie_id = cc.movie_id
#   AND mi.movie_id = mi_idx.movie_id
#   AND mi.movie_id = mk.movie_id
#   AND mi.movie_id = cc.movie_id
#   AND mi_idx.movie_id = mk.movie_id
#   AND mi_idx.movie_id = cc.movie_id
#   AND mk.movie_id = cc.movie_id
#   AND n.id = ci.person_id
#   AND it1.id = mi.info_type_id
#   AND it2.id = mi_idx.info_type_id
#   AND k.id = mk.keyword_id
#   AND cct1.id = cc.subject_id
#   AND cct2.id = cc.status_id;

I = TypeVar('I')
O = TypeVar('O')

def instruction_set(db_path:str, operation_set: Operations[I,O]) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init = operation_set.from_tables(db_path, 'job', ['complete_cast','comp_cast_type','comp_cast_type','cast_info','info_type','info_type','keyword','movie_info','movie_info_idx','movie_keyword','name','title'], ['cc','cct1','cct2','ci','it1','it2','k','mi','mi_idx','mk','n','t']),
        s2_filters = [
            operation_set.filter_field_eq('cct1.kind', ['cast','crew']),
            operation_set.filter_field_eq('cct2.kind', ['complete+verified']),
            operation_set.filter_field_eq('ci.note', ['writer','head writer','written by','story','story editor']),
            operation_set.filter_field_eq('it1.info', ['genres']),
            operation_set.filter_field_eq('it2.info', ['votes']),
            operation_set.filter_field_eq('k.keyword', ['murder','violence','blood','gore','death','female-nudity','hospital']),
            operation_set.filter_field_eq('mi.info', ['Horror','Thriller']),
            operation_set.filter_field_eq('n.gender', ['m']),
            operation_set.filter_field_gt('t.production_year', 2000),
        ],
        s3_joins = [ # 20 JOINS
            operation_set.join_fields('t.id', 'mi.movie_id'),
            operation_set.join_fields('t.id', 'mi_idx.movie_id'),
            operation_set.join_fields('t.id', 'ci.movie_id'),
            operation_set.join_fields('t.id', 'mk.movie_id'),
            operation_set.join_fields('t.id', 'cc.movie_id'),
            operation_set.join_fields('ci.movie_id', 'mi.movie_id'),
            operation_set.join_fields('ci.movie_id', 'mi_idx.movie_id'),
            operation_set.join_fields('ci.movie_id', 'mk.movie_id'),
            operation_set.join_fields('ci.movie_id', 'cc.movie_id'),
            operation_set.join_fields('mi.movie_id', 'mi_idx.movie_id'),
            operation_set.join_fields('mi.movie_id', 'mk.movie_id'),
            operation_set.join_fields('mi.movie_id', 'cc.movie_id'),
            operation_set.join_fields('mi_idx.movie_id', 'mk.movie_id'),
            operation_set.join_fields('mi_idx.movie_id', 'cc.movie_id'),
            operation_set.join_fields('mk.movie_id', 'cc.movie_id'),
            operation_set.join_fields('n.id', 'ci.person_id'),
            operation_set.join_fields('it1.id', 'mi.info_type_id'),
            operation_set.join_fields('it2.id', 'mi_idx.info_type_id'),
            operation_set.join_fields('k.id', 'mk.keyword_id'),
            operation_set.join_fields('cct1.id', 'cc.subject_id'),
            operation_set.join_fields('cct2.id', 'cc.status_id'),
        ],
        s4_aggregation = [
            # select
        ]
    )
