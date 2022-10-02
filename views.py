from framework.templator import *
from patterns.creational import Engine, Logger, FilmFactory, MapperRegistry
from patterns.structural import AppRoute, Debug
from patterns.behavioral import SmsNotifier, EmailNotifier, CreateView, ListView, Serializer
from patterns.architectural_unut_of_work import UnitOfWork

engine = Engine()
logger = Logger('main')
routes = {}
sms_notif = SmsNotifier()
email_notif = EmailNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@AppRoute(url='/')
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


@AppRoute(url='/catalog/')
class Catalog(ListView):
    template_name = 'catalog.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('film')
        return mapper.all()

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Каталог'
        return context



    # def __call__(self, request):
    #     context = {
    #         'title': 'Каталог',
    #         'genre': engine.genre,
    #         'actors': engine.actor
    #     }
    #     objects_list = engine.films
    #     return '200 OK', render('catalog.html', request=request, context=context, objects_list=objects_list)
    #
    # def __repr__(self):
    #     return self.__class__.__name__


class CreateGenre(CreateView):
    template_name = 'create_genre.html'
    success_url = '/GenreList/'

    def create_obj(self, data):
        genre_name = data['genre_name']
        new_genre = engine.create_genre(genre_name)
        engine.genre.append(new_genre)
        new_genre.mark_new()
        UnitOfWork.get_current().commit()

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Новый жанр'
        mapper = MapperRegistry.get_current_mapper('genre')
        context['objects_list'] = mapper.all()
        return context


@AppRoute(url='/GenreList/')
class GenreList(ListView):
    template_name = 'genre_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('genre')
        return mapper.all()

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Жанры'
        return context


class CreateFilm(CreateView):
    template_name = 'create_film.html'
    success_url = '/catalog/'

    def create_obj(self, data):
        film_type = data['types_list']
        film_name = data['film_name']
        film_actors = data['film_actors']
        film_director = data['film_director']
        genre_list = data['genre_list']
        mapper_genre = MapperRegistry.get_current_mapper('genre')
        genre = mapper_genre.find_by_name(genre_list)
        new_film = engine.create_film(film_type, film_name, film_actors, film_director, genre)
        engine.films.append(new_film)
        new_film.mark_new()
        UnitOfWork.get_current().commit()
        new_film.observers.append(sms_notif)
        new_film.observers.append(email_notif)
        new_film.notify()

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Новый фильм'
        mapper_actor = MapperRegistry.get_current_mapper('actor')
        mapper_dir = MapperRegistry.get_current_mapper('director')
        mapper_genre = MapperRegistry.get_current_mapper('genre')
        context['genre'] = mapper_genre.all()
        context['actors'] = mapper_actor.all()
        context['directors'] = mapper_dir.all()
        context['film_types'] = FilmFactory.types.keys()
        return context

    # def __call__(self, request):
    #     logger.log(f'Создание нового фильма')
    #     context = {
    #         'title': 'Новый фильм',
    #         'genre': engine.genre,
    #         'film_types': FilmFactory.types.keys(),
    #         'actors': engine.actor,
    #         'directors': engine.director
    #     }
    #     if request['method'] == 'POST':
    #         film_type = request['data']['types_list']
    #         film_name = request['data']['film_name']
    #         film_actors = request['data']['film_actors']
    #         film_director = request['data']['film_director']
    #         genre_list = request['data']['genre_list']
    #         genre = engine.find_genre_by_name(genre_list)
    #         new_film = engine.create_film(film_type, film_name, film_actors, film_director, genre)
    #         engine.films.append(new_film)
    #         context['title'] = 'Каталог'
    #         obj_list = engine.films
    #         logger.log(f'Создан фильм - {film_name}')

        #     new_film.observers.append(sms_notif)
        #     new_film.observers.append(email_notif)
        #     new_film.notify()
        #
        #     return '200 OK', render('catalog.html', request=request, context=context, objects_list=obj_list)
        # return '200 OK', render('create_film.html', request=request, context=context)


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


@AppRoute(url='/AddActor/')
class CreateActor(CreateView):
    template_name = 'create_actor.html'
    success_url = '/ActorList/'

    def create_obj(self, data):
        actor_name = data['name']
        actor_surname = data['surname']
        new_actor = engine.create_person('actor', actor_name, actor_surname)
        engine.actor.append(new_actor)
        new_actor.mark_new()
        UnitOfWork.get_current().commit()

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Новый актер'
        mapper = MapperRegistry.get_current_mapper('actor')
        context['objects_list'] = mapper.all()
        return context


@AppRoute(url='/ActorList/')
class ActorList(ListView):
    template_name = 'actor_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('actor')
        return mapper.all()

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Актеры'
        return context


@AppRoute(url='/AddDirector/')
class CreateDirector(CreateView):
    template_name = 'create_actor.html'
    success_url = '/DirectorList/'

    def create_obj(self, data):
        dir_name = data['name']
        dir_surname = data['surname']
        new_dir = engine.create_person('director', dir_name, dir_surname)
        engine.director.append(new_dir)
        new_dir.mark_new()
        UnitOfWork.get_current().commit()

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Новый режиссер'
        mapper = MapperRegistry.get_current_mapper('director')
        context['objects_list'] = mapper.all()
        return context


@AppRoute(url='/DirectorList/')
class DirectorList(ListView):
    template_name = 'directors_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('director')
        return mapper.all()

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Режиссеры'
        return context


@AppRoute(url='/api/')
class FilmsApi:
    def __call__(self, request):
        return '200 OK', Serializer(engine.films).save()
