import httpx
from environs import Env

env: Env = Env()
env.read_env('.env')


TOKEN = env('TOKEN')
API_URL = env('API_URL')


def get_information(self, type_request):
    try:
        params = {'type': type_request, 'vin': self.vin, 'token': TOKEN}
        response = httpx.get(API_URL, params=params).json()
    except Exception as error:
        raise ConnectionError(
            f'При выполнении запроса произошла ошибка - {error}'
        )
    status = response.get('status')
    if status != 200 or (status == 200 and not response.get('count')):
        message = response.get('message')
        raise ConnectionError(
            f'Некорректный ответ от сервера {message}'
        )
    return {'records': response.get('records')}
