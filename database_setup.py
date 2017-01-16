from sqlalchemy import Column, ForeignKey, Integer, Boolean, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import types

import datetime
from datetime import date
import time


Base = declarative_base()


class EndUser(Base):
    __tablename__ = "enduser"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    commitment = Column(String(100), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    due_date = Column(Date, nullable=False)
    heads_up = Column(Date, nullable=False)
    enduser_id = Column(Integer, ForeignKey("enduser.id"), nullable=False)
    enduser = relationship(EndUser)
    done = Column(Boolean, nullable=False)

    @property
    def serialize(self):
        due = self.due_date
        now = datetime.date.today()
        daysLeft = (due-now).days

        return {
            "id": self.id,
            "name": self.name,
            "commitment": self.commitment,
            "created_date": str(self.created_date),
            "due_date": str(self.due_date),
            "days_left": daysLeft,
            "heads_up": str(self.heads_up),
            "enduser_id": self.enduser_id,
            "done": self.done
        }


engine = create_engine("postgresql://geordypaul:P1zzaCat@localhost/tasks")
Base.metadata.create_all(engine)
