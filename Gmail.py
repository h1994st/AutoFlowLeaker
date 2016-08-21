#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-22 04:24:26
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import os

from envelopes import Envelope, GMailSMTP

import Config


class Gmail(GMailSMTP):
    '''
    Default email: covert.san@gmail.com
    '''

    def __init__(self):
        assert False, 'Not implemented yet'

        email = Config.Gmail('email')
        password = Config.Gmail('password')

        super(Gmail, self).__init__(email, password)

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
