from datetime import datetime
from datetime import timezone
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import uuid

class Entity(DeclarativeBase):
    pass

class Task(Entity):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    code: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        nullable=False
    )
    subject: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )
    due_date: Mapped[datetime] = mapped_column(
        nullable=False, 
        default=lambda: datetime.now(timezone.utc)
    )
    status: Mapped[int] = mapped_column(
        nullable=False, 
        default=0
    )
    priority: Mapped[int] = mapped_column(
        nullable=False, 
        default=0
    )
    progress: Mapped[float] = mapped_column(
        nullable=False, 
        default=0.0
    )
    notes: Mapped[str] = mapped_column(
        String(1000), 
        nullable=True
    )

    def __repr__(self) -> str:
        return f'<Task {self.code}: {self.subject}>'

    