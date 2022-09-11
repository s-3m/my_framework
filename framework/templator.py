from jinja2 import Environment, FileSystemLoader


def render(template_name, **kwargs):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    tm = env.get_template(template_name)
    if 'context' not in kwargs:
        kwargs['context'] = {}
    return tm.render(**kwargs)


if __name__ == '__main__':
    test = render('index.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    print(test)
