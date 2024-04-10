from peewee import (
    SqliteDatabase,
    Model,
    CharField,
)

db = SqliteDatabase("trial.db")


class Payload(Model):
    input_text = CharField()
    output_text = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Payload])