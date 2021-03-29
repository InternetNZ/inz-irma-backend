"""
The implementation of InternetNZ IRMA backend
"""

from flask import Flask
from flask import request

from inz_irma_backend import single_source, logger

app = Flask(__name__)


@app.route('/single-source/driver-licences', methods=['POST'])
def verify_driver_license():
    """
    A wrapper on /drivers-licences SingleSource API.
    """

    logger.debug('log to main logger!')

    response = single_source.call_driver_license_verification(
        request.json['document_image'],
        request.json['country_code']
    )

    return response.json(), response.status_code


@app.route('/single-source/passports', methods=['POST'])
def verify_passport():
    """
    A wrapper on /passports SingleSource API.
    """

    response = single_source.call_passport_verification(
        request.json['document_image'],
        request.json['country_code']
    )

    return response.json(), response.status_code


@app.route('/single-source/doughnuts/<doughnut>')
def verify_doughnut(doughnut):
    """
    A wrapper on /doughnuts SingleSource API.
    """

    response = single_source.call_doughnut_verification(doughnut)

    return response.json(), response.status_code
