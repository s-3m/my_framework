from wsgiref.simple_server import make_server


class PageNotFound:
    def __call__(self, *args, **kwargs):
        return '404 WHAT', [b'404 page not found']


class BananaFramework:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endwith('/'):
            path = path + '/'

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound()

        request = {}

        for front in self.fronts:
            front(request)

        code, body = view()
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
