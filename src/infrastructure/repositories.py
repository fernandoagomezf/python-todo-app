from uuid import UUID
from domain.tasks import Task
from infrastructure.database import Database
from infrastructure.database import DatabaseRepository
from infrastructure.models import DataTask

class TaskRepository(DatabaseRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    def _map_to_domain(self, dto: DataTask) -> Task:
        task = Task(dto.subject)
        task._id = dto.id
        task._code = dto.code
        task._due_date = dto.due_date 
        task._status = dto.status
        task._priority = dto.priority
        task._progress = dto.progress
        task._notes = dto.notes
        return task
    
    def _map_to_dto(self, task: Task) -> DataTask:
        dto = DataTask()
        dto.id = task.get_id()
        dto.code = task.get_code()
        dto.subject = task.get_subject()
        dto.due_date = task.get_due_date()
        dto.status = task.get_status()
        dto.priority = task.get_priority()
        dto.progress = task.get_progress()
        dto.notes = task.get_notes()
        return dto

    def get_all(self) -> list["Task"]:
        db = self.get_db()
        with db.ctx():
            dto = db.get_db().session.query(Task).all()
        return [self._map_to_domain(task) for task in dto]
    
    def get_by_id(self, id: UUID) -> "Task | None":
        if id is None:
            raise ValueError("ID cannot be null")
        db = self.get_db()
        with db.ctx():
            dto = db.get_db().session.query(DataTask).filter_by(id=id).first()
            if dto is None:
                raise ValueError(f"Task with ID '{id}' not found")
            return self._map_to_domain(dto)

    def get_by_code(self, code: str) -> "Task | None":
        if code is None or code == "":
            raise ValueError("Code cannot be null or empty")
        db = self.get_db()
        with db.ctx():
            return db.get_db().session.query(Task).filter_by(code=code).first()

    def add(self, task: "Task") -> None:
        if task is None:
            raise ValueError("Task cannot be null")
        dto = self._map_to_dto(task)
        db = self.get_db()
        with db.ctx():
            db.get_db().session.add(dto)
            db.get_db().session.commit()

    #def list_all(self) -> list["Task"]:
    #    db = self.get_db()
    #    with db.ctx():
    #        return db.get_db().session.query(Task).all()
        
    def remove(self, task: "Task") -> None:
        if task is None:
            raise ValueError("Task cannot be null")
        dto = self._map_to_dto(task)
        db = self.get_db()
        with db.ctx():
            db.get_db().session.delete(dto)
            db.get_db().session.commit()

    def update(self, task: "Task") -> None:
        if task is None:
            raise ValueError("Task cannot be null")
        dto = self._map_to_dto(task)
        db = self.get_db()
        with db.ctx():
            db.get_db().session.merge(dto)
            db.get_db().session.commit()