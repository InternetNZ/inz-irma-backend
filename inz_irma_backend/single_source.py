"""
This is module is going to be used to call SingleSource APIs
"""

import os
from urllib.parse import urljoin

import requests

SINGLE_SOURCE_API_KEY = os.environ.get('SINGLE_SOURCE_API_KEY')
SINGLE_SOURCE_URL = os.environ.get('SINGLE_SOURCE_URL')


def _send_request(endpoint, method='POST', payload=None, custom_headers=None):
    """
    Sends the request to SingleSource.

    :param endpoint: API endpoint
    :param payload: API payload in JSON or DICT
    :param method: HTTP method
    :param custom_headers: Custom headers. Replaces default headers.

    :return: response object
    """
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': SINGLE_SOURCE_API_KEY,
    }
    if custom_headers:
        headers.update(headers)

    response = requests.request(
        method,
        urljoin(SINGLE_SOURCE_URL, endpoint),
        headers=headers,
        json=payload,
    )

    return response


def call_driver_license_verification(document_image, country_code):
    """
    Calls /drivers-licences endpoint from SingleSource to verify given driver licence and returns the response.

    :param document_image: Image in base64-encoded format.
    :param country_code: The country code simplified to three letters using the ISO 3166 alpha-3 format.

    :return: response object
    """

    payload = {
        'country': country_code,
        'documentImage': document_image,
    }

    response = _send_request('drivers-licences', payload=payload)

    return response


def call_passport_verification(document_image, country_code):
    """
    Calls /passports endpoint from SingleSource to verify given passport and returns the response.

    :param document_image: Image in base64-encoded format.
    :param country_code: The country code simplified to three letters using the ISO 3166 alpha-3 format.

    :return: response object
    """

    payload = {
        'country': country_code,
        'documentImage': document_image,
    }

    response = _send_request('passports', payload=payload)

    return response


def call_doughnut_verification(doughnut):
    """
    Calls /doughnut from SingleSource to verify given doughnut and returns the response.

    :param doughnut: A doughnut which is previously received from another api.

    :return: string
    """

    return _send_request(
        'doughnuts/' + doughnut,
        method='GET'
    )
