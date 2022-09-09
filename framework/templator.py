from jinja2 import Template, Environment, FileSystemLoader


def render(template_name, **kwargs):
    # with open(template_name, encoding='utf-8') as f:
    #     template = Template(f.read())
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    tm = env.get_template(template_name)
    return tm.render(**kwargs)


if __name__ == '__main__':
    test = render('index.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    print(test)
