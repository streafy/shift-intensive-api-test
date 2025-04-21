GET_OTPS_PAGE = "/otps"

CREATE_OTP_CODE = "/auth/otp"

SIGNIN = "/users/signin"
UPDATE_PROFILE = "/users/profile"
GET_USER_SESSION = "/users/session"

GET_DELIVERY_POINTS = "/delivery/points"
GET_DELIVERY_PACKAGE_TYPES = "/delivery/package/types"
CALCULATE_DELIVERY = "/delivery/calc"
CREATE_DELIVERY_ORDER = "/delivery/order"
GET_DELIVERY_ORDERS = "/delivery/orders"
CANCEL_DELIVERY = "/delivery/orders/cancel"


def create_get_delivery_order_endpoint(order_id: str):
    return f"{GET_DELIVERY_ORDERS}/{order_id}"
