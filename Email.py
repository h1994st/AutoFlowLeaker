#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 18:20:44
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os
import smtplib

from envelopes import Envelope, SMTP

import Config


class Email(SMTP):
    '''
    Default email: covert_tom@163.com
    IMAP SSL, Port 465
    '''

    MAIL_163_SMTP_HOST = 'smtp.163.com'
    MAIL_163_SMTP_TLS = True

    def __init__(self):
        email = Config.Email('email')
        password = Config.Email('password')

        super(Email, self).__init__(
            host=self.MAIL_163_SMTP_HOST, port=465,
            login=email, password=password
        )

        # Hack '_conn'
        self._conn = smtplib.SMTP_SSL(self._host, self._port)
        self._tls = False  # Avoid calling 'self._conn.starttls()'
        self._connect(replace_current=False)

    @property
    def email(self):
        return self._login

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
        self.send(envelope)

    def get_emails(self):
        pass

    # Read
    def get_email(self):
        pass

    # Delete
    def delete_email(self):
        pass
