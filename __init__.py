from flask import Flask, render_template, jsonify, make_response

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
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
    return make_response(jsonify(tasks=[t.serialize for t in tasks]))


@app.route("/ondeck/api/v1.0/tasks", methods=["POST"])
def create_task():
    # Create a new task
    tasks = session.query(Task).all()
    return jsonify(tasks=[t.serialize for t in tasks])


@app.route("/ondeck/api/v1.0/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    # Retrieve a task
    task = session.query(Task).filter_by(id=task_id).one()
    return jsonify(task=[task.serialize])


@app.route("/ondeck/api/v1.0/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    # Update an existing task
    task = session.query(Task).filter_by(id=task_id).one()
    return jsonify(task=[task.serialize])


@app.route("/ondeck/api/v1.0/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    # Delete a task
    task = session.query(Task).filter_by(id=task_id).one()
    return jsonify(task=[task.serialize])


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
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
