from flask import Flask, render_template, request, jsonify, make_response, abort

from sqlalchemy import create_engine, asc, desc, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, EndUser, Task

from flask_cors import CORS, cross_origin

from flask_httpauth import HTTPBasicAuth

import json
import string
import random
import hashlib

import datetime
from datetime import date
from datetime import timedelta


app = Flask(__name__)
CORS(app)

# Connect to Database and create database session
engine = create_engine("postgresql://geordypaul:P1zzaCat@localhost/tasks")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()


@app.route("/ondeck/api/v1.0/user", methods=["POST"])
@auth.login_required
def create_user():
    # Create a new user
    if (not request.json or
        "name" in request.json and type(request.json["name"]) != unicode or
        "passsword" in request.json and type(request.json["password"]) != unicode or
        "vision" in request.json and type(request.json["vision"]) != int):
        abort(400)

    # check if user name is already taken
    if get_user_by_name(request.json["name"]):
        return make_response(jsonify({"error": "This username is taken"}), 400)

    password_hash = make_pw_hash(request.json["name"], request.json["password"])
    newUser = EndUser(name=request.json["name"],
                   pw_hash=password_hash,
                   vision=request.json["vision"])
    session.add(newUser)
    session.commit()
    return make_response(jsonify(user=[newUser.serialize]), 201)


@app.route("/ondeck/api/v1.0/user/login", methods=["POST"])
@auth.login_required
def validate_login():
    # Validate user log in
    if (not request.json or
        "name" in request.json and type(request.json["name"]) != unicode or
        "passsword" in request.json and type(request.json["password"]) != unicode):
        abort(400)

    try:
        # get user
        user = get_user_by_name(request.json["name"])

        # confirm password
        if user and is_valid_pw_login(request.json["name"],
                                      request.json["password"],
                                      user.pw_hash):
            return make_response(jsonify(user=[user.serialize]), 200)
        else:
            return make_response(jsonify({"error": "Invalid login"}), 400)
    except NoResultFound:
        abort(404)


@app.route("/ondeck/api/v1.0/user/<int:user_id>", methods=["DELETE"])
@auth.login_required
def delete_user(user_id):
    # Delete a user and their tasks
    try:
        user = session.query(EndUser).filter(EndUser.id == user_id).one()

        userTasks = session.query(Task).filter(Task.enduser_id == user_id).all()
        for task in userTasks:
            session.delete(task)

        session.delete(user)
        session.commit()
        return make_response(jsonify({"result": True}), 202)
    except NoResultFound:
        abort(404)


@app.route("/ondeck/api/v1.0/tasks/<int:user_id>/<string:filter_list>", methods=["GET"])
@auth.login_required
def get_tasks(user_id, filter_list):
    # Retrieve list of tasks
    if filter_list == "done":
        tasks = session.query(Task).\
                filter(Task.enduser_id == user_id,
                Task.done == True).\
                order_by(desc(Task.completion_date)).all()
    elif filter_list == "on_deck":
        try:
            # grabbing the enduser to get their on deck vision setting
            user = session.query(EndUser).filter_by(id=user_id).one()
            # will get tasks with due dates less than or equal to vision (e.g. 3 days from today) and heads_up of today or less
            vision = datetime.date.today() + timedelta(days=user.vision)
            tasks = session.query(Task).\
                    filter(or_(Task.due_date <= vision,
                    Task.heads_up <= datetime.date.today()),
                    Task.enduser_id == user_id,
                    Task.done == False).\
                    order_by(asc(Task.due_date)).all()
        except NoResultFound:
            abort(404)
    elif filter_list == "all":
        tasks = session.query(Task).\
                filter_by(enduser_id=user_id).\
                filter_by(done=False).\
                order_by(asc(Task.due_date)).all()
    else:
        abort(400)
    return make_response(jsonify(tasks=[t.serialize for t in tasks]), 200)


@app.route("/ondeck/api/v1.0/tasks/<int:user_id>", methods=["POST"])
@auth.login_required
def create_task(user_id):
    # Create a new task
    if (not request.json or
        "name" in request.json and type(request.json["name"]) != unicode or
        "commitment" in request.json and type(request.json["commitment"]) != unicode or
        "due_date" in request.json and type(request.json["due_date"]) != unicode or
        "heads_up" in request.json and type(request.json["heads_up"]) != unicode or
        "notes" in request.json and type(request.json["notes"]) != unicode):
        abort(400)

    newTask = Task(name=request.json["name"],
                   commitment=request.json["commitment"],
                   due_date=request.json["due_date"],
                   enduser_id=user_id,
                   done=False,
                   heads_up=request.json.get("heads_up", None),
                   notes=request.json.get("notes", None),
                   completion_date=None)
    session.add(newTask)
    session.commit()
    return make_response(jsonify(task=[newTask.serialize]), 201)


@app.route("/ondeck/api/v1.0/tasks/<int:task_id>", methods=["GET"])
@auth.login_required
def get_task(task_id):
    # Retrieve a task
    try:
        task = session.query(Task).filter(Task.id == task_id).one()
        return make_response(jsonify(task=[task.serialize]), 200)
    except NoResultFound:
        abort(404)


@app.route("/ondeck/api/v1.0/tasks/<int:task_id>", methods=["PUT"])
@auth.login_required
def update_task(task_id):
    # Update an existing task
    try:
        updatedTask = session.query(Task).filter(Task.id == task_id).one()
        if not request.json or
           "name" in request.json and type(request.json["name"]) != unicode or
           "commitment" in request.json and type(request.json["commitment"]) != unicode or
           "due_date" in request.json and type(request.json["due_date"]) != unicode or
           "heads_up" in request.json and type(request.json["heads_up"]) != unicode or
           "done" in request.json and type(request.json["done"]) != bool or
           "completion_date" in request.json and type(request.json["completion_date"]) != unicode or
           "notes" in request.json and type(request.json["notes"]) != unicode:
            abort(400)

        updatedTask.name = request.json.get("name", updatedTask.name)
        updatedTask.commitment = request.json.get("commitment", updatedTask.commitment)
        updatedTask.due_date = request.json.get("due_date", updatedTask.due_date)
        updatedTask.heads_up = request.json.get("heads_up", updatedTask.heads_up)
        updatedTask.done = request.json.get("done", updatedTask.done)
        updatedTask.completion_date = request.json.get("completion_date", updatedTask.completion_date)
        updatedTask.notes = request.json.get("notes", updatedTask.notes)
        return make_response(jsonify(task=[updatedTask.serialize]), 202)
    except NoResultFound:
        abort(404)


@app.route("/ondeck/api/v1.0/tasks/<int:task_id>", methods=["DELETE"])
@auth.login_required
def delete_task(task_id):
    # Delete a task
    try:
        deletedTask = session.query(Task).filter(Task.id == task_id).one()
        session.delete(deletedTask)
        session.commit()
        return make_response(jsonify({"result": True}), 202)
    except NoResultFound:
        abort(404)


def get_user_by_name(name):
    user = session.query(EndUser).filter(EndUser.name == name).all()
    if user:
        return user[0]
    return None


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s,%s" % (h, salt)


def make_salt(length=5):
    return "".join(random.choice(string.letters) for x in xrange(length))


def is_valid_pw_login(name, pw, h):
    salt = h.split(",")[1]
    return h == make_pw_hash(name, pw, salt)


@auth.get_password
def get_password(username):
    if username == "geordypaul":
        return "Appl3B3ar"
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error": "Unauthorized access"}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "No items found"}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({"error": "Bad request"}), 400)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
