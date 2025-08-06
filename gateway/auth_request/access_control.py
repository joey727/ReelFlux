import os
import requests as req  # type: ignore


def access_control(request):
    auth = request.authorization
    if not auth:
        return None, (401, 'Unauthorized')

    response = req.post(
        os.getenv('AUTH_SERVICE_URL') + '/login', json={
            'username': auth.username,
            'password': auth.password}),
    if response.status_code != 200:
        return None, (401, 'Unauthorized')

    return response.text, (200, 'OK')
