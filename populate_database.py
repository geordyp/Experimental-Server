from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, EndUser, Task

engine = create_engine("postgresql://geordypaul:P1zzaCat@localhost/tasks")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a 'staging zone' for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = EndUser(name="Paul", email="paul@gmail.com")
session.add(user1)
session.commit()

task1 = Task(name="clean room",
             commitment="me",
             due_date="1-16-17",
             heads_up="1-16-17",
             notes="do a really good job",
             enduser_id=user1.id,
             status="idle")
session.add(task1)
session.commit()

task2 = Task(name="purge inbox",
             commitment="me",
             due_date="1-11-17",
             heads_up="1-11-17",
             notes="respond to people",
             enduser_id=user1.id,
             status="working")
session.add(task2)
session.commit()

task3 = Task(name="finish reading that book",
             commitment="me",
             due_date="1-16-17",
             heads_up="1-16-17",
             notes="",
             enduser_id=user1.id,
             status="done")
session.add(task3)
session.commit()

task4 = Task(name="set date for ead",
             commitment="nsbe",
             due_date="1-18-17",
             heads_up="1-15-17",
             notes="",
             enduser_id=user1.id,
             status="idle")
session.add(task4)
session.commit()

task5 = Task(name="set dates for coderdojo",
             commitment="coderdojo",
             due_date="1-17-17",
             heads_up="1-17-17",
             notes="",
             enduser_id=user1.id,
             status="idle")
session.add(task5)
session.commit()

task6 = Task(name="homework 1",
             commitment="math551",
             due_date="1-18-17",
             heads_up="1-18-17",
             notes="",
             enduser_id=user1.id,
             status="idle")
session.add(task6)
session.commit()

task7 = Task(name="homework 2",
             commitment="math551",
             due_date="1-19-17",
             heads_up="1-19-17",
             notes="",
             enduser_id=user1.id,
             status="idle")
session.add(task7)
session.commit()

task8 = Task(name="homework 3",
             commitment="math551",
             due_date="1-20-17",
             heads_up="1-18-17",
             notes="",
             enduser_id=user1.id,
             status="idle")
session.add(task8)
session.commit()

print "populated the database!"
