#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-19 22:38:59
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

from auto_flow_leaker.ec_coder import ECCoder
from auto_flow_leaker.comb_coder import Message
from auto_flow_leaker.comb_coder import CombCoder

M, R, I, K = 4, 2, 10, 3


ec_coder = ECCoder(M, R)

with open('data/eva_time_data_3.in', 'r') as fp:
    chunks = ec_coder.encode(fp.read())
    print chunks
    print [len(chunk) for chunk in chunks]
