from framework.templator import render
from patterns.creational import Engine, Logger, FilmFactory

engine = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        context = {'title': 'Главная', 'genre': engine.genre}
        return '200 OK', render('index.html', request=request, context=context)

    def __repr__(self):
        return self.__class__.__name__


class Contact:
    def __call__(self, request):
        context = {'title': 'Контакты', 'genre': engine.genre}
        return '200 OK', render('contact.html', request=request, context=context)

    def __repr__(self):
        return self.__class__.__name__


class About:
    def __call__(self, request):
        context = {'title': 'О проекте', 'genre': engine.genre}
        return '200 OK', render('about.html', request=request, context=context)

    def __repr__(self):
        return self.__class__.__name__


class Catalog:
    def __call__(self, request):
        context = {
            'title': 'Каталог',
            'genre': engine.genre
        }
        objects_list = engine.films
        return '200 OK', render('catalog.html', request=request, context=context, objects_list=objects_list)

    def __repr__(self):
        return self.__class__.__name__


class CreateGenre:
    def __call__(self, request):
        context = {
            'title': 'Новый жанр',
            'genre': engine.genre
        }
        if request['method'] == 'POST':
            genre_name = request['data']['genre_name']
            new_genre = engine.create_genre(genre_name)
            engine.genre.append(new_genre)
            context = {'genre': engine.genre, 'title': 'Главная'}
            return '200 OK', render('index.html', context=context, request=request)
        return '200 OK', render('create_genre.html', request=request, context=context)


class CreateFilm:
    def __call__(self, request):
        context = {
            'title': 'Новый жанр',
            'genre': engine.genre,
            'film_types': FilmFactory.types.keys()
        }
        return '200 OK', render('create_film.html', request=request, context=context)
