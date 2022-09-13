class GetRequest:

    @staticmethod
    def pars_params(params: str):
        result = {}
        if params:
            data = params.split('&')
            for item in data:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_request_param(environ):
        query_string: str = environ['QUERY_STRING']
        query_params = GetRequest.pars_params(query_string)
        return query_params


class PostRequest:

    @staticmethod
    def pars_params(params: str):
        result = {}
        if params:
            data = params.split('&')
            for item in data:
                k, v = item.split('=')
                result[k] = v
        return result

    @classmethod
    def get_wsgi_data(cls, env) -> bytes:
        content_len_data = env.get('CONTENT_LENGTH')
        content_len = int(content_len_data) if content_len_data else 0
        print(content_len)

        data = env['wsgi.input'].read(content_len) if content_len > 0 else b''
        return data

    def pars_wsgi_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            print(f'String after decoding - {data_str}')

            result = PostRequest.pars_params(data_str)
        return result

    def get_request_param(self, environ):
        data = PostRequest.get_wsgi_data(environ)
        data = self.pars_wsgi_data(data)
        return data
