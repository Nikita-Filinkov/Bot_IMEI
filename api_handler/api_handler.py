import json

from decouple import config
import requests


class IMEICheckBot:
    def __init__(self, imei):
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
        try:

            data_imei = requests.post(self.url, headers=self.headers, data=self.body)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error: {http_err}")
            return {"status_code": data_imei.status_code, "error": str(http_err)}

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



