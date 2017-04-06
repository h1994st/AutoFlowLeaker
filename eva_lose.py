#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-04 21:21:21
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import sys
import math
import random

import bitstring

from auto_flow_leaker.ec_coder import ECCoder
from auto_flow_leaker.comb_coder import CombCoder

if len(sys.argv) != 6:
    print 'Error'
    sys.exit(1)

# M, R, I, K = 3, 1, 10, 2
M, R, I, K = [int(arg) for arg in sys.argv[1:5]]
DATA = 'a'  # data to be sent
LOSS_PROB = float(sys.argv[5])

# Init
ec_coder = ECCoder(M, R)
comb_coder = CombCoder(I, K)
capacity = comb_coder.capacity  # in bits

# EC coding
chunks = ec_coder.encode(DATA)
num_chunks = len(chunks)
size_of_chunk = len(chunks[0])

print 'Number of chunks:', num_chunks
print 'Chunk size:', size_of_chunk, 'bytes'

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

num_messages = len(message_integers)
print 'Number of messages:', num_messages

# Combination coding
arrangements = []
for message_integer in message_integers:
    arrangement = comb_coder.encode(message_integer)

    arrangements.append(arrangement)

# Random loss
arrangement_indexs = range(num_messages)
num_loss = int(math.floor(num_messages * LOSS_PROB))
print 'Number of losed message:', num_loss
while num_loss > 0:
    arrangement_indexs.remove(random.choice(arrangement_indexs))

    num_loss -= 1

# Recovered bitstring, including broken part (set as 0, if broken)
recovered_bitstring = bitstring.BitStream(total_chunk_bits)
for index in arrangement_indexs:
    arrangement = arrangements[index]
    message_integer = comb_coder.decode(*arrangement)

    # [begin, end)
    begin = index * capacity
    end = min(begin + capacity, total_chunk_bits)

    recovered_bitstring[begin:end] = bitstring.BitStream(
        'uint:%d=%d' % (end - begin, message_integer))

# Check broken indexs
broken_chunk_indexs = set()
for i in xrange(num_messages):
    if i in arrangement_indexs:
        continue

    # [broken_begin, broken_end)
    broken_begin = i * capacity
    broken_end = min(broken_begin + capacity, total_chunk_bits)

    broken_chunk_indexs.add(broken_begin / size_of_chunk)
    broken_chunk_indexs.add(broken_end / size_of_chunk)

print 'Broken chunks indexs:'
print broken_chunk_indexs

recovered_chunk_data = recovered_bitstring.bytes
recovered_chunks = []
for i in xrange(num_chunks):
    # Skip broken chunks
    if i in broken_chunk_indexs:
        continue

    begin = i * size_of_chunk
    end = (i + 1) * size_of_chunk
    recovered_chunks.append(recovered_chunk_data[begin:end])

print 'Number of recovered chunks:', len(recovered_chunks)
print 'Recovered chunk size:', len(recovered_chunks[0])


recovered_data = ec_coder.decode(recovered_chunks)
print recovered_data
print recovered_data == DATA
