#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-19 22:38:59
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import sys

import bitstring

import Archiver
from auto_flow_leaker.ec_coder import ECCoder
from auto_flow_leaker.comb_coder import Message
from auto_flow_leaker.comb_coder import CombCoder

if len(sys.argv) != 6:
    print 'Error'
    sys.exit(1)

# M, R, I, K = 3, 1, 10, 2
M, R, I, K = [int(arg) for arg in sys.argv[1:5]]

# Init
ec_coder = ECCoder(M, R)
comb_coder = CombCoder(I, K)
capacity = comb_coder.capacity  # in bits

input_file = sys.argv[5]
if not os.path.exists(input_file):
    print 'File does not exist:', input_file
    sys.exit(1)

output_dir = 'data/chunks'
if os.path.exists(output_dir):
    os.rmdir(output_dir)
os.makedirs(output_dir)

# EC coding
with open(input_file, 'r') as fp:
    print 'File size:', os.stat(fp.name).st_size
    ec_coder.encode_file(fp, output_dir)

# Compress
input_files = [os.path.join(
    output_dir, chunk_filename) for chunk_filename in os.listdir(output_dir)]
output_file = '%s.7z' % input_file
Archiver.compress(input_files, output_file)

# Delete chunks
os.rmdir(output_dir)

# Fill messages
# print 'Number of chunks:', len(chunks)
# print 'Sizes of chunks:', [len(chunk) for chunk in chunks]

# total_chunk_len = len(chunks[0]) * len(chunks)  # in bytes
# all_chunk_data = b''.join(chunks)
with open(output_file, 'r') as fp:
    all_chunk_bitstring = bitstring.BitStream(fp)

messages = []
total_chunk_bits = len(all_chunk_bitstring)
chunk_bit_offset = 0
msg_size = capacity - 64  # in bits

print 'Total bits:', total_chunk_bits

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
