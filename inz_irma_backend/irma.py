"""
A module to implement IRMA functionalities
"""
import json
from ctypes import *

IRMA_SIGNATURE_VERIFY = cdll.LoadLibrary("./go/irma_signature_verify.so")


def verify_signature(signature):
    """
    """
    IRMA_SIGNATURE_VERIFY.Verify.argtypes = [c_char_p]
    IRMA_SIGNATURE_VERIFY.Verify.restype = c_char_p

    result = IRMA_SIGNATURE_VERIFY.Verify(c_char_p(signature))

    result_json = result.decode('utf8')
    result_dic = json.loads(result_json)

    if 'error' in result_dic:
        raise Exception(result_dic.get('error'))

    return result_dic
