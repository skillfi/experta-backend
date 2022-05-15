import os

from flask import jsonify, make_response
from bson.objectid import ObjectId

from core.config import app, db


# wrap response in json to return in API
def wrap_response(data, errors=None, auth='Authorized', access='Permitted'):
    body = data
    if isinstance(body, dict) and body.get('errors') is not None:
        if auth == 'Unauthorized':
            return make_response(jsonify({'status': 'Failed',
                                          'reason': body['errors']['message']}), 401)
        elif access == 'Forbidden':
            return make_response(jsonify({'status': 'Failed',
                                          'reason': body['errors']['message']}), 403)
        return make_response(jsonify({'status': 'Failed',
                                      'reason': body['errors']['message']}), 400)
    else:
        response = ''
        # check if body is dictionary and contains 'message' key
        if isinstance(body, dict) and body.get('message'):
            response = body.get('message')
            body = []
        return make_response(jsonify({'status': 'OK',
                                      'data': body,
                                      'response': response}), 200)
