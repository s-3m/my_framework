from quopri import decodestring
from framework.type_requests import PostRequest, GetRequest


class PageNotFound:
    def __call__(self, *args, **kwargs):
        return '404 WHAT', '404 page not found'


class BananaFramework:
    def __init__(self, routes, routes_dict, fronts=None):
        self.routes = routes
        self.routes_dict = routes_dict
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        # pprint(environ)

        if not path.endswith('/'):
            path = path + '/'

        if path in self.routes:
            view = self.routes[path]
        elif path in self.routes_dict:
            view = self.routes_dict[path]
        else:
            view = PageNotFound()

        request = {}

        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_request_param(environ)
            request['data'] = BananaFramework.decode_data(data)
            print(f'Input POST request with params: {request["data"]}')
        if method == 'GET':
            data = GetRequest().get_request_param(environ)
            request['request_param'] = BananaFramework.decode_data(data)
            print(f'Input GET request with params: {request["request_param"]}')

        if self.fronts is not None:
            for front in self.fronts:
                front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_data(data: dict):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
