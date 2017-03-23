#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-12 23:14:40
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

from pushbullet import Pushbullet

import Config

pb = Pushbullet(Config.Pushbullet('api_key'))

DISABLE = (Config.Pushbullet('disable') == 'True')


class VoidDevice(object):
    def __init__(self):
        super(VoidDevice, self).__init__()

    def push_note(self, title, body):
        print 'Push note:'
        print '  title:', title
        print '  body:', body


void_device = VoidDevice()


def get_devices():
    if DISABLE:
        return [void_device]
    return pb.devices


def get_device(name):
    if DISABLE:
        return void_device
    return pb.get_device(name)


del Config
del Pushbullet


def main():
    print get_devices()


if __name__ == '__main__':
    main()
