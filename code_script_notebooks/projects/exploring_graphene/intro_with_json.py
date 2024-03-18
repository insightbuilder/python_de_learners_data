import json
import os
import graphene


class Query(graphene.ObjectType):
    name = graphene.String()
    type = graphene.String()

    def resolve_name(root, info):
        return "Awesome"

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
