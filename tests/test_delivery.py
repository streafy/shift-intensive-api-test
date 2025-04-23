import requests

from api import configuration, endpoints


class TestDelivery:
    def test_get_delivery_points(self):
        response = requests.get(configuration.BASE_URL + endpoints.GET_DELIVERY_POINTS)

        assert response.status_code == 200
        assert response.json()["success"] == True

    def test_get_package_types(self):
        response = requests.get(configuration.BASE_URL + endpoints.GET_DELIVERY_PACKAGE_TYPES)

        assert response.status_code == 200
        assert response.json()["success"] == True

    def test_calculate_delivery_options(self):
        payload = {
            "package": {
                "length": 1,
                "width": 1,
                "weight": 1,
                "height": 1
            },
            "senderPoint": {
                "latitude": 55.018803,
                "longitude": 82.933952
            },
            "receiverPoint": {
                "latitude": 55.751244,
                "longitude": 37.618423
            },
        }

        response = requests.post(configuration.BASE_URL + endpoints.CALCULATE_DELIVERY,
                                 json=payload)

        assert response.status_code == 201
        assert response.json()["success"] == True

    def test_create_delivery_order(self, point, address, person):
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

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["success"] == True
        assert response_data["order"]["_id"]

    def test_get_delivery_orders(self, auth_token):
        response = requests.get(configuration.BASE_URL + endpoints.GET_DELIVERY_ORDERS,
                                headers={"Authorization": 'Bearer ' + auth_token})

        assert response.status_code == 200
        assert response.json()["success"] == True

    def test_get_delivery_order(self, auth_token, order_id):
        assert order_id is not None, "Order was not created"

        response = requests.get(configuration.BASE_URL + endpoints.create_get_delivery_order_endpoint(order_id),
                                headers={"Authorization": 'Bearer ' + auth_token})

        assert response.status_code == 200

        response_data = response.json()

        assert response_data["success"] == True
        assert response_data["order"]["_id"] == order_id

    def test_cancel_delivery(self, auth_token, order_id):
        assert order_id is not None, "Order was not created"

        response = requests.put(configuration.BASE_URL + endpoints.CANCEL_DELIVERY,
                                headers={"Authorization": 'Bearer ' + auth_token},
                                json={"orderId": order_id})

        assert response.status_code == 200
        assert response.json()["success"] == True
