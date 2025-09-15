from typing import Any
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from infrastructure.models import Entity
from infrastructure.models import Task

class Database():
    _db : SQLAlchemy
    _engine: Flask
    _cnnstr: str
    def __init__(self, engine, cnnstr):
        if engine is None:
            raise ValueError("Engine cannot be null")
        if cnnstr is None or cnnstr == "":
            raise ValueError("Connection string cannot be null or empty")
        
        self._cnnstr = cnnstr
        self._engine = engine
        self._db = SQLAlchemy(model_class=Entity)
        self._db.init_app(engine)

    def ctx(self) -> Any:
        return self._engine.app_context()

    def get_db(self) -> SQLAlchemy:
        return self._db
    
    def get_engine(self) -> Flask:
        return self._engine
    
    def get_cnnstr(self) -> str:
        return self._cnnstr
    
    def create(self) -> None:
        with self._engine.app_context():
            self._db.create_all()

class Repository():
    _db: Database

    def __init__(self, db: Database):
        if db is None:
            raise ValueError("Context cannot be null")
        self._db = db

    def get_db(self) -> Database:
        return self._db

class TaskRepository(Repository):
    def __init__(self, db: Database):
        super().__init__(db)

    def get_all(self) -> list["Task"]:
        db = self.get_db()
        with db.ctx():
            return db.session.query(Task).all()

    def get_by_code(self, code: str) -> "Task | None":
        db = self.get_db()
        with db.ctx():
            return db.session.query(Task).filter_by(code=code).first()

    def add(self, task: "Task") -> None:
        db = self.get_db()
        with db.ctx():
            db.session.add(task)
            db.session.commit()

    def list_all(self) -> list["Task"]:
        db = self.get_db()
        with db.ctx():
            return db.session.query(Task).all()
        
    def remove(self, task: "Task") -> None:
        db = self.get_db()
        with db.ctx():
            db.session.delete(task)
            db.session.commit()

    def update(self, task: "Task") -> None:
        db = self.get_db()
        with db.ctx():
            db.session.merge(task)
            db.session.commit()

