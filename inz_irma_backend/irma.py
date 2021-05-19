"""
A module to implement IRMA functionalities
"""
import json
import os
from ctypes import cdll, c_char_p

GO_PATH = os.path.join(os.getcwd(), 'go/irma_signature_verify.so')
IRMA_SIGNATURE_VERIFY = cdll.LoadLibrary(GO_PATH)


def verify_signature(signature):
    """
    Verify given signature by calling Verify function from irmago

    :param signature: IRMA signature payload
    :return: dict
    """
    IRMA_SIGNATURE_VERIFY.Verify.argtypes = [c_char_p]
    IRMA_SIGNATURE_VERIFY.Verify.restype = c_char_p

    result = IRMA_SIGNATURE_VERIFY.Verify(c_char_p(signature))

    result_json = result.decode('utf8')
    result_dic = json.loads(result_json)

    if 'error' in result_dic:
        raise Exception(result_dic.get('error'))

    return result_dic
