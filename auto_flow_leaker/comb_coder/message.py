#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-04 17:37:49
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import struct
import binascii

# Struct for packing and unpacking
_STRUCT_BBHHH = struct.Struct('>BBHHH')


class Message(object):
    '''
    Basic data unit of CombCoder layer.

    6-byte header + message
    '''
    def __init__(self, m, r,
                 total_chunk_len, chunk_offset, data=b''):
        if not (m >= 0 and m <= 255):
            raise ValueError(
                'm must be in the range of [0, 255].')
        if not (r >= 0 and r <= 255):
            raise ValueError(
                'r must be in the range of [0, 255].')

        if not (total_chunk_len >= 0 and total_chunk_len <= 65535):
            raise ValueError(
                'Total Length must be in the range of [0, 65535].')
        if not (chunk_offset >= 0 and chunk_offset <= 65535):
            raise ValueError(
                'Message Offset must be in the range of [0, 65535].')

        if not (chunk_offset >= 0 and chunk_offset <= total_chunk_len):
            raise ValueError(
                'Chunk Offset must be smaller than Total Chunk Length.')

        super(Message, self).__init__()

        self.m = m  # 8-bit number (0~255)
        self.r = r  # 8-bit number (0~255)
        self.total_chunk_len = total_chunk_len  # 16-bit number (0~65535)
        self.chunk_offset = chunk_offset  # 16-bit number (0~65535)

        self.msg_size = len(data)  # 16-bit number (0~65535)
        self.data = data

    def __repr__(self):
        msg = binascii.hexlify(self.data).decode('ascii')
        if len(msg) > 16:
            msg = msg[:16] + '...'

        return (
            'Message(m={!r}, r={!r}, msg_size={!r}, '
            'total_chunk_len={!r}, chunk_offset={!r}, payload={!r})'
        ).format(
            self.m, self.r, self.msg_size,
            self.total_chunk_len, self.chunk_offset, msg)

    def serialize(self):
        '''
        Converts a chunk into a bytestring, representing the serialized form of
        the chunk.
        '''
        msg = self.data
        self.msg_size = len(msg)

        header = _STRUCT_BBHHH.pack(
            self.m & 0xFF,
            self.r & 0xFF,
            self.msg_size & 0xFFFF,
            self.total_chunk_len & 0xFFFF,
            self.chunk_offset & 0xFFFF)

        return header + msg

    @staticmethod
    def parse_message_header(header):
        '''
        Takes a 6-byte message header and returns a tuple of the appropriate
        Chunk object and the length that needs to be read from the lower layer.
        '''
        try:
            fields = _STRUCT_BBHHH.unpack(header)
        except struct.error:
            raise Exception('Invalid message header')

        m = fields[0]
        r = fields[1]
        msg_size = fields[2]
        total_chunk_len = fields[3]
        chunk_offset = fields[4]

        return (Message(m, r, total_chunk_len, chunk_offset), msg_size)

    def parse_message(self, data):
        '''
        Given the data of the message, parses it into message data.

        :param data: A memoryview object containing the message data. Must not
                     contain *more* data than the length returned by
                     :meth:`parse_message_header
                     <auto_flow_leaker.comb_coder.message.Message.parse_message_header>`.
        '''
        if not (self.chunk_offset + len(data) <= self.total_chunk_len):
            raise ValueError(
                'Current message payload is too large.')
        self.data = data.tobytes()  # memoryview
        self.msg_size = len(data)


def test_message():
    message, msg_size = Message.parse_message_header(
        b'\x04\x02\x02\x00\x03\x00\x01\x00')
    print message, msg_size
    message.parse_message(memoryview('A' * msg_size))

    print message

    print message.serialize()
    print message.serialize()[:8]
    print message.serialize()[:8] == b'\x04\x02\x02\x00\x03\x00\x01\x00'


if __name__ == '__main__':
    test_message()
