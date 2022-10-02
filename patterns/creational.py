from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect

from patterns.behavioral import Subject
from patterns.architectural_unut_of_work import DomainObject


class AbstractPerson:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __str__(self):
        return f'{self.name} {self.surname}'


class Actor(AbstractPerson, DomainObject):
    post = 'actor'


class Director(AbstractPerson, DomainObject):
    post = 'director'


class PersonFactory:
    types = {
        'actor': Actor,
        'director': Director
    }

    @classmethod
    def create(cls, type_, name, surname):
        return cls.types[type_](name, surname)


class Genre(DomainObject):
    auto_id = 0

    def __init__(self, name):
        self.id = Genre.auto_id
        Genre.auto_id += 1
        self.name = name
        self.films = []

    def __str__(self):
        return self.name

    def genre_count(self):
        return len(self.films)


class FilmPrototype:
    def clone(self):
        return deepcopy(self)


class Film(FilmPrototype, Subject, DomainObject):
    def __init__(self, name, actor, director, genre: Genre):
        super().__init__()
        self.name = name
        self.actor = actor
        self.director = director
        self.genre = genre
        self.films = []
        self.genre.films.append(self)
        self.films.append(self)


class ThreeDFilm(Film):
    type = '3D'


class FutureReleased(Film):
    type = 'Future released'


class FilmFactory:
    types = {
        'threeD': ThreeDFilm,
        'future_released': FutureReleased
    }

    @classmethod
    def create(cls, type_, name, actor, director, genre: Genre):
        return FilmFactory.types[type_](name, actor, director, genre)


class Engine:
    def __init__(self):
        self.actor = []
        self.director = []
        self.films = []
        self.genre = []

    @staticmethod
    def create_person(type_, name, surname):
        return PersonFactory.create(type_, name, surname)

    @staticmethod
    def create_genre(name):
        return Genre(name)

    @staticmethod
    def create_film(type_, name, actor, director, genre):
        return FilmFactory.create(type_, name, actor, director, genre)

    def get_film(self, name):
        for item in self.films:
            if item.name == name:
                return item
            return None

    def find_genre_by_name(self, genre_name):
        for i in self.genre:
            if i.name == genre_name:
                return i

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)


class FilmsMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'films'

    def all(self):
        sql_text = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(sql_text)
        result = []

        for item in self.cursor.fetchall():
            id, name, actor, director, genre = item
            genre_obj = Engine.create_genre(genre)
            item = Film(name, actor, director, genre_obj)
            item.id = id
            result.append(item)
        return result

    def find_by_id(self, id):
        sql_text = f"SELECT id, type, name, actor, director, genre FROM {self.tablename} WHERE id=?"
        self.cursor.execute(sql_text, (id,))
        result = self.cursor.fetchone()
        if result:
            return Engine.create_film(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        sql_text = f"INSERT INTO {self.tablename} (name, actor, director, genre) VALUES (?, ?, ?, ?)"
        self.cursor.execute(sql_text, (obj.name, obj.actor, obj.director, obj.genre.name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        sql_text = f"UPDATE {self.tablename} SET name=?, actor=?, director=?, genre=? WHERE id=?"
        self.cursor.execute(sql_text, (obj.name, obj.actor, obj.director, obj.genre))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        sql_text = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(sql_text, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)



class BasePersonMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = ''
        self.instance = None

    def all(self):
        sql_text = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(sql_text)
        result = []

        for item in self.cursor.fetchall():
            id, name, surname = item
            item = self.instance(name, surname)
            item.id = id
            result.append(item)
        return result

    def find_by_id(self, id):
        sql_text = f"SELECT id, name, surname FROM {self.tablename} WHERE id=?"
        self.cursor.execute(sql_text, (id,))
        result = self.cursor.fetchone()
        if result:
            return self.instance(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        sql_text = f"INSERT INTO {self.tablename} (name, surname) VALUES (?, ?)"
        self.cursor.execute(sql_text, (obj.name, obj.surname))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        sql_text = f"UPDATE {self.tablename} SET name=?, surname=? WHERE id=?"
        self.cursor.execute(sql_text, (obj.name, obj.surname, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        sql_text = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(sql_text, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class ActorMapper(BasePersonMapper):
    def __init__(self, connection):
        super().__init__(connection)
        self.instance = Actor
        self.tablename = 'actors'


class DirectorMapper(BasePersonMapper):
    def __init__(self, connection):
        super().__init__(connection)
        self.instance = Director
        self.tablename = 'directors'


class GenreMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'genres'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Genre(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Genre(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_by_name(self, name):
        statement = f"SELECT id, name FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        if result:
            return Genre(result[1])
        else:
            raise RecordNotFoundException(f'record with id={id} not found')


    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('my_base.sqlite')


class MapperRegistry:
    mappers = {
        'actor': ActorMapper,
        'director': DirectorMapper,
        'genre': GenreMapper,
        'film': FilmsMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Actor):
            return ActorMapper(connection)
        elif isinstance(obj, Director):
            return DirectorMapper(connection)
        elif isinstance(obj, Genre):
            return GenreMapper(connection)
        elif isinstance(obj, Film):
            return FilmsMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
