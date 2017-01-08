#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 18:20:44
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import pytz
import time
import smtplib
from pprint import pprint

from envelopes import Envelope, SMTP
from betterimap import IMAPAdapter

import Config
from auto_flow_leaker.auto_flow.post import Post
from auto_flow_leaker.auto_flow.channel import Channel


MAIL_163_SMTP_HOST = 'smtp.163.com'
MAIL_163_SMTP_TLS = True

MAIL_163_IMAP_HOST = 'imap.163.com'
MAIL_163_IMAP_TLS = True


class Email(Channel):
    '''
    Default email: covert_tom@163.com
    SMTP, SSL Port 465/994, non-SSL Port 25
    IMAP, SSL Port 993, non-SSL Port 143

    Ref: http://help.163.com/09/1223/14/5R7P3QI100753VB8.html?servCode=6010377
    '''
    def __init__(self,
                 email=None,
                 password=None):
        super(Email, self).__init__()

        self._email = email or Config.Email('email1')
        password = password or Config.Email('password')

        smtp_port = 465 if MAIL_163_SMTP_TLS else 25
        imap_port = 993 if MAIL_163_IMAP_TLS else 143

        # SMTP client
        self.smtp_client = SMTP(
            login=self._email, password=password,
            host=MAIL_163_SMTP_HOST, port=smtp_port)

        if MAIL_163_SMTP_TLS:
            # Hack '_conn' for TLS connection
            self.smtp_client._conn = smtplib.SMTP_SSL(
                self.smtp_client._host, self.smtp_client._port)
            # Avoid calling 'self._conn.starttls()'
            self.smtp_client._tls = False
            self.smtp_client._connect(replace_current=False)

        # IMAP client
        self.imap_client = IMAPAdapter(
            login=self._email, password=password,
            host=MAIL_163_IMAP_HOST, port=imap_port,
            ssl=MAIL_163_IMAP_TLS)

        self.imap_client.select('inbox')

    def description(self):
        return 'email={!r}'.format(self.email)

    def send(self, content, title=None):
        '''
        Default title: unix epoch

        Note: when success, this function will not return a Post object
        '''
        try:
            res = self.send_email(
                subject=(title or '%.6f.txt' % time.time()),
                text_body=content)
        except Exception as e:
            print e
            return None
        else:
            return res

    def receive(self):
        '''Retrieve the latest item from the channel

        Return: {
            'title': ...,
            'content': ...,
            'create_time': ... <unix epoch>,
            'item_id': ...
        }'''
        items = [item for item in self.get_emails(limit=1)]

        if len(items) == 0:
            return None

        return Post(
            id=items[0].uid,
            title=items[0].subject,
            content=[items[0].plaintext(), items[0].html()],
            create_time=items[0].date.replace(tzinfo=pytz.utc))

    def receive_all(self):
        def converter(email_meta):
            return Post(
                id=email_meta.uid,
                title=email_meta.subject,
                content=[email_meta.plaintext(), email_meta.html()],
                create_time=email_meta.date.replace(tzinfo=pytz.utc))

        return map(converter, self.get_emails())

    def delete(self, item):
        self.delete_email(item.id)

    def delete_all(self):
        self.delete_all_emails()

    @property
    def email(self):
        return self._email

    # Write
    def send_email(self, subject=None,
                   text_body=None, html_body=None,
                   attachments=[]):
        '''
        Send email to 'trigger@recipe.ifttt.com'
        '''

        envelope = Envelope(
            from_addr=(self.email, 'San Zhang'),
            to_addr=(Config.IFTTT('email_trigger'), 'IFTTT'),
            subject=subject,
            text_body=text_body,
            html_body=html_body
        )
        for attachment in attachments:
            if not (isinstance(attachment, (str, unicode)) and
                    os.path.exists(attachment)):
                continue
            envelope.add_attachment(attachment)

        # Send
        return self.smtp_client.send(envelope)

    # Read
    def get_email(self, uid):
        '''
        Get an email
        '''
        msg = self.imap_client.fetch_email_by_uid(uid)
        msg.uid = uid
        return msg

    def get_emails(self, limit=100):
        '''
        Get all the emails
        '''
        return self.imap_client.search(limit=limit)

    # Delete
    def delete_email(self, uid):
        '''
        Delete an email
        '''
        self.imap_client.mail.uid('store', uid, '+FLAGS', '(\\Deleted)')
        self.imap_client.mail.expunge()

    def delete_all_emails(self):
        '''
        Delete all the emails
        '''
        for email in self.get_emails():
            print 'Delete %s (%s)' % (email.subject, email.uid)
            self.delete_email(email.uid)


def test_email():
    e = Email()

    # Read all
    pprint(e)

    # Write
    print 'Input file: ./data/eva_time_data_2.in'
    with open('data/eva_time_data_2.in', 'r') as fp:
        e.send(fp.read())

    # Read the latest one
    email = e.receive()

    # Read all
    pprint(e.receive_all())

    # Delete
    e.delete(email)

    # Read all
    pprint(e.receive_all())


def test_delete_all_sent_emails():
    e1 = Email()

    print e1.imap_client.list()

    e1.imap_client.select(e1.imap_client.get_sent_folder())
    print e1.receive()

    print e1.delete_all_emails()


if __name__ == '__main__':
    test_email()
