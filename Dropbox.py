#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-24 16:33:59
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import time
from pprint import pprint

import dropbox

import Config


class Dropbox(object):
    '''
    Default user: covert.san@gmail.com
    '''

    def __init__(self):
        super(Dropbox, self).__init__()

        self._dbx = dropbox.Dropbox(Config.Dropbox('access_token'))

    @property
    def files(self):
        return self.get_files()

    def create_file(self, content):
        '''
        Upload a new file
        '''
        filename = '%s.txt' % str(int(time.time()))
        fullpath = os.path.join(Config.Dropbox('root_dir'), filename)

        try:
            res = self._dbx.files_upload(content, fullpath, autorename=True)
        except dropbox.exceptions.ApiError as err:
            print '*** API error', err
            raise err
        else:
            return res

    def get_file(self, filename, save=False):
        '''
        Download a file in 'AutoFlow' folder
        '''
        fullpath = os.path.join(Config.Dropbox('root_dir'), filename)

        try:
            if save:
                md, res = self._dbx.files_download_to_file(
                    Config.Dropbox('local_folder'), fullpath)
            else:
                md, res = self._dbx.files_download(fullpath)
        except dropbox.exceptions.ApiError as err:
            print '*** API error', err
            raise err
        else:
            return res

    def get_files(self):
        '''
        Get the metadata of all files
        '''
        res = self._dbx.files_list_folder(
            Config.Dropbox('root_dir'),
            recursive=False, include_deleted=False)
        return res.entries

    def delete_file(self, filename):
        '''
        Delete a file
        '''
        fullpath = os.path.join(Config.Dropbox('root_dir'), filename)
        return self._dbx.files_delete(fullpath)

    def delete_all_files(self):
        '''
        Delete all the files
        '''
        # Delete root dir
        self._dbx.files_delete(Config.Dropbox('root_dir'))

        # Create new root dir
        self._dbx.files_create_folder(Config.Dropbox('root_dir'))


def test_dropbox():
    dbx = Dropbox()

    # Read all
    pprint(dbx.files)

    # Write
    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        md = dbx.create_file(fp.read())

    # Read all
    pprint(dbx.files)

    # Delete
    dbx.delete_file(md.name)

    # Read all
    pprint(dbx.files)


def test_file_upload():
    dbx = Dropbox()

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        dbx.create_file(fp.read())


if __name__ == '__main__':
    test_dropbox()
