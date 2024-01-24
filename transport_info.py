import httpx
from environs import Env

env: Env = Env()
env.read_env('.env')


TOKEN = env('TOKEN')
API_URL = env('API_URL')


class TransportInfo:
    def __init__(
            self,
            vin: str,
            reg_number: str | None,
            sts_number: str | None):
        self.vin = vin
        self.reg_number = reg_number
        self.sts_number = sts_number

    def get_gibdd_information(self):
        """Метод, получающий основную информацию по VIN номеру."""

        try:
            params = {'type': 'gibdd', 'vin': self.vin, 'token': TOKEN}
            response = httpx.get(API_URL, params=params).json()
        except Exception as error:
            raise ConnectionError(
                f'При выполнении запроса произошла ошибка - {error}'
            )
        status = response.status
        if status in (404, 503) or (status == 200 and response.message):
            raise ConnectionError(
                f'Некорректный ответ от сервера {response.message}'
            )
        return {
            'vehicle': response.vehicle,
            'vehiclePassport': response.vehiclePassport,
            'ownershipPeriod': response.ownershipPeriod
        }
