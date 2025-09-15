from flask import render_template
from application.webapp import WebApp
import uuid

webapp = WebApp(__name__)

@webapp.get_engine().route('/')
@webapp.get_engine().route('/index')
def index():
    return render_template("index.html", title="Home")

@webapp.get_engine().route('/task/<uuid:task_id>')
def task(task_id: uuid.UUID):
    return render_template("task.html", title="Task Details", task_id=str(task_id))

webapp.start()
