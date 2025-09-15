import os
from flask import Flask
from infrastructure.database import Database

class Config():
    _basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(_basedir, 'app.db')
    DEBUG = True

class WebApp():
    _engine: Flask
    _db: Database
    
    def __init__(self, name:str):
        self._engine = Flask(name)
        self._engine.config.from_object(Config)
        self._db = Database(self._engine, Config.SQLALCHEMY_DATABASE_URI)
        self._db.create()

    def get_engine(self) -> Flask:
        return self._engine    
    
    def get_db(self) -> Database:
        return self._db
    
    def start(self):
        self._engine.run(debug=Config.DEBUG)



    