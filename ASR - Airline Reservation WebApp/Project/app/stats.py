from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import wraps
from .models import User, Seat
from . import db
from matplotlib import pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

stats = Blueprint('stats', __name__)
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator



@stats.route('/graph1', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def graph_seats():
    global buf
    airlines = db.session.query(Seat.airline).distinct().all()
    airlines = [airline[0] for airline in airlines]
    reserved_seats = {}
    available_seats = {}
    for airline in airlines:
        reserved = Seat.query.filter(Seat.status == 'reserved', Seat.airline == airline).count()
        available = Seat.query.filter(Seat.status == 'available', Seat.airline == airline).count()
        reserved_seats[airline] = reserved
        available_seats[airline] = available
    fig, ax = plt.subplots()
    ax.bar(reserved_seats.keys(), reserved_seats.values(), label="Reserved")
    ax.bar(available_seats.keys(), available_seats.values(), label="Available")
    ax.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    imdata = base64.b64encode(buf.read()).decode("ascii")
    return render_template("graph.html", mimetype="buf/png", cache_timeout=0, imdata=imdata)

