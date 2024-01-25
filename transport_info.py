import httpx

from utils import API_URL, TOKEN, get_information


class TransportInfo:
    def __init__(
            self,
            vin: str,
            reg_number: str | None,
            sts_number: str | None
    ):
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
        status = response.get('status')
        if status in (404, 503) or (status == 200 and response.get('message')):
            message = response.get('message')
            raise ConnectionError(
                f'Некорректный ответ от сервера {message}'
            )
        return {
            'vehicle': response.get('vehicle'),
            'vehiclePassport': response.get('vehiclePassport'),
            'ownershipPeriod': response.get('ownershipPeriod')
        }

    def get_fines_information(self):
        """Метод, получающий информацию по штрафам."""

        try:
            params = {
                'regNumber': self.reg_number,
                'type': 'fines',
                'stsNumber': self.sts_number,
                'token': TOKEN
            }
            response = httpx.get(API_URL, params=params).json()
        except Exception as error:
            raise ConnectionError(
                f'При выполнении запроса произошла ошибка - {error}'
            )
        status = response.get('status')
        if status != 200 or (status == 200 and not response.get('num')):
            message = response.get('message')
            raise ConnectionError(
                f'Некорректный ответ от сервера {message}'
            )
        return {'fines': response.get('rez')}

    def get_wanted_information(self):
        """Метод, получающий информацию о нахождении транспорта в розыске."""

        return get_information(self, type_request='wanted')

    def get_restrict_information(self):
        """Метод, получающий информацию об ограничениях."""

        return get_information(self, type_request='restrict')

    def get_dtp_information(self):
        """Метод, получающий информацию о ДТП."""

        return get_information(self, type_request='dtp')

    def get_eaisto_information(self):
        """Метод, получающий информацию по диагностическим картам и пробегу."""

        return get_information(self, type_request='eaisto')
