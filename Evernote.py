#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 18:25:17
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import time
import pytz
import binascii
import datetime
from pprint import pprint

import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors
from evernote.edam.notestore import NoteStore
from evernote.api.client import EvernoteClient

import Config
from timeout import timeout
from auto_flow_leaker.auto_flow.post import Post
from auto_flow_leaker.auto_flow.channel import Channel


TIMEOUT = int(Config.Global('timeout'))


class Evernote(EvernoteClient, Channel):
    '''
    Default user: ctom357 (covert.san@gmail.com)
    '''

    def __init__(self, **kwargs):
        print 'Initializing Evernote/Yinxiang:'

        kwargs.setdefault('service_host', Config.Evernote('host'))
        print '  Service host: %s' % Config.Evernote('host')

        kwargs.setdefault('token', Config.Evernote('token'))
        print '  Access token: %s' % Config.Evernote('token')

        kwargs.setdefault('sandbox', False)
        print '  Sandbox: False'

        super(Evernote, self).__init__(**kwargs)

        self._note_store = self.get_note_store()

        self.default_notebook = kwargs.pop(
            'default_notebook', self.note_store.getDefaultNotebook(self.token))
        print '  Default notebook: %s' % self.default_notebook.name

    def description(self):
        return 'username={!r}, email={!r}, server_host={!r}, token={!r}, sandbox={!r}'.format(
            Config.Evernote('username'), Config.Evernote('email'),
            Config.Evernote('host'), Config.Evernote('token'), False)

    def send(self, content, title=None):
        '''
        Default title: unix epoch
        '''
        try:
            note = self.create_note(
                (title or '%.6f' % time.time()), content)
        except Exception:
            return None
        else:
            return Post(
                id=note.guid,
                title=note.title,
                create_time=datetime.datetime.fromtimestamp(
                    note.created / 1000, pytz.utc))

    def receive_all(self):
        def converter(note):
            return Post(
                id=note.guid,
                title=note.title,
                content=self.get_note(note.guid).content,
                create_time=datetime.datetime.fromtimestamp(
                    note.created / 1000, pytz.utc))

        return sorted(
            map(converter, self.get_notes()),
            key=lambda x: x.create_time, reverse=True)

    def delete(self, item):
        self.delete_note(guid=item.id)

    def delete_all(self):
        self.delete_notes(notebook=self.default_notebook)

    @property
    def default_notebook(self):
        '''
        Default notebook for Evernote channel.

        :rtype: evernote.edam.type.ttypes.Notebook
        '''
        if self._default_notebook_value is not None:
            return self._default_notebook_value
        else:
            raise AttributeError('missing required field \'default_notebook\'')

    @default_notebook.setter
    def default_notebook(self, val):
        if isinstance(val, str):
            self._default_notebook_value = self.get_notebook(name=val)
        elif isinstance(val, Types.Notebook):
            self._default_notebook_value = val
        else:
            raise AttributeError('attribute \'default_notebook\' type error')

    @default_notebook.deleter
    def default_notebook(self):
        self._default_folder_value = self.note_store.getDefaultNotebook(
            self.token)

    @property
    def note_store(self):
        return self._note_store

    @property
    def notebooks(self):
        return self.get_notebooks(readable=True)

    def _notebook_to_dict(self, notebook):
        assert isinstance(notebook, Types.Notebook), notebook

        ret = {
            'guid': notebook.guid,
            'name': notebook.name,
            'default': notebook.defaultNotebook
        }

        return ret

    def _note_to_dict(self, note):
        assert isinstance(note, (Types.Note, NoteStore.NoteMetadata)), note

        ret = {
            'guid': note.guid,
            'title': note.title,
            'length': note.contentLength,
            'created': note.created,  # Unix Epoch
            'notebook_guid': note.notebookGuid,
        }

        if isinstance(note, Types.Note):
            ret['content'] = note.content
            ret['resources'] = note.resources

        return ret

    @timeout(TIMEOUT)
    def get_notebooks(self, readable=False):
        assert isinstance(readable, bool)

        notebooks = self.note_store.listNotebooks(self.token)
        if readable:
            return map(self._notebook_to_dict, notebooks)
        return notebooks

    @timeout(TIMEOUT)
    def get_notebook(self, guid=None, name=None, readable=False):
        assert guid is None or isinstance(guid, (str, unicode)), guid
        assert name is None or isinstance(name, (str, unicode)), name
        assert isinstance(readable, bool), readable

        if name is None and guid is None:
            return None

        if guid is not None:
            # Using guid to retrieve notebook
            notebook = self.note_store.getNotebook(self.token, guid)
        else:
            # name is not None
            # Get notebooks at first
            notebooks = self.get_notebooks()
            candidate_notebooks = filter(
                lambda notebook: notebook.name == name, notebooks)
            assert len(candidate_notebooks) <= 1
            if len(candidate_notebooks) == 0:
                return None
            notebook = candidate_notebooks[0]

        assert isinstance(notebook, Types.Notebook), notebook

        if readable:
            return self._notebook_to_dict(notebook)
        return notebook

    @timeout(TIMEOUT)
    def get_notes(self, notebook=None, notebook_guid=None, readable=False):
        assert (notebook is None or
                isinstance(notebook, Types.Notebook)), notebook
        assert (notebook_guid is None or
                isinstance(notebook_guid, (str, unicode))), notebook_guid
        assert isinstance(readable, bool), readable

        if notebook is None and notebook_guid is None:
            # Set default notebook
            notebook = self.note_store.getDefaultNotebook(self.token)

        note_filter = NoteStore.NoteFilter()
        note_filter.order = Types.NoteSortOrder.CREATED
        note_filter.ascending = False

        if notebook is not None:
            note_filter.notebookGuid = notebook.guid
        else:
            # notebook_guid is not None
            note_filter.notebookGuid = notebook_guid

        spec = NoteStore.NotesMetadataResultSpec(
            includeTitle=True,
            includeCreated=True,
            includeNotebookGuid=True,
            includeContentLength=True)

        notes_meta_list = self.note_store.findNotesMetadata(
            self.token, note_filter, 0, 256, spec)

        assert isinstance(
            notes_meta_list, NoteStore.NotesMetadataList), notes_meta_list

        if readable:
            return map(self._note_to_dict, notes_meta_list.notes)
        return notes_meta_list.notes

    # Write
    @timeout(TIMEOUT)
    def create_note(self, title, body, resources=[], notebook=None):
        '''
        Create a Note instance with title and body
        Send Note object to user's account
        '''

        assert isinstance(title, (str, unicode)), title
        assert isinstance(body, (str, unicode)), body

        ourNote = Types.Note()
        ourNote.title = title

        # Build body of note
        nBody = '<?xml version="1.0" encoding="UTF-8"?>'
        nBody += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        nBody += '<en-note>%s' % body
        if resources:
            # Add Resource objects to note body
            nBody += '<br />' * 2
            ourNote.resources = resources
            for resource in resources:
                hexhash = binascii.hexlify(resource.data.bodyHash)
                nBody += 'Attachment with hash %s: <br /><en-media type="%s" hash="%s" /><br />' % (hexhash, resource.mime, hexhash)
        nBody += '</en-note>'

        ourNote.content = nBody

        # parentNotebook is optional; if omitted, default notebook is used
        if notebook and hasattr(notebook, 'guid'):
            ourNote.notebookGuid = notebook.guid

        # Attempt to create note in Evernote account
        try:
            note = self.note_store.createNote(self.token, ourNote)
        except Errors.EDAMUserException, edue:
            # Something was wrong with the note data
            # See EDAMErrorCode enumeration for error code explanation
            # http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
            print 'EDAMUserException:', edue
            return None
        except Errors.EDAMNotFoundException, ednfe:
            # Parent Notebook GUID doesn't correspond to an actual notebook
            print 'EDAMNotFoundException: Invalid parent notebook GUID'
            print ednfe
            return None

        # Return created note object
        return note

    # Delete
    @timeout(TIMEOUT)
    def delete_note(self, note=None, guid=None):
        assert (note is None or
                isinstance(note, (Types.Note, NoteStore.NoteMetadata))), note
        assert guid is None or isinstance(guid, (str, unicode)), guid

        if note is None and guid is None:
            return

        if note is not None:
            self.note_store.deleteNote(self.token, note.guid)
        else:
            # guid is not None
            self.note_store.deleteNote(self.token, guid)

    # Read
    @timeout(TIMEOUT)
    def get_note(self, guid,
                 withContent=True,
                 withResourcesData=False,
                 withResourcesRecognition=False,
                 withResourcesAlternateData=False,
                 readable=False):
        assert isinstance(guid, (str, unicode)), guid

        note = self.note_store.getNote(
            self.token, guid,
            withContent, withResourcesData,
            withResourcesRecognition, withResourcesAlternateData)

        assert isinstance(note, Types.Note)

        if readable:
            return self._note_to_dict(note)
        return note

    def delete_notes(self, notebook=None, notebook_guid=None):
        '''
        Delete all the posts
        '''
        assert (notebook is None or
                isinstance(notebook, Types.Notebook)), notebook
        assert (notebook_guid is None or
                isinstance(notebook_guid, (str, unicode))), notebook_guid

        if notebook is None and notebook_guid is None:
            # Set default notebook
            notebook = self.note_store.getDefaultNotebook(self.token)

        # Retrieve all notes in the notebook
        notes = self.get_notes(notebook=notebook, notebook_guid=notebook_guid)

        for note in notes:
            print 'Delete %s (%s)' % (note.title, note.guid)
            self.delete_note(note=note)


def test_evernote():
    e = Evernote()

    # Read all
    pprint(e.receive_all())

    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        content = fp.read()
        print e.send(content)

    # time.sleep(3)

    pprint(e.receive_all())

    # Delete all
    e.delete_all()

    # Read all
    pprint(e.receive_all())


if __name__ == '__main__':
    print Evernote()
    # test_evernote()
