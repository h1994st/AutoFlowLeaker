#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-19 22:38:59
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os

import bitstring

import Archiver
from auto_flow_leaker.ec_coder import ECCoder
from auto_flow_leaker.comb_coder import Message
from auto_flow_leaker.comb_coder import CombCoder

M, R, I, K = 4, 2, 5, 2

# Init
ec_coder = ECCoder(M, R)
comb_coder = CombCoder(I, K)
capacity = comb_coder.capacity  # in bits

# Compress
input_files = ['data/eva_time_data_3.in']
output_file = 'data/eva_time_data_3.in.7z'
Archiver.compress(input_files, output_file)

# EC coding
with open(output_file, 'r') as fp:
    print 'File size:', os.stat(fp.name).st_size
    chunks = ec_coder.encode(fp.read())

# Fill messages
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

    chunk_bit_offset += msg_size

    messages.append(message)

print 'Number of messages:', len(messages)

# Combination coding
arrangements = []
for message in messages:
    msg_byte_data = message.serialize()
    msg_bin_data = bitstring.BitStream(bytearray(msg_byte_data))
    arrangement = comb_coder.encode(msg_bin_data.int)

    arrangements.append(arrangement)
