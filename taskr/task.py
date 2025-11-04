from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from taskr.auth import login_required
from taskr.db import get_db


bp = Blueprint('task', __name__)

@bp.route('/')
def index():
    return render_template('task/index.html')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        pass
    return render_template('task/create.html')

@bp.route('/update', methods=('GET', 'POST'))
@login_required
def update():
    if request.method == 'POST':
        pass
    return render_template('task/update.html')



