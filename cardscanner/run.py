#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: YJ
Email: yj1516268@outlook.com
Created Time: 2019-03-27 15:00:35

use <evdev> package
"""

import json
import logging
import os
import re
import time
import threading

import requests
import toml
from evdev import InputDevice
from devicer import findDevice, kvc2kv

from utils import setLog, getIP, createData


RUN_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

LOGS_DIR = '{}{}{}'.format(RUN_FILE_PATH, os.sep, 'logs')
if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)

CONFILE = '{}{}{}'.format(RUN_FILE_PATH, os.sep, 'conf/conf.toml')
CONF = toml.load(CONFILE)

setLog(CONF['log'])


class CardScanner:

    """Card scan monitor"""

    def __init__(self):
        """init """
        # run
        self.keyword = keyword = CONF['device'].get('keyword', 'usb')
        self.device = findDevice(keyword)
        self.cardnumber = ''

        # request
        getip_ip = CONF['url'].get('getip_ip', '127.0.0.1')
        getip_port = CONF['url'].get('getip_port', 80)
        self.my_ip = getIP((getip_ip, getip_port))
        self.url = CONF['url'].get('url', None)

        self.log = logging.getLogger('main')

        # heartbeat
        self.interval = CONF['interval'].get('heartbeat', 30)

    def match(self):
        """验证刷卡所得数据是否有小数点
        :returns: bool

        """
        pattern = r'(\d+)\.(\d+)'
        compile_obj = re.compile(pattern)
        match_obj = compile_obj.search(self.cardnumber)

        return bool(match_obj is not None)

    def request(self):
        """将卡号作为参数发送请求.

        """
        data = createData(REQUEST_IP=self.my_ip, CARDNUMBER=self.cardnumber)

        if len(self.cardnumber) == 10:
            self.log.debug('Requesting: <{}>'.format(self.url))
            try:
                resp = requests.post(self.url, data=json.dumps(data))
            except Exception:
                self.log.warning('Request failed: <{}>!'.format(self.url))
            else:
                self.log.debug(resp.text)
        elif self.match():
            self.log.warning('Card number format error!')
        else:
            pass

    def run(self):
        """run.

        """
        if not self.device:
            self.log.error("Can't find any {} devices!".format(self.keyword))
        else:
            dev = InputDevice(self.device)
            for event in dev.read_loop():
                if event.value == 1 and event.code != 0:
                    in_value = kvc2kv(event.code)
                    if in_value == 'enter':
                        self.log.debug(self.cardnumber)
                        self.request()
                        self.cardnumber = ''
                    elif in_value == 'space':
                        pass
                    else:
                        self.cardnumber = self.cardnumber + in_value
                else:
                    pass

    def heartbeat(self):
        """Heartbeat

        """
        while True:
            time.sleep(self.interval)
            self.log.info('Heartbeat')


def main():
    """Main Function

    """
    print('Starting Card Scanner daemon...')

    card_scanner = CardScanner()

    thead_scanner = threading.Thread(
        target=card_scanner.run, name='Monitor'
    )
    thead_heartbeat = threading.Thread(
        target=card_scanner.heartbeat, name='Heartbeat'
    )

    thead_scanner.daemon = True
    thead_heartbeat.daemon = True

    thead_scanner.start()
    thead_heartbeat.start()

    thead_scanner.join()
    thead_heartbeat.join()


if __name__ == "__main__":
    main()
