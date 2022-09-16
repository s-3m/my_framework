from copy import deepcopy
from quopri import decodestring


class AbstractPerson:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


class Actor(AbstractPerson):
    post = 'actor'


class Director(AbstractPerson):
    post = 'director'


class PersonFactory:
    types = {
        'actor': Actor,
        'director': Director
    }

    @classmethod
    def create(cls, type_, name, surname):
        return cls.types[type_](name, surname)


class Genre:
    auto_id = 0

    def __init__(self, name):
        self.id = Genre.auto_id
        Genre.auto_id += 1
        self.name = name
        self.films = []

    def genre_count(self):
        return len(self.films)


class FilmPrototype:
    def clone(self):
        return deepcopy(self)


class Film(FilmPrototype):
    def __init__(self, name, actor, director, genre: Genre):
        self.name = name
        self.actor = actor
        self.director = director
        self.genre = genre
        self.genre.films.append(self)


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

