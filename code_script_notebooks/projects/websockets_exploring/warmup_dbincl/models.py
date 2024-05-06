from peewee import (
    SqliteDatabase,
    Model,
    CharField
) 

db = SqliteDatabase('test.db')
db.connect()


class Mynotes(Model):
    heading = CharField(null=False, unique=True)
    content = CharField(null=False)

    class Meta:
        database = db


db.create_tables([Mynotes])