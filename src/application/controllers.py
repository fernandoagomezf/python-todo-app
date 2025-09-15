from flask import Flask
from flask import render_template
from flask import flash
from typing import Any
from typing import Callable

class Controller():    
    def __init__(self):
        self._routes = self.build_routes()

    
    
    