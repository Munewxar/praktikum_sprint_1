import uuid
from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class FilmWork:
    title: str
    description: str
    creation_date: date
    rating: float
    type: str
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.id = uuid.UUID(self.id)

        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)

        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.id = uuid.UUID(self.id)

        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)

        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)


@dataclass
class Person:
    full_name: str
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.id = uuid.UUID(self.id)

        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)

        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)


@dataclass
class GenreFilmWork:
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: datetime = field(default=datetime.now())
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.id = uuid.UUID(self.id)
        self.genre_id = uuid.UUID(self.genre_id)
        self.film_work_id = uuid.UUID(self.film_work_id)

        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)


@dataclass
class PersonFilmWork:
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created_at: datetime = field(default=datetime.now())
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.id = uuid.UUID(self.id)
        self.person_id = uuid.UUID(self.person_id)
        self.film_work_id = uuid.UUID(self.film_work_id)

        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)


TableType = FilmWork | Genre | Person | GenreFilmWork | PersonFilmWork
