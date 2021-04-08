"""
The implementation of InternetNZ IRMA backend
"""
import traceback

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from inz_irma_backend import single_source, logger

app = Flask(__name__)
CORS(app)


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
    return response


@app.route('/single-source/drivers-licences', methods=['POST'])
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
