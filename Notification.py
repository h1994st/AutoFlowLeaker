#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-12 23:14:40
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

from pushbullet import Pushbullet

import Config

pb = Pushbullet(Config.Pushbullet('api_key'))


def get_devices():
    return pb.devices


def get_device(name):
    return pb.get_device(name)


del Config
del Pushbullet


def main():
    print get_devices()


if __name__ == '__main__':
    main()
