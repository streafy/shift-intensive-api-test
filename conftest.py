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
