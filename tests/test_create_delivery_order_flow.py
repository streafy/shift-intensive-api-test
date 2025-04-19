import requests

from api import configuration, endpoints


def test_create_delivery_order_flow():
    points_response = requests.get(configuration.BASE_URL + endpoints.GET_DELIVERY_POINTS)
    assert points_response.status_code == 200

    points = points_response.json()["points"]
    assert len(points) >= 2

    package_types_response = requests.get(configuration.BASE_URL + endpoints.GET_DELIVERY_PACKAGE_TYPES)
    assert package_types_response.status_code == 200

    package_types = package_types_response.json()["packages"]
    assert len(package_types) >= 1

    delivery_options_response = requests.post(configuration.BASE_URL + endpoints.CALCULATE_DELIVERY, json={
        "senderPoint": points[0],
        "receiverPoint": points[1],
        "package": package_types[0],
    })
    assert delivery_options_response.status_code == 201

    delivery_options = delivery_options_response.json()["options"]
    assert len(delivery_options) >= 1

    create_delivery_order_response = requests.post(configuration.BASE_URL + endpoints.CREATE_DELIVERY_ORDER, json={
        "senderPoint": points[0],
        "senderAddress": {
            "street": "streetone",
            "house": "houseone",
            "apartment": "apartmentone"
        },
        "sender": {
            "firstname": "firstname",
            "lastname": "lastname",
            "middlename": "middlename",
            "phone": "89990009999"
        },
        "receiverPoint": points[1],
        "receiverAddress": {
            "street": "streettwo",
            "house": "housetwo",
            "apartment": "apartmenttwo"
        },
        "receiver": {
            "firstname": "namefirst",
            "lastname": "namelast",
            "middlename": "namemiddle",
            "phone": "89990009998"
        },
        "payer": "RECEIVER",
        "option": delivery_options[0]
    })
    assert create_delivery_order_response.status_code == 201
    assert create_delivery_order_response.json()["success"] == True