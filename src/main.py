
from uuid import UUID
from application.webapp import WebApp
from application.controllers import HomeController
from application.controllers import TaskController

webapp = WebApp(__name__)
webapp.register("home", HomeController())
webapp.register("task", TaskController())

@webapp.get_engine().route("/")
@webapp.get_engine().route("/index")
@webapp.get_engine().route("/home/index")
def home_index():
    return webapp.route("home", "get_index")

@webapp.get_engine().route("/home/about")
def home_about():
    return webapp.route("home", "get_about")

@webapp.get_engine().route('/task/index')
def task_index():
    return webapp.route("task", "get_index")

@webapp.get_engine().route('/task/<uuid:id>')
def task_detail(id: UUID):
    return webapp.route("task", "detail", {"id": id})

webapp.start()
