import requests
from api import configuration, endpoints


def test_get_package_types_success_response():
    response = requests.get(configuration.BASE_URL + endpoints.GET_DELIVERY_PACKAGE_TYPES)

    assert response.status_code == 200
    assert response.json()["success"] == True