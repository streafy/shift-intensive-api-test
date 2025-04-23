import requests

from api import configuration, endpoints


class TestUsers:
    def test_auth(self, phone_number, otp_code):
        assert otp_code is not None, "OTP was not created"

        response = requests.post(configuration.BASE_URL + endpoints.SIGNIN, json={
            "phone": phone_number,
            "code": int(otp_code)
        })

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["success"] == True
        assert response_data["user"]["phone"] == phone_number
        assert response_data["token"]

    def test_update_user_profile(self, auth_token, phone_number):
        assert auth_token is not None, "Token was not created"

        response = requests.patch(configuration.BASE_URL + endpoints.UPDATE_PROFILE,
                                  headers={"Authorization": 'Bearer ' + auth_token},
                                  json={
                                      "profile": {
                                          "firstname": "firstname",
                                          "middlename": "middlename",
                                          "lastname": "lastname",
                                          "email": "email@gmail.com",
                                          "city": "city"
                                      },
                                      "phone": phone_number
                                  })

        assert response.status_code == 200, response.text

    def test_get_user_session(self, auth_token):
        assert auth_token is not None, "Token was not created"

        response = requests.get(configuration.BASE_URL + endpoints.GET_USER_SESSION,
                                headers={"Authorization": 'Bearer ' + auth_token})

        assert response.status_code == 200
        assert response.json()["success"] == True
