import requests
from api import configuration, endpoints


def test_get_delivery_points_success_response():
    response = requests.get(configuration.BASE_URL + endpoints.GET_DELIVERY_POINTS)

    assert response.status_code == 200
    assert response.json()["success"] == True