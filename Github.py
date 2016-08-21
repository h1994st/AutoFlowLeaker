#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 14:45:16
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import github

import Config


class Github(github.Github):
    '''
    Default repository: covertsan/Test-Py
    Default user: covertsan (covert.san@gmail.com)
    '''

    def __init__(self):
        username = Config.Github('username')
        password = Config.Github('password')
        repo = Config.Github('repo')

        super(Github, self).__init__(username, password)

        self._user = self.get_user()

        self._repo = self._user.get_repo(repo)

    @property
    def user(self):
        return self._user

    @property
    def repo(self):
        return self._repo

    @property
    def issues(self):
        return self.get_issues(readable=True)

    def _issue_to_dict(self, issue):
        return {
            'id': issue.id,
            'number': issue.number,
            'title': issue.title,
            'body': issue.body
        }

    def get_issues(self, readable=False):
        issues = self.repo.get_issues()
        if readable:
            return map(self._issue_to_dict, issues)
        return issues

    # Write
    def create_issue(self, title, body=github.GithubObject.NotSet):
        return self.repo.create_issue(title, body=body)

    # Read
    def get_issue(self, number, readable=False):
        issue = self.repo.get_issue(number)
        if readable:
            return self._issue_to_dict(issue)
        return issue

    # Delete (impossible)
    def delete_issue(self):
        assert False, 'Impossible'

    # Close
    def close_issue(self, number):
        self.get_issue(number).edit(state='closed')
