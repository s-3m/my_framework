class Index:
    def __call__(self, *args, **kwargs):
        return '200 OK', [b'index page']


class Contact:
    def __call__(self, *args, **kwargs):
        return '200 OK', [b'Contacts page']


class About:
    def __call__(self, *args, **kwargs):
        return '200 OK', [b'About page']
