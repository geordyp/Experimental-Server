from flask import Flask, render_template, request, jsonify, make_response, abort

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, EndUser, Task

from flask_cors import CORS, cross_origin

from flask_httpauth import HTTPBasicAuth

import json


app = Flask(__name__)
CORS(app)

# Connect to Database and create database session
engine = create_engine("postgresql://geordypaul:P1zzaCat@localhost/tasks")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()


@app.route("/ondeck/api/v1.0/tasks", methods=["GET"])
@auth.login_required
def get_tasks():
    # Retrieve list of tasks
    tasks = session.query(Task).all()
    return make_response(jsonify(tasks=[t.serialize for t in tasks]), 200)


@app.route("/ondeck/api/v1.0/tasks", methods=["POST"])
def create_task():
    # Create a new task
    if (not request.json or
        not "name" in request.json or
        not "commitment" in request.json or
        not "due_date" in request.json or
        not "heads_up" in request.json or
        not "enduser_id" in request.json):
        abort(400)

    if (type(request.json["name"]) != unicode or
        type(request.json["commitment"]) != unicode or
        type(request.json["due_date"]) != unicode or
        type(request.json["heads_up"]) != unicode or
        type(request.json["enduser_id"]) != int):
        print("************ second")
        abort(400)

    newTask = Task(name=request.json["name"],
                   commitment=request.json["commitment"],
                   due_date=request.json["due_date"],
                   heads_up=request.json["heads_up"],
                   enduser_id=request.json["enduser_id"],
                   done=False)
    session.add(newTask)
    session.commit()
    return make_response(jsonify(task=[newTask.serialize]), 201)


@app.route("/ondeck/api/v1.0/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    # Retrieve a task
    try:
        task = session.query(Task).filter_by(id=task_id).one()
        return make_response(jsonify(task=[task.serialize]), 200)
    except NoResultFound:
        abort(404)


@app.route("/ondeck/api/v1.0/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    # Update an existing task
    try:
        updatedTask = session.query(Task).filter_by(id=task_id).one()
        if not request.json:
            abort(400)
        if "name" in request.json and type(request.json["name"]) != unicode:
            abort(400)
        if "commitment" in request.json and type(request.json["commitment"]) != unicode:
            abort(400)
        if "due_date" in request.json and type(request.json["due_date"]) != unicode:
            abort(400)
        if "heads_up" in request.json and type(request.json["heads_up"]) != unicode:
            abort(400)
        if "done" in request.json and type(request.json["done"]) != bool:
            abort(400)

        updatedTask.name = request.json.get("name", updatedTask.name)
        updatedTask.commitment = request.json.get("commitment", updatedTask.commitment)
        updatedTask.due_date = request.json.get("due_date", updatedTask.due_date)
        updatedTask.heads_up = request.json.get("heads_up", updatedTask.heads_up)
        updatedTask.done = request.json.get("done", updatedTask.done)
        return make_response(jsonify(task=[updatedTask.serialize]), 202)
    except NoResultFound:
        abort(404)


@app.route("/ondeck/api/v1.0/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    # Delete a task
    try:
        deletedTask = session.query(Task).filter_by(id=task_id).one()
        session.delete(deletedTask)
        session.commit()
        return make_response(jsonify({"result": True}), 202)
    except NoResultFound:
        abort(404)


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
