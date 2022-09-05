from framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('templates/index.html', date=request['date'])

    def __repr__(self):
        return self.__class__.__name__


class Contact:
    def __call__(self, request):
        return '200 OK', render('templates/contact.html', date=request['date'])

    def __repr__(self):
        return self.__class__.__name__


class About:
    def __call__(self, request):
        return '200 OK', render('templates/about.html', date=request['date'])

    def __repr__(self):
        return self.__class__.__name__


