from peewee import *

db = SqliteDatabase('dbweb.db')


class BaseModel(Model):
    class Meta:
        database = db


class Account(BaseModel):
    url = CharField(unique=True)
    points = IntegerField(default=0)
    is_up = BooleanField(default=False)


class Flag(BaseModel):
    flag = CharField()
    account = ForeignKeyField(Account, related_name='flags')


db.connect()
db.create_tables([Account, Flag], safe=True)