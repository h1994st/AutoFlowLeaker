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

    def get_issues(self, readable=False):
        issues = self.repo.get_issues()
        if readable:
            return map(self._issue_to_dict, issues)
        return issues

    # Write
    @timeout(TIMEOUT)
    def create_issue(self, title, body=github.GithubObject.NotSet,
                     assignee=github.GithubObject.NotSet):
        return self.repo.create_issue(title, body=body, assignee=assignee)

    # Read
    @timeout(TIMEOUT)
    def get_issue(self, number, readable=False):
        issue = self.repo.get_issue(number)
        if readable:
            return self._issue_to_dict(issue)
        return issue

    # Delete (impossible)
    def delete_issue(self, number=None, issue=None):
        self.close_issue(number=number, issue=issue)

    # Close
    @timeout(TIMEOUT)
    def close_issue(self, number=None, issue=None):
        assert (number is None or
                isinstance(number, int)), number
        assert (issue is None or
                isinstance(issue, github.Issue.Issue)), issue

        if number is None and issue is None:
            return

        if issue is not None:
            issue.edit(state='closed')
            return

        # issue is None, but number is not None
        self.get_issue(number).edit(state='closed')

    # Create a new repository
    def create_repo(self, name=Config.Github('repo')):
        self._repo = self.user.create_repo(
            name, description='HEHEH', has_issues=True,
            has_wiki=False, has_downloads=False, auto_init=True)

        return self._repo

    # Get a repository
    def change_repo(self, name=None):
        assert name is None or isinstance(name, (str, unicode)), name

        if name is None:
            # Change to default
            name = Config.Github('repo')  # Default repository name

        self._repo = self.user.get_repo(name)
        return self._repo

    # Delete a repository
    def delete_repo(self, name=None):
        assert name is None or isinstance(name, (str, unicode)), name

        if name is None or name == self.repo.name:
            # Current repo
            repo = self.repo
        else:
            repo = self.user.get_repo(name)

        if repo is None:
            # no repo
            print 'The repository you designate does not exist.'
            return

        # Delete
        repo.delete()

        # Change to default
        self.change_repo()

    # Delete all issues
    def delete_all_issues(self, name=None):
        assert name is None or isinstance(name, (str, unicode)), name

        # Delete repo
        self.delete_repo(name=name)

        # Create new repo
        self.create_repo(name=name)


if __name__ == '__main__':
    g = Github()

    print g.repo

    # Change repository
    print g.change_repo('Yinxiang')

    # Create repository
    repository = g.create_repo(name='Test')

    # Write
    issue = g.create_issue('title', body='body')
    print issue

    # Read
    print g.get_issue(issue.number)

    # Delete (Close)
    g.delete_issue(issue=issue)

    # Delete repository
    g.delete_repo()

    print g.repo
