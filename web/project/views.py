from project import app, lm
from flask import request, redirect, render_template, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, TodoForm
from .user import User
from bson.objectid import ObjectId


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("todo"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/todo')
@login_required
def todo():
    form = TodoForm()
    items = []
    if current_user.is_authenticated:
        _items = app.config['TODO_COLLECTION'].find(
            {"user": current_user.username}
        )
        items = [item for item in _items]

    return render_template('todo.html', items=items, form=form, action="/create")


@app.route('/create', methods=['POST'])
@login_required
def new():
    form = TodoForm()
    if request.method == 'POST' and form.validate_on_submit():
        item = {
            'user': current_user.username,
            'name': request.form['name'],
            'description': request.form['description']
        }
        result = app.config['TODO_COLLECTION'].insert_one(item)
        if result.inserted_id:
            flash("Todo created successfully!", category='success')
        else:
            flash("Something went wrong!", category='error')
    return redirect(url_for('todo'))


@app.route('/edit/<_id>', methods=['GET'])
@login_required
def edit(_id):
    if current_user.is_authenticated:
        todo = app.config['TODO_COLLECTION'].find_one({
            '_id': ObjectId(_id),
            'user': current_user.username
        })
        if todo:
            todo_obj = type('Todo', (object,), {})
            todo_obj.object_id = todo['_id']
            todo_obj.name = todo['name']
            todo_obj.description = todo['description']

            form = TodoForm(obj=todo_obj)
        else:
            abort(403)
    return render_template('form.html', form=form, action="/update")



@app.route('/update', methods=['POST'])
@login_required
def update():
    form = TodoForm()
    if request.method == 'POST' and form.validate_on_submit():
        todo = app.config['TODO_COLLECTION'].find_one({
            '_id': ObjectId(form.object_id.data),
            'user': current_user.username
        })

        if todo:
            todo['name'] = form.name.data
            todo['description'] = form.description.data

            result = app.config['TODO_COLLECTION'].update(
                {
                    '_id': ObjectId(form.object_id.data)
                },
                todo
            )

            if result['updatedExisting']:
                flash("Edited successfully!", category='success')
            else:
                flash("Something went wrong!", category='error')
            return redirect(url_for('todo'))
        else:
            abort(403)


@app.route('/delete/<_id>', methods=['Get'])
@login_required
def delete_todo(_id):
    deleted = app.config['TODO_COLLECTION'].remove({
        '_id': ObjectId(_id),
        'user': current_user.username
    });
    if deleted:
        flash("Todo deleted successfully!", category='success')
    else:
        flash("Something went wrong!", category='error')
    return redirect(url_for('todo'))


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403
