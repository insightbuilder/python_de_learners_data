#!/usr/bin/env python
"""The script will create connection through python objects and query the database"""

from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.sql.sqltypes import TIMESTAMP

import sqlite3
db_conn = create_engine('sqlite:///trial_data.db')
#SessionLocal = sessionmaker(bind=db_conn)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class Hacker(Base):
    """Hacker class provides access to the table hack_data in any Database"""
    __tablename__ = 'hack_data'
    Index = Column(Integer, primary_key=True,nullable=False)
    Datetime = Column(String)
    Host = Column(String)
    Src = Column(Integer)
    Proto = Column(String)
    Type = Column(String)
    Spt = Column(Float)
    Dpt = Column(Float)
    Srcstr = Column(String)
    Cc = Column(String)
    Country = Column(String)
    Locale = Column(String)
    Localeabbr = Column(String)
    Postalcode = Column(String)
    Latitude = Column(Float)
    Longitude = Column(Float)

def query_data(data_bconn,table_obj):
    select_ten = data_bconn.query(table_obj).limit(10).all()
    print(select_ten)
    return select_ten

#recd_data = query_data(get_db,Hacker)

#print(type(recd_data))

with Session(db_conn) as connected:
    data_recd = connected.scalars(select(Hacker).limit(10))
    for row in data_recd: 
        print(row.Datetime)
