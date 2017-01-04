#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-04 15:55:52
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import OurSystem


class CombCoder(object):
    '''
    Encoder/Decoder of CombCoder layer.
    '''
    def __init__(self, i, k):
        super(CombCoder, self).__init__()

        print 'Initializing CombCoder:'
        self.i = i
        self.k = k
        print '  i=%d, k=%d' % (i, k)

        self.capacity = OurSystem.capacity(i, k)
        print '  capacity=%d bit' % self.capacity

    def encode(self, data):
        '''
        Binary data -> post
        '''
        post, rK = OurSystem.unrank(self.i, self.k, data)

    def decode(self, post, rK):
        '''
        Post -> binary data
        '''
        return OurSystem.rank(post, rK)


def test_comb_coder():
    comb_coder = CombCoder(3, 3)
    comb_coder.encode(b'123123')


if __name__ == '__main__':
    test_comb_coder()
