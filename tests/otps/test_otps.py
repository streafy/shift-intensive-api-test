import requests

from api import configuration, endpoints

class TestOtps:
    def test_create_otp_code(self, phone_number):
        response = requests.post(configuration.BASE_URL + endpoints.CREATE_OTP_CODE, json={
            "phone": phone_number
        })

        assert response.status_code == 201
        assert response.json()["success"] == True

    def test_opt_created(self, otp_code):
        assert otp_code is not None, "OTP was not created"