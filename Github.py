#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-20 14:45:16
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

import github

import Config
from timeout import timeout

TIMEOUT = int(Config.Global('timeout'))


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

        self._repo = self.user.get_repo(repo)

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

    @timeout(TIMEOUT)
    def get_issues(self, readable=False):
        issues = self.repo.get_issues()
        if readable:
            return map(self._issue_to_dict, issues)
        return issues

    # Write
    @timeout(TIMEOUT)
    def create_issue(self, title, body=github.GithubObject.NotSet):
        return self.repo.create_issue(title, body=body)

    # Read
    @timeout(TIMEOUT)
    def get_issue(self, number, readable=False):
        issue = self.repo.get_issue(number)
        if readable:
            return self._issue_to_dict(issue)
        return issue

    # Delete (impossible)
    def delete_issue(self):
        assert False, 'Impossible'

    # Close
    @timeout(TIMEOUT)
    def close_issue(self, number):
        self.get_issue(number).edit(state='closed')

    # Create a new repository
    def create_repo(self, name='Test-Py'):
        assert self.repo is None, self.repo

        self._repo = self.user.create_repo(
            name, description='HEHEH', has_issues=True,
            has_wiki=False, has_downloads=False, auto_init=True)

    # Delete a repository
    def delete_repo(self):
        assert self.repo is not None, self.repo

        self.repo.delete()
        self._repo = None

    # Delete all issues
    def delete_all_issues(self):
        # Delete repo
        self.delete_repo()

        # Create new repo
        self.create_repo()
