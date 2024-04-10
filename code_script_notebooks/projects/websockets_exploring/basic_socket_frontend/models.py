from peewee import *

db = SqliteDatabase("warmup.db")


class Payload(Model):
    payload = CharField(max_length=250)
    packet = CharField(max_length=500)

    class Meta:
        database = db


db.connect()
db.create_tables([Payload])