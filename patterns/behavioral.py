from framework.templator import render
from jsonpickle import dumps, loads


# Наблюдатель
class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for i in self.observers:
            i.update(self)


class SmsNotifier(Observer):
    def update(self, subject):
        print(f'SMS --> В Каталог добавлен новый фильм - {subject.films[-1].name}')


class EmailNotifier(Observer):
    def update(self, subject):
        print(f'E-mail --> В Каталог добавлен новый фильм - {subject.films[-1].name}')


class TemplateView:
    template_name = ''

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template(self, request, success_url=None):
        template_name = self.get_template()
        context = self.get_context_data()
        if success_url:
            view = request['routes_dict'][success_url]
            return view(request)
        return '200 OK', render(template_name, **context, request=request)

    def __call__(self, request):
        return self.render_template(request)


class ListView(TemplateView):
    queryset = []
    template_name = ''
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = ''
    success_url = None

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template(request, success_url=self.success_url)
        else:
            return super().__call__(request)


class Serializer:
    def __init__(self, obj):
        self.object = obj

    def save(self):
        return dumps(self.object)

    @staticmethod
    def load(data):
        return loads(data)
