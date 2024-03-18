import graphene

# The data is already present here
# which the QL is controlling
DATA = [{
    "name": "name1",
    "age": "age1"
}, 
    {
    "name": "name2",
    "age": "age2"
}]


class Person(graphene.ObjectType):
    name = graphene.String()
    age = graphene.String()


class Query(graphene.ObjectType):
    array = graphene.List(Person, size=graphene.Int(default_value=1))
    # name = graphene.String(value=graphene.String(default_value='sam'))
    # type = graphene.String()

    def resolve_array(root, info, size):
        return DATA[:size]
    # def resolve_name(root, info, value):
        # return value

    # def resolve_type(root, info):
        # return "Pedtro"


schema = graphene.Schema(query=Query)

print(schema)

query_via_ql2 = """
    query newquery{
        array (size : 2) {
            name
            age
        }
    }
"""

 # The query is requesting for an array
query_via_ql = """  
    query newquery{
        array (size:1) {
            age
        }
    }
"""

# query_via_ql0 = """
    # query myquery {
        # your_name: name 
        # type
    # }
# """
query_via_ql1 = """
    query myquery {
        your_name: name
        type
    }"""

result = schema.execute(query_via_ql)
# result = schema.execute(query_via_ql)

print(result.data)