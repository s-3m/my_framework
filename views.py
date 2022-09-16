from framework.templator import render
from patterns.creational import Engine, Logger

engine = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        context = {'title': 'Главная'}
        return '200 OK', render('index.html', request=request, context=context)

    def __repr__(self):
        return self.__class__.__name__


class Contact:
    def __call__(self, request):
        context = {'title': 'Контакты'}
        return '200 OK', render('contact.html', request=request, context=context)

    def __repr__(self):
        return self.__class__.__name__


class About:
    def __call__(self, request):
        context = {'title': 'О проекте'}
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
