# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DateTime, SmallInteger
from sqlalchemy_dao import Model

dao = None

class Cron(Model):
    queue = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    last = Column(DateTime)
    schedule = Column(String, nullable=False)

class Task(Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    args = Column(String, nullable=False)
    eta = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    queue = Column(String, nullable=False)
    retries = Column(SmallInteger, nullable=False)
    