#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-27 14:31:50
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import argparse

import libarchive.public
import libarchive.constants

from ArgParseActionExtension import ReadableDirPath
from ArgParseActionExtension import ReadableFilePath


def compress(input_files, output_file):
    assert isinstance(input_files, list), input_files
    for file in input_files:
        assert isinstance(file, str) and os.path.exists(file), file
    assert isinstance(output_file, str), output_file
    assert not os.path.isdir(output_file), output_file
    assert not os.path.islink(output_file), output_file

    print 'Compressing...'
    print 'Input files: %s' % input_files

    # Compress
    libarchive.public.create_file(
        output_file,
        libarchive.constants.ARCHIVE_FORMAT_7ZIP,
        input_files)

    print 'Output file: %s' % output_file


def decompress(input_file, output_dir):
    assert isinstance(input_file, str), input_file
    assert os.path.exists(input_file), input_file
    assert os.path.isfile(input_file), input_file
    assert isinstance(output_dir, str), output_dir
    assert os.path.isdir(output_dir), output_dir

    print 'Decompressing...'
    print 'Input file: %s' % input_file
    print 'Ourput directory: %s' % output_dir

    # Decompress
    with libarchive.public.file_reader(input_file) as e:
        for entry in e:
            print '  ' + str(entry)
            with open(os.path.join(output_dir, str(entry)), 'wb') as f:
                for block in entry.get_blocks():
                    f.write(block)


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(
        description='Tool: compressor/decompressor using 7zip.')

    # Version
    parser.add_argument(
        '--version', action='version', version='%(prog)s 1.0')

    subparsers = parser.add_subparsers(
        dest='subcommand',
        title='subcommands',
        description='valid subcommands')

    # 'compress' command
    compress_parser = subparsers.add_parser('compress', help='Encoder')
    compress_parser.add_argument(
        '-f', '--files',
        nargs='+',
        help='files to compress',
        required=True)
    compress_parser.add_argument(
        '-o', '--output',
        help='output file',
        default='archiver.7z')

    # 'decompress' command
    decompress_parser = subparsers.add_parser('decompress', help='Decoder')
    decompress_parser.add_argument(
        '-F', '--file',
        action=ReadableFilePath,
        help='file to decompress',
        required=True)
    decompress_parser.add_argument(
        '-d', '--dest',
        action=ReadableDirPath,
        help='directory to drop decompressed file',
        default=os.path.abspath('.'))

    (args, _) = parser.parse_known_args()
    print 'Starting program...'
    print args

    if args.subcommand == 'compress':
        compress(args.files, args.output)
    elif args.subcommand == 'decompress':
        decompress(args.file, args.dest)
    else:
        raise Exception('Unknown subcommand.')

    print 'Done!'
