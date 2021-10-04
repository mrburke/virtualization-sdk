#
# Copyright (c) 2021 by Delphix. All rights reserved.
#


"""
Utility functions to convert between unicode and bytes.
"""

import six


def to_bytes(string, encoding=None):
    """
    Converts the given object to binary object, bytes (Py3) or str (Py2).

    :param string: The string like object to convert to bytes
    :type string: ``object``
    :param encoding: The encoding to encode the string with.
    :type encoding: ``str``
    :returns: The decoded string.
    :rtype: ``six.binary_type``
    """
    if string is None:
        return

    if not encoding:
        encoding = "utf-8"

    if isinstance(string, dict):
        for k, v in string.items():
            string[k] = to_bytes(v, encoding=encoding)
        return string

    if isinstance(string, list):
        return [to_bytes(i, encoding=encoding) for i in string]

    if isinstance(string, set):
        return {to_bytes(i, encoding=encoding) for i in string}

    _str = str if six.PY3 else unicode
    if isinstance(string, _str):
        return _to_bytes(string, encoding)

    return string


def _to_bytes(string, encoding):
    if six.PY3:
        if isinstance(string, str):
            return string.encode(encoding)
        else:
            return bytes(string)
    else:
        if isinstance(string, unicode):
            return string.encode(encoding)
        else:
            return str(string)


def to_str(b, encodings=None):
    """
    Converts the given object to a text object, unicode (Py2) or str (Py3).

    :param b: The object to convert
    :type b: ``object``
    :param encodings: A list of encodings to decode with, they will each
        be tried in order to determine the encoding of the string.
    :type encodings:  ``None`` or ``List`` of ``str``
    :returns: Returns the decoded string.
    :rtype: ``six.text_type``
    """
    if b is None:
        return

    # If the encoding is not set or if the first value in the lis is
    # None then we want to use the standard, default encodings.
    if not encodings or not encodings[0]:
        encodings = ("utf-8", "utf-16", "latin-1", "ascii")

    if isinstance(b, dict):
        for k, v in b.items():
            b[k] = to_str(v, encodings=encodings)
        return b

    if isinstance(b, list):
        return [to_str(i, encodings=encodings) for i in b]

    if isinstance(b, set):
        return {to_str(i, encodings=encodings) for i in b}

    _bytes = bytes if six.PY3 else str
    if isinstance(b, _bytes):
        return _to_str(b, encodings=encodings)
    return b


def _to_str(b, encodings):
    if six.PY3:
        if isinstance(b, bytes):
            for encoding in encodings:
                try:
                    return str(b, encoding)
                except UnicodeDecodeError:
                    pass
            raise UnicodeError(
                "Could not decode value with encodings {}".format(encodings)
            )
        else:
            return b
    else:
        if isinstance(b, str):
            for encoding in encodings:
                try:
                    return b.decode(encoding)
                except UnicodeDecodeError:
                    pass
            raise UnicodeError(
                "Could not decode value with encodings {}".format(encodings)
            )
        return b


def response_to_str(response):
    """
    The response_to_str function ensures all relevant properties of the given
    response are unicode (py2) / str (py3). Should be called on a response as
    soon as it is received.

    Args:
        response (RunPowerShellResponse or RunBashResponse or RunExpectResponse):
        Response received by run_bash or run_powershell or run_expect
    """
    if response.HasField("return_value"):
        if hasattr(response.return_value, "stdout"):
            response.return_value.stdout = to_str(response.return_value.stdout)
        if hasattr(response.return_value, "stderr"):
            response.return_value.stderr = to_str(response.return_value.stderr)
