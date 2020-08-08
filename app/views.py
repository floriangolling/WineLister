from app import app
from flask import render_template, request, redirect, flash, url_for, session
from app.models import *
from app.controller import *
from datetime import datetime

@app.route('/', methods=['GET'])
def home():
    return render_template('pages/index.html', title="Titre")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
            flash("Vous êtes déjà connecté")
            return render_template('pages/index.html', title="Titre")
    if request.method == 'GET':
        return render_template('pages/register.html', title="Register")
    User.username = request.form['username']
    User.password = request.form['password']
    if user_exists(User.username) == True:
        flash("Le compte existe déjà")
        return render_template('pages/register.html', title="Register")
    if 'username' in session:
        flash("Vous êtes déjà connecté")
        return render_template('pages/index.html', title="Titre")
    register_user(User.username, User.password)
    return redirect(url_for('login'))

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            flash("Vous êtes déjà connecté")
            return render_template('pages/index.html', title="Titre")
        return render_template('pages/signin.html', title="Login")
    User.username = request.form['username']
    User.password = request.form['password']
    if user_exists(User.username) == True:
        if get_user(User.username)[2] == User.password:
            session['username'] = User.username
            return redirect('/')
    flash ("Identifiant ou mot de passe incorrect")
    return render_template('pages/signin.html', title="Login")

@app.route('/task/add', methods=['POST', 'GET'])
def add():
    if (request.method == 'GET'):
        if not 'username' in session:
            flash("Vous n'êtes pas connecté")
            return render_template('pages/signin.html', title="Login")
        return render_template('pages/add.html', title="Add")
    User.username = session['username']
    Task.task_name = request.form['name']
    if (Task.task_name == ''):
        Task.task_name = 'Task'
    Task.task_description = request.form['task_description']
    if (Task.task_description == ''):
        Task.task_description = 'Description'
    dateTimeObj = datetime.now()
    Task.task_begin = dateTimeObj
    Task.task_end = dateTimeObj
    Task.quantity = request.form['quantity']
    add_task(Task.task_name, Task.task_description, Task.task_begin, Task.task_end, User.username, Task.quantity)
    return redirect(url_for('usertask'))

@app.route('/signout', methods=['POST'])
def signout():
    if 'username' in session:
        session.pop('username', None)
        return redirect(url_for('login'))
    return render_template('pages/index.html', title="Titre")

@app.route('/user/task', methods=['GET'])
def usertask():
    if 'username' in session:
        User.username = session['username']
        tasks = get_task_user(User.username)
        return render_template('pages/index.html', title="tasks", tasks=tasks)
    else:
        flash("Vous n'êtes pas connecté")
        return render_template('pages/signin.html', title="Login")
    return render_template('pages/index.html', title="Titre")

@app.route('/user', methods=['GET'])
def user():
    if 'username' in session:
        User.username = session['username']
        flash("Rebonjour !")
        flash(User.username)
        flash(":)")
    else:
        flash("Vous n'êtes pas connecté")
        return render_template('pages/signin.html', title="Login")
    return render_template('pages/index.html', title="Titre")

@app.route('/user/task/del/id', methods=['POST'])
def delete():
    if (request.method == 'POST'):
        id_t = request.form['value']
        delete_task(id_t)
        tasks = get_task_user(User.username)
        return render_template('pages/index.html', title="tasks", tasks=tasks)

@app.route('/user/task/id', methods=['GET', 'POST'])
def show():
    if (request.method == 'POST'):
        change = request.form['change']
        if change == '0':
            id_t = request.form['value2']
            tasks = get_task(id_t)
            tasks[0].id = id_t
            return render_template('pages/task.html', title="tasks", tasks=tasks)
        name = request.form['name']
        desc = request.form['desc']
        id_t = request.form['id_t']
        quantity = request.form['quantity']
        tasks = change_task(name,desc, id_t,quantity)
        tasks = get_task_user(session['username'])
        return render_template('pages/index.html', title="tasks", tasks=tasks)