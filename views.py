from framework.templator import render


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
        context = {'title': 'Каталог'}
        return '200 OK', render('catalog.html', request=request)

    def __repr__(self):
        return self.__class__.__name__
