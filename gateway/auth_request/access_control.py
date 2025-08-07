import os
import requests as req
from requests.auth import HTTPBasicAuth


def access_control(request):
    auth = request.authorization
    if not auth:
        return None, ('invalid credentials', 401)

    response = req.post(
        os.getenv('AUTH_SERVICE_URL') + '/login', auth=HTTPBasicAuth(
            auth.username, auth.password))
    print(response)
    if response.status_code != 200:
        return None, response.status_code

    token = response.json().get('token')
    return token, 200
