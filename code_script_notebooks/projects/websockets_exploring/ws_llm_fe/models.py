from peewee import (
    SqliteDatabase,
    CharField,
    Model
)

db = SqliteDatabase('llm_data.db')
db.connect()


class Promptdata(Model):
    user_prompt = CharField(max_length=500)
    system_prompt = CharField(max_length=500)
    llm_reply = CharField(max_length=750)

    class Meta:
        database = db


db.create_tables([Promptdata])