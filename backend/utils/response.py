import json
from flask import Response

def create_response(status_code, message, data=None):
    response = {
        "status": status_code,
        "message": message,
        "data": data
    }

    return Response(json.dumps(response), status=status_code, mimetype='application/json')
