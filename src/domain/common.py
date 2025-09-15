import uuid

class Entity():
    _id: uuid.UUID

    def __init__(self, id: uuid.UUID | None = None):
        if id is None:
            self._id = uuid.uuid4()
        else:
            self._id = id

    def get_id(self) -> uuid.UUID:
        return self._id
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id!r})"
    
class ValueObject():
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__!r})"
    
class DomainEvent(ValueObject):
    _code: str
    _bounded_context: str
    _entity_name: str

    def __init__(self, code: str, bounded_context: str, entity_name: str):
        self._code = code
        self._bounded_context = bounded_context
        self._entity_name = entity_name

    def get_code(self) -> str:
        return self._code
    
    def get_bounded_context(self) -> str:
        return self._bounded_context
    
    def get_entity_name(self) -> str:
            return self._entity_name
    
class AggregateRoot(Entity):
    def __init__(self, id: uuid.UUID | None = None):
        super().__init__(id)
        self._events: list[DomainEvent] = []

    def add_event(self, event: DomainEvent) -> None:
        if event is None:
            raise ValueError("Event cannot be null")
        self._events.append(event)

    def remove_event(self, event: DomainEvent) -> None:
        if event is None:
            raise ValueError("Event cannot be null")
        if event in self._events:
            self._events.remove(event)

    def pull_events(self) -> list[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events

    def get_events(self) -> list[DomainEvent]:
        return list(self._events)

    def clear_events(self) -> None:
        self._events.clear()