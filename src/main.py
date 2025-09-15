from flask import render_template
from uuid import UUID
from application.webapp import WebApp
from application.controllers import HomeController

webapp = WebApp(__name__)
webapp.register("home", HomeController())

@webapp.get_engine().route("/")
@webapp.get_engine().route("/index")
@webapp.get_engine().route("/home/index")
def home_index():
    return webapp.route("home", "get_index")

@webapp.get_engine().route("/about")
def home_about():
    return webapp.route("home", "get_about")

@webapp.get_engine().route('/task/<uuid:task_id>')
def task_detail(id: UUID):
    return webapp.route("task", "detail", {"id": id})

webapp.start()
