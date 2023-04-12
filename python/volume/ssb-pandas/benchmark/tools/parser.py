import sqlparse

def parse(query, operation_class):
    # tokens = sqlparse.parse(query)[0].tokens
    
    select_index = query.find("select ")
    from_index = query.find("from ")
    where_index = query.find("where ")
    group_index = query.find("group by ")
    order_index = query.find("order by ")
    
    select = query[select_index:from_index]
    fromm = query[from_index:where_index]
    where = query[where_index:group_index]
    group = query[group_index:order_index]
    order = query[order_index:]
    
    print(select)
    print(fromm)
    print(where)
    print(group)
    print(order)
    
    print("done")
    