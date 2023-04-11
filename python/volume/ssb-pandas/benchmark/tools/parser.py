import sqlparse

def parse(query:str, operation_set):
    tokens = sqlparse.parse(str)[0].tokens
    # TODO parse the tokens