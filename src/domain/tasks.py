from datetime import datetime, timedelta
from enum import Enum
from domain.common import AggregateRoot
import uuid

class TaskStatus(Enum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    CANCELLED = 3

class TaskPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2

class Task(AggregateRoot):
    _code: str
    _subject: str
    _due_date: datetime
    _status: int
    _priority: int
    _progress: float
    _notes: str | None

    def __init__(
        self, 
        subject: str
    ):
        super().__init__(None)

        if len(subject) == 0:
            raise ValueError("Subject cannot be empty")

        self._code = str(uuid.uuid4())[:8]
        self._subject = subject
        self._due_date = datetime.now().date()
        self._status = TaskStatus.PENDING.value
        self._priority = TaskPriority.NORMAL.value
        self._progress = 0.0
        self._notes = str()
    
    def __str__(self) -> str:
        return f"Task(id={self.get_id()}, code={self._code}, subject={self._subject})"
    
    def __repr__(self) -> str:
        return f"Task(id={self.get_id()!r}, code={self._code!r}, subject={self._subject!r})"

    def get_code(self) -> str:
        return self._code
    
    def get_subject(self) -> str:
        return self._subject
    
    def get_due_date(self) -> str:
        return self._due_date
    
    def get_status(self) -> int:
        return self._status
    
    def get_priority(self) -> int:
        return self._priority
    
    def get_progress(self) -> float:
        return self._progress
    
    def get_notes(self) -> str | None:
        return self._notes
    
    def update_content(self, *, subject: str = None, notes: str = None) -> None:
        if subject is not None:
            if len(subject) == 0:
                raise ValueError("Subject cannot be empty")
            self._subject = subject
        if notes is not None:
            self._notes = notes

    def move_due_date(self, *, days: int = None, new_date: datetime = None) -> None:
        if new_date is None and days is None:
            raise ValueError("Either days or new_date must be provided")
        if new_date is not None:
            if new_date < datetime.now().date():
                raise ValueError("New date cannot be in the past")
            self._due_date = new_date
        if days is not None:
            self._due_date += timedelta(days=days)

    def report_progress(self, progress: float) -> None:
        if progress < 0.0 or progress > 100.0:
            raise ValueError("Progress must be between 0 and 100")
        self._progress = progress
        if self._progress == 100.0:
            self._status = TaskStatus.COMPLETED.value
        elif self._progress > 0.0:
            self._status = TaskStatus.IN_PROGRESS.value
        else:
            self._status = TaskStatus.PENDING.value

    def complete(self) -> None:
        self.report_progress(100.0)

    def cancel(self) -> None:
        self._status = TaskStatus.CANCELLED.value
        self._progress = 0.0

    def promote(self) -> None:
        if self._priority != TaskPriority.HIGH.value:
            self._priority = TaskPriority.HIGH.value if self._priority == TaskPriority.NORMAL.value else TaskPriority.NORMAL.value 

    def demote(self) -> None:
        if self._priority != TaskPriority.LOW.value:
            self._priority = TaskPriority.NORMAL.value if self._priority == TaskPriority.HIGH.value else TaskPriority.LOW.value

