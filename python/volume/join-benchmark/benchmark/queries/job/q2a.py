# SELECT MIN(t.title) AS movie_title
# FROM company_name AS cn,
#      keyword AS k,
#      movie_companies AS mc,
#      movie_keyword AS mk,
#      title AS t
# WHERE cn.country_code ='[de]'
#   AND k.keyword ='character-name-in-title'
#   AND cn.id = mc.company_id
#   AND mc.movie_id = t.id
#   AND t.id = mk.movie_id
#   AND mk.keyword_id = k.id
#   AND mc.movie_id = mk.movie_id;



def instruction_set(operation_set):
    return [
        [
            operation_set.from_tables('job', ["company_name","keyword","movie_companies","movie_keyword","title"], ["cn","k","mc","mk","t"])
        ],
        [
            operation_set.filter_field_eq('cn.country_code', ['[de]']),
            operation_set.filter_field_eq('k.keyword', ['character-name-in-title']),
        ],
        [ # 6 JOINS
            operation_set.join_fields("cn.id", "mc.company_id"),
            operation_set.join_fields("mc.movie_id", "t.id"),
            operation_set.join_fields("t.id", "mk.movie_id"),
            operation_set.join_fields("mk.keyword_id", "k.id"),
            operation_set.join_fields("mc.movie_id", "mk.movie_id")
        ],
        [
            # select
        ]
    ]
