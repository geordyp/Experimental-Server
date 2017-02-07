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
import uuid
import re

import datetime
from datetime import date
from datetime import timedelta


app = Flask(__name__)
CORS(app)

# connect to database and create database session
engine = create_engine('postgresql://me:password@localhost/tasks')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()


@app.route('/ondeck/api/v1.0/user', methods=['POST'])
@auth.login_required
def create_user():
    # create a new user
    if (not request.json or
        not 'name' in request.json or
        not 'password' in request.json):
        abort(400)

    if (type(request.json['name']) != unicode or
        type(request.json['password']) != unicode):
        abort(400)

    # check if username is the correct format
    if not is_valid_username(request.json['name']):
        return make_response(jsonify({"error": "Invalid username"}), 400)

    # check if password is the correct format
    if not is_valid_password(request.json['password']):
        return make_response(jsonify({"error": "Invalid password"}), 400)

    # check if username is already taken
    if get_user_by_name(request.json['name']):
        return make_response(jsonify({"error": "Username is taken"}), 400)

    password_hash = make_pw_hash(request.json['name'], request.json['password'])
    newUser = EndUser(id=str(uuid.uuid1()),
                      name=request.json['name'],
                      pw_hash=password_hash,
                      vision=3)
    session.add(newUser)
    session.commit()
    return make_response(jsonify(user=[newUser.serialize]), 201)


@app.route('/ondeck/api/v1.0/user/login', methods=['POST'])
@auth.login_required
def validate_login():
    # validate user log in
    if (not request.json or
        not 'name' in request.json or
        not 'password' in request.json):
        abort(400)

    if (type(request.json['name']) != unicode or
        type(request.json['password']) != unicode):
        abort(400)

    try:
        # get user
        user = get_user_by_name(request.json['name'])

        # confirm password
        if user and is_valid_pw_login(request.json['name'],
                                      request.json['password'],
                                      user.pw_hash):
            return make_response(jsonify(user=[user.serialize]), 200)
        else:
            return make_response(jsonify({"error": "Invalid login"}), 400)
    except NoResultFound:
        abort(404)


@app.route('/ondeck/api/v1.0/user/<string:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    # update a user
    if not request.json:
        abort(400)

    # check username
    if 'name' in request.json:
        if type(request.json['name']) != unicode:
            abort(400)
        elif not is_valid_username(request.json['name']):
            return make_response(jsonify({"error": "Invalid username"}), 400)
        elif get_user_by_name(request.json['name']):
            return make_response(jsonify({"error": "Username is taken"}), 400)

    # check password
    if 'password' in request.json:
        if type(request.json['password']) != unicode:
            abort(400)
        elif not is_valid_password(request.json['password']):
            return make_response(jsonify({"error": "Invalid password"}), 400)

    # check vision
    if 'vision' in request.json:
        if type(request.json['vision']) != int:
            abort(400)
        elif not is_valid_vision(request.json['vision']):
            return make_response(jsonify({"error": "Invalid on deck setting"}), 400)

    try:
        updatedUser = session.query(EndUser).filter(EndUser.id == user_id).one()
        updatedUser.name = request.json.get('name', updatedUser.name)
        updatedUser.vision = request.json.get('vision', updatedUser.vision)
        if 'password' in request.json:
            password_hash = make_pw_hash(updatedUser.name, request.json['password'])
            updatedUser.password = password_hash

        session.commit()
        return make_response(jsonify(user=[updatedUser.serialize]), 202)
    except NoResultFound:
        abort(404)


@app.route("/ondeck/api/v1.0/user/<string:user_id>", methods=["DELETE"])
@auth.login_required
def delete_user(user_id):
    # delete a user and their tasks
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


@app.route("/ondeck/api/v1.0/tasks/<string:user_id>/<string:filter_list>", methods=["GET"])
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
    elif filter_list == "active":
        tasks = session.query(Task).\
                filter_by(enduser_id=user_id).\
                filter_by(done=False).\
                order_by(asc(Task.due_date)).all()
    else:
        abort(400)
    return make_response(jsonify(tasks=[t.serialize for t in tasks]), 200)


@app.route("/ondeck/api/v1.0/tasks/new/<int:user_id>", methods=["POST"])
@auth.login_required
def create_task(user_id):
    # Create a new task
    if (not request.json or
        not "name" in request.json or
        not "task_group" in request.json or
        not "due_date" in request.json or
        not "heads_up" in request.json or
        not "notes" in request.json):
        abort(400)

    if (type(request.json["name"]) != unicode or
        type(request.json["task_group"]) != unicode or
        type(request.json["due_date"]) != unicode or
        type(request.json["heads_up"]) != unicode or
        type(request.json["notes"]) != unicode):
        abort(400)

    newTask = Task(name=request.json["name"],
                   task_group=request.json["task_group"],
                   due_date=request.json["due_date"],
                   enduser_id=user_id,
                   done=False,
                   heads_up=request.json["heads_up"] if request.json["heads_up"] != "" else None,
                   notes=request.json["notes"] if request.json["notes"] != "" else None,
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
        if (not request.json):
            abort(400)

        if ("name" in request.json and type(request.json["name"]) != unicode or
            "task_group" in request.json and type(request.json["task_group"]) != unicode or
            "due_date" in request.json and type(request.json["due_date"]) != unicode or
            "heads_up" in request.json and type(request.json["heads_up"]) != unicode or
            "done" in request.json and type(request.json["done"]) != bool or
            "completion_date" in request.json and type(request.json["completion_date"]) != unicode or
            "notes" in request.json and type(request.json["notes"]) != unicode):
            abort(400)

        updatedTask.name = request.json.get("name", updatedTask.name)
        updatedTask.task_group = request.json.get("task_group", updatedTask.task_group)
        updatedTask.due_date = request.json.get("due_date", updatedTask.due_date)
        updatedTask.done = request.json.get("done", updatedTask.done)
        updatedTask.heads_up = request.json.get("heads_up", updatedTask.heads_up)
        updatedTask.heads_up = None if updatedTask.heads_up == "" else updatedTask.heads_up
        updatedTask.completion_date =  request.json.get("completion_date", updatedTask.completion_date)
        updatedTask.completion_date =  None if updatedTask.completion_date == "" else updatedTask.completion_date
        updatedTask.notes = request.json.get("notes", updatedTask.notes)
        updatedTask.notes = None if updatedTask.notes == "" else updatedTask.notes
        session.commit()
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


def is_valid_username(name):
    # check if username is the correct format
    username_re = re.compile(r"^[a-zA-Z0-9_-]{1,20}$")
    if not username_re.match(name):
        return False

    return True


def is_valid_password(password):
    # check if password is the correct format
    password_re = re.compile(r"^.{3,20}$")
    if not password_re.match(password):
        return False

    return True


def is_valid_vision(vision):
    # check if vision is the correct format
    if (int(vision) > 0 and int(vision) < 61):
        return True

    return False


@auth.verify_password
def verify_password(username, password):
    if username == "me" and password == "password":
        return True
    return False


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
