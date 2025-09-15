import os
from flask import Flask
from infrastructure.database import Database
from application.controllers import Controller

class Config():
    _basedir = os.path.abspath(os.path.dirname(__file__))
    _parentdir = os.path.abspath(os.path.join(_basedir, os.pardir))
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(_parentdir, 'todo.db')
    DEBUG = True

class WebApp():
    _engine: Flask
    _db: Database
    _map: dict[str, dict[str, Controller]]
    
    def __init__(self, name:str):
        self._engine = Flask(name)
        self._engine.config.from_object(Config)
        self._db = Database(self._engine, Config.SQLALCHEMY_DATABASE_URI)
        self._map = { }
        self._db.create()

    def get_engine(self) -> Flask:
        return self._engine    
    
    def get_db(self) -> Database:
        return self._db
    
    def start(self):
        self._engine.run(debug=Config.DEBUG)

    def register(self, section:str, controller: Controller) -> None:
        if section is None or section == "":
            raise ValueError("Section cannot be null or empty")
        if controller is None:
            raise ValueError("Controller cannot be null")
        self._map[section] = controller

    def route(self, section: str, action: str, data: dict[str, any] = {}) -> any:
        data = data or {}
        ctrl = self._map.get(section)
        if ctrl is None:
            raise ValueError(f"Section '{section}' not found")
        return ctrl.invoke(action, data)
