from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID
from infrastructure.database import Database
from infrastructure.models import DataTask

@dataclass(frozen=True)
class QueryResult:
    items: list[Any]
    total: int
    page_index: int
    page_size: int
    page_count: int

class Query:
    _db : Database
    _page_index : int 
    _page_size : int

    def __init__(self, db: Database):
        if db is None:
            raise ValueError("Database cannot be null")
        self._db = db
        self._page_index = 1
        self._page_size = 10

    def get_db(self) -> Database:
        return self._db
    
    def get_page_index(self) -> int:
        return self._page_index
    
    def set_page_index(self, index: int) -> None:
        if index < 1:
            raise ValueError("Page index must be greater than 0")
        self._page_index = index

    def get_page_size(self) -> int:
        return self._page_size
    
    def set_page_size(self, size: int) -> None:
        if size < 2:
            raise ValueError("Page size must be greater than 1")
        self._page_size = size
    
    def execute(self) -> QueryResult:
        pass

    def _paginate(self, query) -> QueryResult:
        page_index = self.get_page_index()
        page_size = self.get_page_size()
        total = query.count()
        items = query.offset((page_index - 1) * page_size).limit(page_size).all()
        result = QueryResult(
            items=items,
            total=total,
            page_index=page_index,
            page_size=page_size,
            page_count=(total + page_size - 1) // page_size
        )
        return result

class GetAllTasksQuery(Query):
    def execute(self) -> QueryResult:
        db = self.get_db()
        with db.ctx():
            query = db.get_db().session.query(DataTask)
            return self._paginate(query)

@dataclass(frozen=True)
class Summary:
    pending: int
    in_progress: int
    closed: int
    total: int
    overdue: int
    high_priority: int
    normal_priority: int

class GetSummaryQuery(Query):
    def execute(self) -> QueryResult:
        db = self.get_db()
        self._page_index = 1
        self._page_size = 1000
        with db.ctx():
            query = db.get_db().session.query(DataTask)
            result = self._paginate(query)
            summary = Summary(
                pending=sum(1 for item in result.items if item.status == 0),
                in_progress=sum(1 for item in result.items if item.status == 1),
                closed=sum(1 for item in result.items if item.status == 2),
                total=len(result.items),
                overdue=sum(1 for item in result.items if item.due_date.date() < datetime.now().date() and item.status != 2),
                high_priority=sum(1 for item in result.items if item.priority == 2),
                normal_priority=sum(1 for item in result.items if item.priority == 1)
            )
            return QueryResult(
                items=[summary],
                total=1,
                page_index=1,
                page_size=1,
                page_count=1
            )
            
