import pytest
import requests
from bs4 import BeautifulSoup

from api import configuration, endpoints


@pytest.fixture(scope="function")
def otp_code(phone_number):
    create_otp_code_response = requests.post(configuration.BASE_URL + endpoints.CREATE_OTP_CODE, json={
        "phone": phone_number
    })
    if create_otp_code_response.status_code != 201:
        return None

    otps_page_response = requests.get(configuration.BASE_URL + endpoints.GET_OTPS_PAGE)
    if otps_page_response.status_code != 200:
        return None

    soup = BeautifulSoup(otps_page_response.text, 'html.parser')

    table = soup.find('table')
    if not table:
        return None

    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        current_phone = cols[0].get_text(strip=True)

        if current_phone == phone_number:
            return cols[1].get_text(strip=True)

    return None


@pytest.fixture(scope="function")
def phone_number():
    return "89990009999"


@pytest.fixture(scope="function")
def auth_token(phone_number, otp_code):
    if otp_code is None:
        return None

    response = requests.post(configuration.BASE_URL + endpoints.SIGNIN, json={
        "phone": phone_number,
        "code": int(otp_code)
    })

    if response.status_code != 201:
        return None

    return response.json()["token"]


@pytest.fixture(scope="function")
def point():
    return {
        "id": "1",
        "name": "name",
        "latitude": 50,
        "longitude": 50
    }


@pytest.fixture(scope="function")
def address():
    return {
        "street": "street",
        "house": "house",
        "apartment": "apartment",
        "comment": "comment"
    }


@pytest.fixture(scope="function")
def person():
    return {
        "firstname": "firstname",
        "lastname": "lastname",
        "middlename": "middlename",
        "phone": "89990009999"
    }


@pytest.fixture(scope="function")
def order_id(point, address, person):
    response = requests.post(configuration.BASE_URL + endpoints.CREATE_DELIVERY_ORDER, json={
        "senderPoint": point,
        "senderAddress": address,
        "sender": person,
        "receiverPoint": point,
        "receiverAddress": address,
        "receiver": person,
        "payer": "SENDER",
        "option": {
            "id": "1",
            "price": 10000,
            "days": 2,
            "name": "name",
            "type": "DEFAULT"
        }
    })

    if response.status_code != 201:
        return None

    return response.json()["order"]["_id"]
