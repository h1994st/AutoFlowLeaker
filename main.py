#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-18 14:17:38
# @Author  : Tom Hu (h1994st@gmail.com)
# @Link    : http://h1994st.com
# @Version : 1.0

from github import Github
from evernote.api.client import EvernoteClient
import evernote.edam.error.ttypes as Errors
import evernote.edam.type.ttypes as Types
import smtplib
from email.mime.text import MIMEText  # 引入smtplib和MIMEText
import facebook
import requests


CONTENT = '''
# h1
## h2
### h3
#### h4
##### h5
###### h6
~~~
_iii_
__ooo__

<img width="16" height="16" alt="star" src="data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7" />

<img alt="star" src="data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7" />
'''


YINXIANG_PRODUCTION_DEV_TOKENS = 'S=s72:U=eed9c2:E=15df5c792e2:C=1569e1664f8:P=1cd:A=en-devtoken:V=2:H=ae124edf7dc25c7251d1a9588974fc1c'
EVERNOTE_SANDBOX_DEV_TOKENS = 'S=s1:U=92d33:E=15df5bf58c9:C=1569e0e2b80:P=1cd:A=en-devtoken:V=2:H=be0a1031b571827267a3d968cf90436f'

IFTTT_TRIGGER = 'trigger@recipe.ifttt.com'


def test_github():
    # First create a Github instance:
    g = Github('covertsan', 'P0lyUSecurity')

    # Then play with your Github objects:
    repo = g.get_user().get_repo('Test-Py')

    repo.create_issue(
        'The first issue',
        body=CONTENT)


def makeNote(authToken, noteStore, noteTitle, noteBody, parentNotebook=None):
    nBody = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    nBody += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
    nBody += "<en-note>%s</en-note>" % noteBody

    # Create note object
    ourNote = Types.Note()
    ourNote.title = noteTitle
    ourNote.content = nBody

    # parentNotebook is optional; if omitted, default notebook is used
    if parentNotebook and hasattr(parentNotebook, 'guid'):
        ourNote.notebookGuid = parentNotebook.guid

    # Attempt to create note in Evernote account
    try:
        note = noteStore.createNote(authToken, ourNote)
    except Errors.EDAMUserException, edue:
        # Something was wrong with the note data
        # See EDAMErrorCode enumeration for error code explanation
        # http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
        print "EDAMUserException:", edue
        return None
    except Errors.EDAMNotFoundException, ednfe:
        # Parent Notebook GUID doesn't correspond to an actual notebook
        print "EDAMNotFoundException: Invalid parent notebook GUID"
        print ednfe
        return None
    # Return created note object
    return note


def test_evernote_sandbox():
    client = EvernoteClient(
        token=EVERNOTE_SANDBOX_DEV_TOKENS,
        sandbox=True)
    print 'Sandbox'

    noteStore = client.get_note_store()

    notebooks = noteStore.listNotebooks()
    for n in notebooks:
        print 'Notebook', n.name


def test_evernote():
    pass


def test_yinxiang():
    client = EvernoteClient(
        token=YINXIANG_PRODUCTION_DEV_TOKENS,
        sandbox=False,
        service_host='app.yinxiang.com')
    print 'Token: ', client.token

    note_store = client.get_note_store()

    # Make API calls
    notebook = note_store.getDefaultNotebook(client.token)
    print 'Default Notebook: ', notebook.name

    makeNote(
        client.token, note_store,
        'qwr',
        CONTENT,
        notebook)
    print 'Done!'


def test_wordpress():
    pass


def test_163_email():
    host = 'smtp.163.com'  # 设置发件服务器地址
    port = 465  # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式
    sender = 'covert_tom@163.com'  # 设置发件邮箱，一定要自己注册的邮箱
    # pwd = 'PolyUSecurity'  # 设置发件邮箱的密码，等会登陆会用到
    pwd = 'hst521'  # 设置发件邮箱的密码，等会登陆会用到
    receiver = IFTTT_TRIGGER  # 设置邮件接收人
    body = CONTENT  # 设置邮件正文，这里是支持HTML的

    msg = MIMEText(body, 'html')  # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = 'yeiqwer'  # 设置邮件标题
    msg['from'] = sender  # 设置发送人
    msg['to'] = receiver  # 设置接收人

    s = smtplib.SMTP_SSL(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
    s.login(sender, pwd)  # 登陆邮箱
    s.sendmail(sender, receiver, msg.as_string())  # 发送邮件！

    print 'over'  # 发送成功就会提示


def test_facebook():
    def some_action(post):
        print(post)

    access_token = 'EAACEdEose0cBAJHY1DNkrZCpRlVPRFah2OS1JjFxngLELFPY3Gv0LE9ax651j9li8P14JrhMl7bZCIaHt3Xklwa4rnkmvJDllNOGZBUPs0mxDmigvvZCbIGiOI93E9lkQgQi1TZBh3PEoevvQ8KZBZAn5O0IwQgOuK8ZC11KNa6X6qDTxuXGOG3H'
    # Look at Bill Gates's profile for this example by using his Facebook id.
    user = 'me'

    graph = facebook.GraphAPI(access_token=access_token, version='2.7')
    profile = graph.get_object(user)
    posts = graph.get_connections(profile['id'], 'posts')

    # Wrap this block in a while loop so we can keep paginating requests until
    # finished.
    while True:
        try:
            [some_action(post=post) for post in posts['data']]
            # Attempt to make a request to the next page of data, if it exists.
            posts = requests.get(posts['paging']['next']).json()
        except KeyError:
            # When there are no more pages (['paging']['next']), break from the
            # loop and end the script.
            break


def main():
    test_yinxiang()

if __name__ == '__main__':
    main()
