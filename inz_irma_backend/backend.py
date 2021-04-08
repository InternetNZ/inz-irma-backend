"""
The implementation of InternetNZ IRMA backend
"""
import os
import traceback

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager, login_required, UserMixin
from werkzeug.exceptions import HTTPException

from inz_irma_backend import single_source, logger

app = Flask(__name__)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

ALLOWED_ORIGIN = os.environ.get('ALLOWED_ORIGIN')


class InternalServerError(Exception):
    """
    Internal server error class.
    """

    def __init__(self, description=None, code=None):
        Exception.__init__(self)
        self.description = description if description else \
            "Something bad happened on the server! Check the server logs for more details!"
        self.code = code if code else 500
        self.name = "Internal Server Error"


@app.errorhandler(401)
@app.errorhandler(InternalServerError)
@app.errorhandler(HTTPException)
def error_handler(error):
    """
    Handles registered errors by returning code and description in
    JSON format
    """
    response = jsonify({
        "code": error.code,
        "name": error.name,
        "description": error.description,
    })
    return response, error.code


@app.route('/single-source/drivers-licences', methods=['POST'])
@login_required
def verify_driver_license():
    """
    A wrapper on /drivers-licences SingleSource API.
    """

    try:
        response = single_source.call_driver_license_verification(
            request.json['document_image'],
            request.json['country_code']
        )

        return response.json(), response.status_code
    except Exception as exc:
        logger.error('Internal error: %s - %s', str(exc),
                     traceback.format_exc())
        raise InternalServerError() from exc


@app.route('/single-source/passports', methods=['POST'])
@login_required
def verify_passport():
    """
    A wrapper on /passports SingleSource API.
    """

    try:
        response = single_source.call_passport_verification(
            request.json['document_image'],
            request.json['country_code']
        )

        return response.json(), response.status_code
    except Exception as exc:
        logger.error('Internal error: %s - %s', str(exc),
                     traceback.format_exc())
        raise InternalServerError() from exc


@app.route('/single-source/doughnuts/<doughnut>')
@login_required
def verify_doughnut(doughnut):
    """
    A wrapper on /doughnuts SingleSource API.
    """

    try:
        response = single_source.call_doughnut_verification(doughnut)

        return response.json(), response.status_code
    except Exception as exc:
        logger.error('Internal error: %s - %s', str(exc),
                     traceback.format_exc())
        raise InternalServerError() from exc


@login_manager.request_loader
def check_origin(api_request):
    """
    Checks origin header to be matched by ALLOWED_ORIGIN.
    """
    logger.debug('Authorize api call by checking api call origin')

    origin = api_request.headers.get('Origin')

    logger.debug('Origin: %s', origin)

    if origin != ALLOWED_ORIGIN:
        return None

    return ApiUser(origin)


class ApiUser(UserMixin):
    """
    Flask login user class
    """

    def __init__(self, origin):
        self.id = origin  # pylint: disable=invalid-name
