#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-27 14:32:22
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import argparse

from pyeclib.ec_iface import ECDriver

from ArgParseActionExtension import ReadableDirPath


class ECCoder(object):
    '''
    Encoder/Decoder of ECCoder layer.
    '''
    def __init__(self, k, m, ec_type='isa_l_rs_vand'):
        assert isinstance(k, int), k
        assert isinstance(m, int), m

        super(ECCoder, self).__init__()

        print 'Initializing ECCoder:'
        self.ec_driver = ECDriver(k=k, m=m, ec_type=ec_type)
        print '  k=%d, m=%d' % (k, m)
        print '  ec_type=%s' % ec_type

    def encode(self, data):
        '''
        Data -> data fragments
        '''
        print 'Encoding...'
        return self.ec_driver.encode(data)

    def encode_file(self, input_file, output_dir):
        assert isinstance(input_file, file), input_file
        assert isinstance(output_dir, str), output_dir
        assert os.path.isdir(output_dir), output_dir

        print 'Encoding input file:'
        print '  Intput file: %s' % os.path.abspath(input_file.name)
        print '  Output directory: %s' % output_dir

        # Encode
        fragments = self.encode(input_file.read())
        input_file.close()

        # Save to files
        i = 0
        origin_filename = os.path.basename(input_file.name)
        for fragment in fragments:
            filename = '%s.%d' % (origin_filename, i)
            with open(os.path.join(
                    output_dir, filename), 'wb') as fp:
                fp.write(fragment)
            print '  ' + filename
            i += 1

    def decode(self, fragments):
        '''
        Data fragments -> data
        '''
        print 'Decoding...'
        return self.ec_driver.decode(fragments)

    def decode_file(self, input_fragments, output_file):
        assert isinstance(input_fragments, list), input_fragments
        for input_fragment in input_fragments:
            assert isinstance(input_fragment, file), input_fragment
        assert isinstance(output_file, file), output_file

        print 'Decoding input fragments:'
        print '  Intput fragments: %s' % map(
            lambda x: os.path.abspath(x.name), input_fragments)

        fragment_list = []
        for input_fragment in input_fragments:
            print '  ' + os.path.basename(input_fragment.name)
            fragment_list.append(input_fragment.read())
            input_fragment.close()

        # Decode
        decoded_file = self.decode(fragment_list)

        # Save to file
        output_file.write(decoded_file)
        output_file.close()

        print '  Output file: %s' % os.path.abspath(output_file.name)


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Tool: encoder/decoder using erasure codes (Reed-Solomon codes).')

    # Version
    parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0')

    parser.add_argument(
        '-k', type=int,
        help='number of data elements',
        required=True)
    parser.add_argument(
        '-m', type=int,
        help='number of parity elements',
        required=True)
    parser.set_defaults(ec_type='isa_l_rs_vand')

    subparsers = parser.add_subparsers(
        dest='subcommand',
        title='subcommands',
        description='valid subcommands')

    # 'encode' command
    encode_parser = subparsers.add_parser('encode', help='Encoder')
    encode_parser.add_argument(
        '-f', '--file',
        type=argparse.FileType('r'),
        help='file to encode',
        required=True)
    encode_parser.add_argument(
        '-d', '--dest',
        action=ReadableDirPath,
        help='directory to drop encoded fragments',
        default=os.path.abspath('.'))

    # 'decode' command
    decode_parser = subparsers.add_parser('decode', help='Decoder')
    decode_parser.add_argument(
        '-f', '--fragments',
        type=argparse.FileType('r'),
        nargs='+',
        help='fragments to decode',
        required=True)
    decode_parser.add_argument(
        '-o', '--output',
        type=argparse.FileType('w'),
        help='output file',
        default='output.tmp')

    (args, _) = parser.parse_known_args()
    print 'Starting program...'
    print args

    ec_coder = ECCoder(args.k, args.m)

    if args.subcommand == 'encode':
        ec_coder.encode_file(args.file, args.dest)
    elif args.subcommand == 'decode':
        ec_coder.decode_file(args.fragments, args.output)
    else:
        raise Exception('Unknown subcommand.')

    print 'Done!'
