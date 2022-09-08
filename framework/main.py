class PageNotFound:
    def __call__(self, *args, **kwargs):
        return '404 WHAT', '404 page not found'


class BananaFramework:
    def __init__(self, routes, fronts=None):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = path + '/'

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound()

        request = {}

        if self.fronts is not None:
            for front in self.fronts:
                front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
