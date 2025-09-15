from flask import Flask
from flask import render_template
from flask import flash
from typing import Any, Callable

class Controller():    
    _actions: dict[str, Callable[[dict[str, Any]], Any]]
    def __init__(self):
        self._actions = { }

    def map(self, action: str, func: Callable[[dict[str, Any]], Any]) -> None:
        if action is None or action == "":
            raise ValueError("Action cannot be null or empty")
        if func is None:
            raise ValueError("Function cannot be null")
        self._actions[action] = func
    
    def invoke(self, action: str, data:dict[str, Any]) -> Any:
        if action is None or action == "":
            raise ValueError("Action cannot be null or empty")
        data = data or { }
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
    def __init__(self):
        super().__init__()
        self.map("get_index", self.index)
        self.map("get_about", self.about)

    def index(self, _) -> Any:
        return render_template("home/index.html", title="Home")
    
    def about(self, _) -> Any:
        return render_template("home/about.html", title="About")

class TaskController(Controller):
    def __init__(self):
        super().__init__()
        self.map("get_index", self.index)

    def index(self, _) -> Any:
        return render_template("task/index.html", title="Tasks")

    