#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-19 22:38:59
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import bitstring

from auto_flow_leaker.ec_coder import ECCoder
from auto_flow_leaker.comb_coder import Message
from auto_flow_leaker.comb_coder import CombCoder

M, R, I, K = 4, 2, 10, 3

ec_coder = ECCoder(M, R)
comb_coder = CombCoder(I, K)
capacity = comb_coder.capacity  # in bits

with open('data/eva_time_data_3.in', 'r') as fp:
    chunks = ec_coder.encode(fp.read())

total_chunk_len = len(chunks[0]) * len(chunks)  # in bytes
all_chunk_data = b''.join(chunks)

all_chunk_bitstring = bitstring.BitStream(bytearray(all_chunk_data))

messages = []
total_chunk_bits = len(all_chunk_bitstring)
chunk_bit_offset = 0
msg_size = capacity - 64  # in bits

while chunk_bit_offset < total_chunk_bits:
    begin = chunk_bit_offset
    end = chunk_bit_offset + msg_size
    message = Message(
        M, R,
        total_chunk_bits, chunk_bit_offset,
        data=all_chunk_bitstring[begin:end].tobytes())

    print begin, end
    print all_chunk_bitstring[begin:end]
    print all_chunk_bitstring[begin:end].tobytes()
    print message
    print ''

    chunk_bit_offset += msg_size

    messages.append(message)
