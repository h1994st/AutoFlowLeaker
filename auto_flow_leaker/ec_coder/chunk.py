#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-04 11:59:55
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

# import struct
import binascii

# Struct for packing and unpacking
# _STRUCT_BBH = struct.Struct('>BBH')


class Chunk(object):
    '''
    Basic data unit of ECCoder layer.

    pure data chunk
    '''
    def __init__(self, data=b''):
    # def __init__(self, seq_num, chunk_num, data=b''):
        # if not (seq_num >= 0 and seq_num <= 255):
        #     raise ValueError(
        #         'Sequence Number must be in the range of [0, 255]')
        # if not (chunk_num >= 0 and chunk_num <= 255):
        #     raise ValueError(
        #         'Chunk Number must be in the range of [0, 255]')

        super(Chunk, self).__init__()

        # self.seq_num = seq_num  # 8-bit number (0~255)
        # self.chunk_num = chunk_num  # 8-bit number (0~255)
        self.data = data

        self.body_len = 0  # 16-bit number (0~65535)

    def __repr__(self):
        body = binascii.hexlify(self.serialize_body()).decode('ascii')
        if len(body) > 16:
            body = body[:16] + '...'

        # return (
        #     'Chunk(seq={!r}, #={!r}, body_len={!r}, body={!r})'
        # ).format(self.seq_num, self.chunk_num, self.body_len, body)
        return (
            'Chunk(body_len={!r}, body={!r})'
        ).format(self.body_len, body)

    def serialize(self):
        '''
        Converts a chunk into a bytestring, representing the serialized form of
        the chunk.
        '''
        body = self.serialize_body()
        self.body_len = len(body)

        # header = _STRUCT_BBH.pack(
        #     self.seq_num & 0xFF,
        #     self.chunk_num & 0xFF,
        #     self.body_len & 0xFFFF)

        # return header + body
        return self.serialize_body()

    def serialize_body(self):
        return b''.join([self.data])

    # @staticmethod
    # def parse_chunk_header(header):
    #     '''
    #     Takes a 4-byte chunk header and returns a tuple of the appropriate
    #     Chunk object and the length that needs to be read from the lower layer.
    #     '''
    #     try:
    #         fields = _STRUCT_BBH.unpack(header)
    #     except struct.error:
    #         raise Exception('Invalid chunk header')

    #     seq_num = fields[0]
    #     chunk_num = fields[1]
    #     body_len = fields[2]

    #     return (Chunk(seq_num, chunk_num), body_len)

    def parse_body(self, data):
        '''
        Given the body of the chunk, parses it into chunk data.

        :param data: A memoryview object containing the body data of the chunk.
                     Must not contain *more* data than the length returned by
                     :meth:`parse_chunk_header
                     <auto_flow_leaker.ec_coder.chunk.Chunk.parse_chunk_header>`.
        '''
        self.data = data.tobytes()  # memoryview
        self.body_len = len(data)


def test_chunk():
    # chunk, body_len = Chunk.parse_chunk_header(b'\x01\x03\xff\xff')
    # chunk.parse_body(memoryview('A' * body_len))

    # print chunk
    chunk = Chunk(data='starsadfdsfa')

    print chunk


if __name__ == '__main__':
    test_chunk()
