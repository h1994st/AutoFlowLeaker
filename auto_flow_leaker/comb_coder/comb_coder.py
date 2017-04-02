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

        self.capacity, count, t9, t5 = OurSystem.capacity(i, k)
        print '  capacity=%d bit(s) (%d)' % (self.capacity, count)

    def encode(self, data):
        '''
        Binary data -> post
        '''
        post, rK = OurSystem.unrank(self.i, self.k, data)

        return post, rK

    def decode(self, post, rK):
        '''
        Post -> binary data
        '''
        return OurSystem.rank(post, rK)


def test_comb_coder():
    comb_coder = CombCoder(3, 3)
    print comb_coder.encode(0)


if __name__ == '__main__':
    test_comb_coder()
