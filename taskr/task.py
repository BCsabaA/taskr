from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from taskr.auth import login_required
from taskr.db import get_db

from datetime import date


bp = Blueprint('task', __name__)

@bp.route('/')
def index():
    db = get_db()
    tasks = db.execute(
        'SELECT t.id, title, description, created_at, due_at, owner_user_id, username'
        ' FROM task t JOIN user u ON t.owner_user_id = u.id'
        ' ORDER BY created_at DESC'
    ).fetchall()
    return render_template('task/index.html', tasks=tasks)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due =  request.form['due_date']
        due_date = date.fromisoformat(due) if due else None
        
        error = None

        if not title or title.strip() == "":
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO task (title, description, due_at, created_user_id, owner_user_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, description, due_date, g.user['id'], g.user['id'])
            )
            db.commit()
            return redirect(url_for('task.index'))
        
    return render_template('task/create.html')


@bp.route('/<int:id>/task/update', methods=('GET', 'POST'))
@login_required
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due =  request.form['due_date']
        due_date = date.fromisoformat(due) if due else None
        
        error = None

        if not title or title.strip() == "":
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE task SET title=?, description=?, due_at=? '
                ' WHERE id=?',
                (title, description, due_date, id)
            )
            db.commit()
            return redirect(url_for('task.index'))
        
    return render_template('task/update.html', task=_get_task(id=id))


def _get_task(id, check_author=True):
    task = get_db().execute(
        'SELECT t.id, title, description, created_at, due_at, owner_user_id, username'
        ' FROM task t JOIN user u ON t.owner_user_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if task is None:
        abort(404, f"Task id {id} doesn't exist.")

    if check_author and task['owner_user_id'] != g.user['id']:
        abort(403)

    return task




