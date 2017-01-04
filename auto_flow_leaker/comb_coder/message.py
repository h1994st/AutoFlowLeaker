#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-04 17:37:49
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import struct
import binascii

# Struct for packing and unpacking
_STRUCT_HHH = struct.Struct('>HHH')


class Message(object):
    '''
    Basic data unit of CombCoder layer.

    6-byte header + message
    '''
    def __init__(self, total_len, msg_offset, data=b''):
        if not (total_len >= 0 and total_len <= 65535):
            raise ValueError(
                'Total Length must be in the range of [0, 65535].')
        if not (msg_offset >= 0 and msg_offset <= 65535):
            raise ValueError(
                'Message Offset must be in the range of [0, 65535].')
        if not (msg_offset <= total_len):
            raise ValueError(
                'Message Offset must be smaller than Total Length.')

        super(Message, self).__init__()

        self.total_len = total_len  # 16-bit number (0~65535)
        self.msg_offset = msg_offset  # 16-bit number (0~65535)
        self.data = data

        self.msg_len = 0  # 16-bit number (0~65535)

    def __repr__(self):
        msg = binascii.hexlify(self.data).decode('ascii')
        if len(msg) > 16:
            msg = msg[:16] + '...'

        return (
            'Message(total_len={!r}, msg_len={!r}, msg_offset={!r}, msg={!r})'
        ).format(self.total_len, self.msg_len, self.msg_offset, msg)

    def serialize(self):
        '''
        Converts a chunk into a bytestring, representing the serialized form of
        the chunk.
        '''
        msg = self.data
        self.msg_len = len(msg)

        header = _STRUCT_HHH.pack(
            self.total_len & 0xFFFF,
            self.msg_len & 0xFFFF,
            self.msg_offset & 0xFFFF)

        return header + msg

    @staticmethod
    def parse_message_header(header):
        '''
        Takes a 6-byte message header and returns a tuple of the appropriate
        Chunk object and the length that needs to be read from the lower layer.
        '''
        try:
            fields = _STRUCT_HHH.unpack(header)
        except struct.error:
            raise Exception('Invalid message header')

        total_len = fields[0]
        msg_len = fields[1]
        msg_offset = fields[2]

        return (Message(total_len, msg_offset), msg_len)

    def parse_message(self, data):
        '''
        Given the data of the message, parses it into message data.

        :param data: A memoryview object containing the message data. Must not
                     contain *more* data than the length returned by
                     :meth:`parse_message_header
                     <auto_flow_leaker.comb_coder.message.Message.parse_message_header>`.
        '''
        if not (self.msg_offset + len(data) <= self.total_len):
            raise ValueError(
                'Current message fragment is too large.')
        self.data = data.tobytes()  # memoryview
        self.msg_len = len(data)


def test_message():
    message, msg_len = Message.parse_message_header(
        b'\x04\x00\x03\x00\x01\x00')
    message.parse_message(memoryview('A' * msg_len))

    print message

    print message.serialize()
    print message.serialize()[:6]
    print message.serialize()[:6] == b'\x04\x00\x03\x00\x01\x00'


if __name__ == '__main__':
    test_message()
