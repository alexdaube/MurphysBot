from flask import request, jsonify, json


class FlaskUtilsWrapper(object):
    def get_request_json(self):
        data = request.get_json()
        if not isinstance(data, dict):
            data = json.loads(data)
        return data

    def to_json(self, dictionary):
        return jsonify(dictionary)

    def remote_address(self):
        headers_list = request.headers.getlist("X-Forwarded-For")
        return headers_list[0] if headers_list else request.remote_addr

    def get_shutdown_function(self):
        return request.environ.get('werkzeug.server.shutdown')
