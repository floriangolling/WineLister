import pymysql as sql
import json
from flask import jsonify
from config import *


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class Taskr:
    def __init__(self, id_t: str, task_name: str, task_description: str, quantity : int):
        self.task_name = task_name
        self.task_description = task_description
        self.id = id_t
        self.task_quantity = quantity

class Task:
    def __init__(self, task_name: str, task_description: str, quantity: int, status: None, begin = None, end = None):
        self.task_name = task_name
        self.task_description = task_description
        self.begin = begin
        self.end = end
        self.status = status
        self.task_quantity = quantity

class Database:
    def __init__(self, *args, **kwargs):
        self.connect = sql.connect(*args, **kwargs)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def execute(self, *args, **kwargs):
        return self.cursor.execute(*args, **kwargs)

    def commit(self):
        self.connect.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

database = Database(host=DATABASE_HOST, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)


def register_user(username, password):
    database.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
    database.commit()

def user_exists(username):
    return database.execute("SELECT 1 FROM user WHERE username = %s", (username))

def get_user(user):
    database.execute("SELECT * FROM user WHERE username = %s", (user))
    result = database.fetchone()
    return result

def get_user_id(user):
    database.execute("SELECT user_id FROM user WHERE username = %s", (user))
    result = database.fetchone()
    return result

def add_task(name, description, begin, end, user, quantity):
    database.execute("INSERT INTO task (name, description, begin, end, quantity) VALUES (%s, %s, %s, %s, %s)", (name, description, begin, end, int(quantity)))
    database.commit()
    database.execute("SELECT task_id FROM task ORDER BY task_id DESC")
    result = database.fetchone()
    user_id = get_user_id(user)
    database.execute("INSERT INTO user_has_task (fk_task_id, fk_user_id) VALUES (%s, %s)", (result[0], user_id[0]))
    database.commit()

def get_task_user(user):
    tasks = []
    user_id = get_user_id(user)
    database.execute("SELECT fk_task_id FROM user_has_task WHERE fk_user_id =%s", (user_id))
    ids = list(database.fetchall())
    for id in ids:
        database.execute("SELECT name FROM task WHERE task_id =%s", id)
        task = list(database.fetchall()[0])
        name = task[0]
        database.execute("SELECT description FROM task WHERE task_id =%s", id)
        task = list(database.fetchall()[0])
        description = task[0]
        database.execute("SELECT quantity FROM task WHERE task_id =%s", id)
        task = list(database.fetchall()[0])
        quantity = task[0]
        tasks.append(Taskr(id, name, description, quantity))
    return tasks

def delete_task(id_t):
    database.execute("DELETE task from task WHERE task_id =%s", id_t)
    database.commit()

def get_task(id_t):
    tasks = []
    database.execute("SELECT name FROM task WHERE task_id =%s", id_t)
    task = list(database.fetchall()[0])
    name = task[0]
    database.execute("SELECT description FROM task WHERE task_id =%s", id_t)
    task = list(database.fetchall()[0])
    description = task[0]
    database.execute("SELECT quantity FROM task WHERE task_id =%s", id_t)
    task = list(database.fetchall()[0])
    quantity = task[0]
    tasks.append(Taskr(id, name, description, quantity))
    return tasks

def change_task(name, desc, id_t, quantity):
    if (name != ''):
        database.execute("UPDATE task SET name=%s WHERE task_id=%s", (name, id_t))
    if (desc != ''):
        database.execute("UPDATE task SET description=%s WHERE task_id=%s", (desc, id_t))
    database.execute("UPDATE task SET quantity=%s WHERE task_id=%s", (int(quantity), id_t))
    database.commit()
    tasks = get_task(id_t)
    return (tasks)
