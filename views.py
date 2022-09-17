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
        logger.log('Создание нового жанра')
        context = {
            'title': 'Новый жанр',
            'genre': engine.genre
        }
        if request['method'] == 'POST':
            genre_name = request['data']['genre_name']
            new_genre = engine.create_genre(genre_name)
            engine.genre.append(new_genre)
            context = {'genre': engine.genre, 'title': 'Главная'}
            logger.log(f'Создан жанр {genre_name}')
            return '200 OK', render('index.html', context=context, request=request)
        return '200 OK', render('create_genre.html', request=request, context=context)


class CreateFilm:
    def __call__(self, request):
        logger.log(f'Создание нового фильма')
        context = {
            'title': 'Новый фильм',
            'genre': engine.genre,
            'film_types': FilmFactory.types.keys()
        }
        if request['method'] == 'POST':
            film_type = request['data']['types_list']
            film_name = request['data']['film_name']
            film_actors = request['data']['film_actors']
            film_director = request['data']['film_director']
            genre_list = request['data']['genre_list']
            genre = engine.find_genre_by_name(genre_list)
            new_film = engine.create_film(film_type, film_name, film_actors, film_director, genre)
            engine.films.append(new_film)
            context['title'] = 'Каталог'
            obj_list = engine.films
            logger.log(f'Создан фильм - {film_name}')
            return '200 OK', render('catalog.html', request=request, context=context, objects_list=obj_list)
        return '200 OK', render('create_film.html', request=request, context=context)


class CopyFilm:
    def __call__(self, request):
        logger.log('Копирование фильма')
        context = {
            'title': 'Каталог',
            'genre': engine.genre
        }
        request_param = request['request_param']
        try:
            name = request_param['name']
            old_film = engine.get_film(name)
            if old_film:
                new_name = f'copy_{name}'
                new_film = old_film.clone()
                new_film.name = new_name
                engine.films.append(new_film)
            obj_list = engine.films
            logger.log(f'Создана копия фильма {old_film.name}')
            return '200 OK', render('catalog.html', request=request, objects_list=obj_list, context=context)
        except KeyError:
            return '200 OK', 'No films have been added yet'


