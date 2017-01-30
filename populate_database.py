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

user1 = EndUser(name="Paul", pw_hash="lolololol", vision=5)
session.add(user1)
session.commit()

user2 = EndUser(name="Geordy", pw_hash="lolololol", vision=2)
session.add(user2)
session.commit()

task1 = Task(name="clean room",
             commitment="me",
             due_date="1-22-17",
             heads_up="1-21-17",
             notes="do a good job",
             enduser_id=1,
             completion_date="1-21-17",
             done=True)
session.add(task1)
session.commit()

task2 = Task(name="purge inbox",
             commitment="me",
             due_date="1-23-17",
             enduser_id=1,
             done=False)
session.add(task2)
session.commit()

task3 = Task(name="finish reading that book",
             commitment="me",
             due_date="1-24-17",
             heads_up="1-22-17",
             enduser_id=1,
             done=False)
session.add(task3)
session.commit()

task4 = Task(name="set date for ead",
             commitment="nsbe",
             due_date="1-24-17",
             enduser_id=1,
             done=False)
session.add(task4)
session.commit()

task5 = Task(name="set dates for coderdojo",
             commitment="coderdojo",
             due_date="1-25-17",
             heads_up="1-24-17",
             enduser_id=2,
             done=False)
session.add(task5)
session.commit()

task6 = Task(name="homework 1",
             commitment="math551",
             notes="page 10: 10,11,12,23,44,45",
             due_date="1-25-17",
             heads_up="1-23-17",
             enduser_id=2,
             completion_date="1-22-17",
             done=True)
session.add(task6)
session.commit()

task7 = Task(name="homework 2",
             commitment="math551",
             notes="page 72: 13,23,34,45",
             due_date="1-27-17",
             heads_up="1-19-17",
             enduser_id=2,
             done=False)
session.add(task7)
session.commit()

task8 = Task(name="homework 3",
             commitment="math551",
             notes="page 56: 1,2,3,4,5",
             due_date="1-26-17",
             heads_up="1-21-17",
             enduser_id=2,
             done=False)
session.add(task8)
session.commit()

print "populated the database!"
