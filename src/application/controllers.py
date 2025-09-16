from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash
from typing import Any, Callable
from domain.tasks import Task
from infrastructure.database import Database
from infrastructure.queries import GetAllTasksQuery
from infrastructure.queries import GetSummaryQuery
from infrastructure.queries import GetTaskDetailQuery
from infrastructure.repositories import TaskRepository
from application.viewmodels import EditTaskViewModel, ViewModel
from application.viewmodels import NewTaskViewModel
from application.viewmodels import EditTaskViewModel
import uuid

class Controller():    
    _actions: dict[str, Callable[[dict[str, any]], Any]]
    def __init__(self):
        self._actions = { }

    def map(self, action: str, func: Callable[[dict[str, any]], Any]) -> None:
        if action is None or action == "":
            raise ValueError("Action cannot be null or empty")
        if func is None:
            raise ValueError("Function cannot be null")
        self._actions[action] = func

    def invoke(self, action: str, data: dict[str, any]) -> Any:
        if action is None or action == "":
            raise ValueError("Action cannot be null or empty")
        
        func = self._actions.get(action)
        if func is None:
            raise ValueError(f"Action '{action}' not found")
        return func(data)

    def message(self, message: str) -> None:
        flash(message, "info")

    def alert(self, message: str) -> None:
        flash(message, "warning")

    def error(self, message: str) -> None:
        flash(message, "danger")


class HomeController(Controller):
    _db : Database
    _tasksQuery : GetAllTasksQuery
    _summaryQuery : GetSummaryQuery
    def __init__(self, db: Database):
        super().__init__()
        if db is None:
            raise ValueError("Database cannot be null")
        self._db = db
        self._tasksQuery = GetAllTasksQuery(db)
        self._summaryQuery = GetSummaryQuery(db)
        self.map("get_index", self.index)
        self.map("get_about", self.about)

    def index(self, _) -> Any:
        self._tasksQuery.set_page_index(1)
        self._tasksQuery.set_page_size(5)
        tasks = self._tasksQuery.execute()
        summary = self._summaryQuery.execute()
        return render_template("home/index.html", title="Home", tasks=tasks.items, summary=summary.items)

    def about(self, _) -> Any:
        return render_template("home/about.html", title="About")

class TaskController(Controller):
    _db : Database
    _repository : TaskRepository
    _get_all_query: GetAllTasksQuery
    _get_detail_query: GetTaskDetailQuery

    def __init__(self, db: Database):
        super().__init__()
        if db is None:
            raise ValueError("Database cannot be null")
        self._db = db
        self._repository = TaskRepository(db)
        self._get_all_query = GetAllTasksQuery(db)
        self._get_detail_query = GetTaskDetailQuery(db)
        self.map("get_index", self.index)
        self.map("get_new", self.get_new)
        self.map("post_new", self.post_new)
        self.map("get_detail", self.get_detail)
        self.map("get_edit", self.get_edit)
        self.map("post_edit", self.post_edit)

    def index(self, _) -> Any:
        self._get_all_query.set_page_index(1)
        self._get_all_query.set_page_size(1000)
        result = self._get_all_query.execute()
        return render_template("task/index.html", title="Tasks", query=result)

    def get_new(self, _) -> Any:
        vm = NewTaskViewModel()
        return render_template("task/new.html", title="New Task", vm=vm)
    
    def post_new(self, data: dict[str, any]) -> Any:        
        if data is None:
            raise ValueError("Invalid data")

        task = Task(data["subject"])
        task.update_content(notes=data["notes"])
        task.move_due_date(new_date=data["due_date"])
        self._repository.add(task)

        self.message("Task created successfully")
        return redirect(url_for("task_index"))
    
    def get_edit(self, data: dict[str, any]) -> Any:
        id = data["id"]
        if id is None:
            self.error("Task ID is required")
            return redirect(url_for("task_index"))
        
        self._get_detail_query.set_page_index(1)
        self._get_detail_query.set_page_size(1)
        self._get_detail_query.set_id(id)
        result = self._get_detail_query.execute()
        if result is None or result.total <= 0:
            self.error("Task not found")
            return redirect(url_for("task_index"))
        
        vm = EditTaskViewModel()
        vm.id.data = str(result.items[0].id)
        vm.subject.data = result.items[0].subject
        vm.notes.data = result.items[0].notes
        vm.code.data = result.items[0].code
        return render_template("task/edit.html", title="Edit Task", vm=vm)
    
    def post_edit(self, data: dict[str, any]) -> Any:
        if data is None:
            raise ValueError("Invalid data")

        id = data["id"]
        if id is None:
            self.error("Task ID is required")
            return redirect(url_for("task_index"))
        
        task = self._repository.get_by_id(id)
        if task is None:
            self.error("Task not found")
            return redirect(url_for("task_index"))

        task.update_content(notes=data["notes"], subject=data["subject"])
        self._repository.update(task)

        self.message("Task updated successfully")
        return redirect(url_for("task_detail", task_id=id))

    def get_detail(self, data: dict[str, any]) -> Any:
        id = data["id"]
        if id is None:
            self.error("Task ID is required")
            return redirect(url_for("task_index"))
        
        self._get_detail_query.set_page_index(1)
        self._get_detail_query.set_page_size(1)
        self._get_detail_query.set_id(id)
        result = self._get_detail_query.execute()
        if result is None or result.total <= 0:
            self.error("Task not found")
            return redirect(url_for("task_index"))

        return render_template("task/detail.html", title="Task Detail", vm=result.items[0])