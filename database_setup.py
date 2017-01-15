from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import types

import datetime

Base = declarative_base()


class EndUser(Base):
    __tablename__ = "enduser"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    commitment = Column(String(100), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(Date, nullable=False)
    heads_up = Column(Date, nullable=False)
    notes = Column(String(500))
    enduser_id = Column(Integer, ForeignKey("enduser.id"), nullable=False)
    enduser = relationship(EndUser)
    status = Column(String(20), nullable=False)


engine = create_engine("postgresql://geordypaul:P1zzaCat@localhost/tasks")
Base.metadata.create_all(engine)
