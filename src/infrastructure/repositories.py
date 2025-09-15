from domain.tasks import Task
from infrastructure.database import Database
from infrastructure.database import DatabaseRepository
from infrastructure.models import DataTask

class TaskRepository(DatabaseRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    def _map_to_domain(self, dto: DataTask) -> Task:
        task = Task(task.subject)
        task._id = dto.id
        task._code = dto.code
        task._due_date = dto.due_date
        task._status = dto.status
        task._priority = dto.priority
        task._progress = dto.progress
        task._notes = dto.notes
        return task

    def get_all(self) -> list["Task"]:
        db = self.get_db()
        with db.ctx():
            dto = db.session.query(Task).all()
        return [self._map_to_domain(task) for task in dto]

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