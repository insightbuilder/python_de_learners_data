import json
import os
import graphene


class Query(graphene.ObjectType):
    name = graphene.String(value=graphene.String(default_value='sam'))
    type = graphene.String()

    def resolve_name(root, info, value):
        return value

    def resolve_type(root, info):
        return "Pedtro"


schema = graphene.Schema(query=Query)

print(schema)

query_via_ql0 = """
    query myquery {
        your_name: name 
        type
    }
"""
query_via_ql = """
    query myquery {
        your_name: name
        type
    }"""

result = schema.execute(query_via_ql)
print(result.data)
