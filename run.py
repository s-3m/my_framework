from wsgiref.simple_server import make_server
from framework.main import BananaFramework
from urls import routes
from front_control import fronts_list

banana = BananaFramework(routes=routes, fronts=fronts_list)
with make_server('', 8000, banana) as httpd:
    print('Start server with port 8000...')
    httpd.serve_forever()

