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
    pw_hash = Column(String(250), nullable=False)
    vision = Column(Integer, nullable=False)  # On Deck setting

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "vision": self.vision,
            "userURI": "http://localhost:5000/ondeck/api/v1.0/user/" + str(self.id),
            "createTaskURI": "http://localhost:5000/ondeck/api/v1.0/tasks/" + str(self.id),
            "doneTasksURI": "http://localhost:5000/ondeck/api/v1.0/tasks/" + str(self.id) + "/done",
            "onDeckTasksURI": "http://localhost:5000/ondeck/api/v1.0/tasks/" + str(self.id) + "/on_deck",
            "activeTasksURI": "http://localhost:5000/ondeck/api/v1.0/tasks/" + str(self.id) + "/active",
        }


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    commitment = Column(String(250), nullable=False)
    due_date = Column(Date, nullable=False)
    heads_up = Column(Date, nullable=True)
    done = Column(Boolean, nullable=False)
    completion_date = Column(Date, nullable=True)
    notes = Column(String(400), nullable=True)
    enduser_id = Column(Integer, ForeignKey("enduser.id"), nullable=False)
    enduser = relationship(EndUser)

    @property
    def serialize(self):
        due = self.due_date
        now = datetime.date.today()
        daysLeft = (due-now).days

        return {
            "name": self.name,
            "commitment": self.commitment,
            "completion_date": str(self.completion_date),
            "due_date": str(self.due_date),
            "days_left": daysLeft,
            "notes": self.notes,
            "heads_up": str(self.heads_up),
            "done": self.done,
            "uri": "http://localhost:5000/ondeck/api/v1.0/tasks/" + str(self.id)
        }


engine = create_engine("postgresql://geordypaul:P1zzaCat@localhost/tasks")
Base.metadata.create_all(engine)
