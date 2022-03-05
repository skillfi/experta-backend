import os

from flask import jsonify, make_response

from core.config import app, db


def wrap_response(data, errors=None, auth='Authorized', access='Permitted'):
    body = data
    if not errors:
        response = ''
        # check if body is dictionary and contains 'message' key
        if isinstance(body, dict) and body.get('message'):
            response = body.get('message')
        if '_id' in body:
            body['_id'] = str(body['_id'])
        if 'electionId' in body:
            body['electionId'] = str(body['electionId'])
        return make_response(jsonify({'status': 'OK',
                                      'data': body,
                                      'response': response}), 200)
    else:
        if auth == 'Unauthorized':
            return make_response(jsonify({'status': 'Failed',
                                          'reason': body['errors']['message']}), 401)
        elif access == 'Forbidden':
            return make_response(jsonify({'status': 'Failed',
                                          'reason': body['errors']['message']}), 403)
        return make_response(jsonify({'status': 'Failed',
                                      'reason': body['errors']['message']}), 400)
