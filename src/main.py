
from uuid import UUID
from application.webapp import WebApp
from application.controllers import HomeController
from application.controllers import TaskController
from application.viewmodels import NewTaskViewModel
from application.viewmodels import EditTaskViewModel
from infrastructure.repositories import TaskRepository

webapp = WebApp(__name__)
webapp.register("home", HomeController(webapp.get_db()))
webapp.register("task", TaskController(webapp.get_db()))

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

@webapp.get_engine().route('/task/new', methods=['GET', 'POST'])
def task_new():
    vm = NewTaskViewModel()
    if vm.validate_on_submit():
        data = {
            "subject": vm.subject.data,
            "notes": vm.notes.data,
            "due_date": vm.due_date.data,
        }
        return webapp.route("task", "post_new", data)
    return webapp.route("task", "get_new")

@webapp.get_engine().route('/task/edit/<uuid:task_id>', methods=['GET', 'POST'])
def task_edit(task_id: UUID):
    vm = EditTaskViewModel()
    if vm.validate_on_submit():
        data = {
            "id": task_id,
            "subject": vm.subject.data,
            "notes": vm.notes.data,
        }
        return webapp.route("task", "post_edit", data)
    return webapp.route("task", "get_edit", { "id": task_id })

@webapp.get_engine().route('/task/detail/<uuid:task_id>')
def task_detail(task_id: UUID):
    return webapp.route("task", "get_detail", { "id": task_id })

@webapp.get_engine().route('/task/complete/<uuid:task_id>', methods=["POST"])
def task_complete(task_id: UUID):
    return webapp.route("task", "post_complete", { "id": task_id })

webapp.start()
