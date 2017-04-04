#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-04 21:21:21
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import sys

import bitstring

from auto_flow_leaker.ec_coder import ECCoder
from auto_flow_leaker.comb_coder import CombCoder

if len(sys.argv) != 5:
    print 'Error'
    sys.exit(1)

# M, R, I, K = 3, 1, 10, 2
M, R, I, K = [int(arg) for arg in sys.argv[1:5]]
DATA = 'a'  # data to be sent

# Init
ec_coder = ECCoder(M, R)
comb_coder = CombCoder(I, K)
capacity = comb_coder.capacity  # in bits

# EC coding
chunks = ec_coder.encode(DATA)

print 'Number of chunks:', len(chunks)
print 'Chunk size:', len(chunks[0])

all_chunk_data = b''.join(chunks)
all_chunk_bitstring = bitstring.BitStream(bytearray(all_chunk_data))

total_chunk_bits = len(all_chunk_bitstring)

print 'Total bits:', total_chunk_bits

message_integers = []
cur_offset = 0
while cur_offset < total_chunk_bits:
    cur_begin = cur_offset
    cur_end = cur_begin + capacity
    message_integers.append(
        all_chunk_bitstring[cur_begin:cur_end].uint)

    cur_offset += capacity

print 'Number of messages:', len(message_integers)

# Combination coding
arrangements = []
for message_integer in message_integers:
    arrangement = comb_coder.encode(message_integer)

    arrangements.append(arrangement)
