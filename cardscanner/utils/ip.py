#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: YJ
Email: yj1516268@outlook.com
Created Time: 2019-03-28 16:57:55


"""

import socket


def get_ip(connect_to: tuple):
    """get local IP.

    :connect_to: tuple: Echo address, used to get the local IP
    :returns: str: local IP

    """
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_obj.connect(connect_to)
    my_ip = socket_obj.getsockname()[0]

    return my_ip


if __name__ == "__main__":
    ip = get_ip(('8.8.8.8', 80))
    print(ip)
