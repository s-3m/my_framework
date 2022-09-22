from pprint import pprint

from jinja2 import Environment, FileSystemLoader
from jinja2.ext import Markup


def render(template_name, **kwargs):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    tm = env.get_template(template_name)
    env.globals['static_prefix'] = '/'
    if 'context' not in kwargs:
        kwargs['context'] = {}
    return tm.render(**kwargs)


if __name__ == '__main__':
    test = render('index.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    print(test)
