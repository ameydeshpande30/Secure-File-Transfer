from peewee import SqliteDatabase, Model, CharField
import datetime

db = SqliteDatabase('data.db')
class BaseModel(Model):
    class Meta:
        database = db


class File(BaseModel):
    name = CharField(max_length=150)
    path = CharField(max_length=150, unique=True)
 
db.connect()
db.create_tables([File])

def addFile(name, path):
    File.create(name=name, path=path)
    db.commit()

def getAllFiles():
    out = File.select()
    data = []
    for i  in out:
        data.append(i.name)
    return(data)
 

def getAllFilesPath():
    out = File.select()
    data = []
    for i  in out:
        data.append({"name" : i.name, "path" : i.path})
    return(data)