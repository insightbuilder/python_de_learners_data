import graphene

Data = [{
    "name": "name1",
    "age": "28"
}, {
    "name": "name1",
    "age": "28"
}]


class Person(graphene.ObjectType):
    name = graphene.String(required=True)
    age = graphene.String(required=True)


class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        age = graphene.String()

    ok = graphene.Boolean()
    person = graphene.Field(Person)

    def mutate(self, info, name, age):
        person = Person(name=name,
                        age=age)
        ok = True
        return CreatePerson(person=person,
                            ok=ok)


class PersonMutated(graphene.ObjectType):
    make_person = CreatePerson.Field()


class Query(graphene.ObjectType):
    person = graphene.Field(Person)


schema = graphene.Schema(query=Query,
                         mutation=PersonMutated)

# print(schema)
# makePerson below is coming from PersonMutated's make_person
query = """
    mutation mutated {
        makePerson(name:"Mutate2", age:"22") {
            person {
                name
                age
            }
            ok
        }
    }
"""

result = schema.execute(query)

print(result)