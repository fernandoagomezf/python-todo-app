from flask import Flask, redirect, url_for
from flask import render_template
from flask import flash
from typing import Any, Callable
from domain.tasks import Task
from infrastructure.database import Database
from infrastructure.queries import GetAllTasksQuery, GetSummaryQuery
from infrastructure.repositories import TaskRepository
from application.viewmodels import ViewModel
from application.viewmodels import NewTaskViewModel
import uuid

class Controller():    
    _actions: dict[str, Callable[[ViewModel], Any]]
    def __init__(self):
        self._actions = { }

    def map(self, action: str, func: Callable[[ViewModel], Any]) -> None:
        if action is None or action == "":
            raise ValueError("Action cannot be null or empty")
        if func is None:
            raise ValueError("Function cannot be null")
        self._actions[action] = func

    def invoke(self, action: str, vm: ViewModel) -> Any:
        if action is None or action == "":
            raise ValueError("Action cannot be null or empty")
        vm = vm or ViewModel()
        func = self._actions.get(action)
        if func is None:
            raise ValueError(f"Action '{action}' not found")
        return func(vm)

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
    _query: GetAllTasksQuery

    def __init__(self, db: Database):
        super().__init__()
        if db is None:
            raise ValueError("Database cannot be null")
        self._db = db
        self._repository = TaskRepository(db)
        self._query = GetAllTasksQuery(db)
        self.map("get_index", self.index)
        self.map("get_new", self.get_new)
        self.map("post_new", self.post_new)

    def index(self, _) -> Any:
        self._query.set_page_index(1)
        self._query.set_page_size(1000)
        result = self._query.execute()
        return render_template("task/index.html", title="Tasks", query=result   )

    def get_new(self, _) -> Any:
        vm = NewTaskViewModel()
        return render_template("task/new.html", title="New Task", form=vm)
    
    def post_new(self, vm: ViewModel) -> Any:        
        if vm is None:
            raise ValueError("Invalid view model")
        
        task = Task(vm.data["subject"])
        task.update_content(notes=vm.data["notes"])
        task.move_due_date(new_date=vm.data["due_date"])
        self._repository.add(task)

        self.message("Task created successfully")
        return redirect(url_for("task_index"))

    