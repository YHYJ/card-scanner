#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: YJ
Email: yj1516268@outlook.com
Created Time: 2019-03-28 17:10:24


"""


def create_data(method='get_cardnumber', **kwargs):
    """Create request parameters.

    :method: str
    :**kwargs: dict
    :returns: dict: request parameters

    """
    data = {
        'method': method,
        'params': {
            'result': kwargs
        },
        'jsonrpc': '2.0',
        'id': '1',
    }

    return data


if __name__ == "__main__":
    data = create_data(REQUEST_IP='127.0.0.1', CARDNUMBER='1234567890')
    print(data)
