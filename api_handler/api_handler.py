import json

from decouple import config
import requests


class IMEICheckBot:
    """
    Класс для проверки IMEI устройств с помощью сервиса imeicheck.net.

    Attributes:
        token_api_imei (str): Токен API для сервиса imeicheck.net.
        imei (str): IMEI устройства, который нужно проверить.
        url (str): URL для отправки запроса на сервер imeicheck.net.
        headers (dict): Заголовки HTTP-запроса.
        body (str): Тело HTTP-запроса в формате JSON.

    Methods:
        info(): Метод для получения информации о устройстве по IMEI.

    """
    def __init__(self, imei):
        """
            Инициализация класса с указанием токена API и IMEI устройства.

            Args:
                imei (str): IMEI устройства, который нужно проверить.

            Raises:
                ValueError: Если IMEI не является строкой или его длина меньше 15 символов.

        """
        self.token_api_imei = config('TOKEN_API_IMEI')
        self.imei = imei
        self.url = 'https://api.imeicheck.net/v1/checks'
        self.headers = {
            'Authorization': 'Bearer ' + self.token_api_imei,
            'Content-Type': 'application/json'
        }

        self.body = json.dumps({
            "deviceId": "356735111052198",
            "serviceId": 12
        })

    def info(self):
        """
            Метод для получения информации об устройстве по IMEI.

            Returns:
                str: Информация об устройстве в формате строки.

            Raises:
                requests.exceptions. RequestException: Если произошла ошибка при отправке запроса на
                сервер imeicheck.net.

        """
        try:

            data_imei = requests.post(self.url, headers=self.headers, data=self.body)

        except requests.exceptions.RequestException as req_err:
            print(f"Request error: {req_err}")
            return {"status_code": None, "error": str(req_err)}
        properties = data_imei.json().get("properties", {})
        if properties.get('status') == 'unsuccessful':
            text = 'Нет информации'
            return text
        text = (
            f"Device Info:\n"
            f"Model: {properties.get('deviceName', '-')}\n"
            f"Description: {properties.get('modelDesc', '-')}\n"
            f"IMEI 1: {properties.get('imei', '-')}\n"
            f"IMEI 2: {properties.get('imei2', '-')}\n"
            f"Serial: {properties.get('meid', '-')}\n"
            f"Purchase Country: {properties.get('purchaseCountry', '-')}\n"
            f"SIM Lock: {'Locked' if properties.get('simLock') else 'Unlocked'}\n"
            f"Replacement: {'Yes' if properties.get('replacement') else 'No'}\n"
            f"Lost Mode: {'Lost' if properties.get('lostMode') else 'Not Lost'}\n"
            f"Repair Coverage: {'Covered' if properties.get('repairCoverage') else 'Not Covered'}\n"
        )

        return text
