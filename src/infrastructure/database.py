from typing import Any
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from infrastructure.models import DataEntity
from infrastructure.models import DataTask

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
        self._db = SQLAlchemy(model_class=DataEntity)
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

class DatabaseRepository():
    _db: Database

    def __init__(self, db: Database):
        if db is None:
            raise ValueError("Context cannot be null")
        self._db = db

    def get_db(self) -> Database:
        return self._db



