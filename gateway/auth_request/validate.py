import os
import requests as req  # type: ignore


def validate(request):
    token = request.headers.get('Authorization')
    if not token:
        return (401, 'Unauthorized')

    response = req.post(
        os.getenv('AUTH_SERVICE_URL') + '/validate', headers={
            'Authorization': token})

    if response.status_code != 200:
        return 'Invalid token', response.status_code

    return response.text, 200
