#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-24 16:33:59
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import pytz
import time
from pprint import pprint

import dropbox

import Config
from auto_flow_leaker.auto_flow.post import Post
from auto_flow_leaker.auto_flow.channel import Channel


class Dropbox(Channel):
    '''
    Default user: covert.san@gmail.com
    '''

    def __init__(self, folder=None):
        super(Dropbox, self).__init__()

        print 'Initialzing Dropbox channel:'

        self._dbx = dropbox.Dropbox(Config.Dropbox('access_token'))
        print '  Access token: %s' % Config.Dropbox('access_token')

        self.default_folder = folder
        print '  Default folder: %s' % self.default_folder

    def description(self):
        return 'access_token={!r}, default_folder={!r}'.format(
            Config.Dropbox('access_token'), self.default_folder)

    def send(self, content, title=None):
        '''
        Default title: unix epoch
        '''
        try:
            res = self.create_file(
                content, filename=(title or '%.6f.txt' % time.time()))
        except Exception:
            return None
        else:
            return Post(
                id=res.id,
                title=res.name,
                create_time=res.server_modified.replace(tzinfo=pytz.utc))

    def receive_all(self):
        def converter(file_meta):
            return Post(
                id=file_meta.id,
                title=file_meta.name,
                content=self.get_file(file_meta.name).content,
                create_time=file_meta.server_modified.replace(tzinfo=pytz.utc))

        return sorted(
            map(converter, self.get_files()),
            key=lambda x: x.create_time, reverse=True)

    def delete(self, item):
        self.delete_file(item.title)

    def delete_all(self):
        self.delete_all_files()

    @property
    def default_folder(self):
        '''
        Default folder for Dropbox channel.

        :rtype: str
        '''
        if self._default_folder_value is not None:
            return self._default_folder_value
        else:
            raise AttributeError('missing required field \'default_folder\'')

    @default_folder.setter
    def default_folder(self, val):
        self._default_folder_value = val or Config.Dropbox('root_dir')

    @default_folder.deleter
    def default_folder(self):
        self._default_folder_value = Config.Dropbox('root_dir')

    @property
    def files(self):
        return self.get_files()

    def create_file(self, content, filename=None):
        '''
        Upload a new file

        Default filename: unix epoch
        '''
        fullpath = os.path.join(self.default_folder, filename)

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
        fullpath = os.path.join(self.default_folder, filename)

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
        try:
            res = self._dbx.files_list_folder(
                self.default_folder,
                recursive=False, include_deleted=False)
        except Exception:
            return []
        else:
            return res.entries

    def delete_file(self, filename):
        '''
        Delete a file
        '''
        fullpath = os.path.join(self.default_folder, filename)
        self._dbx.files_delete(fullpath)

    def delete_all_files(self):
        '''
        Delete all the files
        '''
        print 'Delete all files in %s' % self.default_folder
        # Delete root dir
        print '  Delete default folder: %s' % self.default_folder
        self._dbx.files_delete(self.default_folder)

        # Create new root dir
        print '  Create new default folder: %s' % self.default_folder
        self._dbx.files_create_folder(self.default_folder)


def test_dropbox():
    dbx = Dropbox()

    # Read all
    pprint(dbx.files)

    # Write
    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        md = dbx.create_file(fp.read())

    # Read one
    res = dbx.get_file(md.name)
    print res
    print type(res)
    print dir(res)
    print res.content

    # Read all
    pprint(dbx.files)

    # Delete
    dbx.delete_file(md.name)

    # Read all
    pprint(dbx.files)


def test_upload_files():
    dbx = Dropbox()

    # Read all
    pprint(dbx.files)

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        content = fp.read()
        print '1'
        print dbx.send(content)
        time.sleep(1)
        print '2'
        print dbx.send(content)
        time.sleep(1)
        print '3'
        print dbx.send(content)
        time.sleep(1)
        print '4'
        print dbx.send(content)
        time.sleep(1)
        print '5'
        print dbx.send(content)
        time.sleep(1)

    # time.sleep(3)

    pprint(dbx.receive_all())

    # Read all
    pprint(dbx.files)

    # Delete all
    dbx.delete_all_files()

    # Read all
    pprint(dbx.files)


def test_delete_file():
    dbx = Dropbox()

    # Delete all
    dbx.delete_all()

    # Read all
    pprint(dbx.files)

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        content = fp.read()
        post = dbx.send(content)
    print post

    time.sleep(3)

    # Read all
    pprint(dbx.receive_all())

    # Delete all
    dbx.delete(post)

    # Read all
    pprint(dbx.receive_all())


if __name__ == '__main__':
    # test_delete_file()
    dbx = Dropbox(folder='/Zapier')
    posts = dbx.receive_all()
    print posts
    dbx.delete(posts[0])
    posts = dbx.receive_all()
    print posts
