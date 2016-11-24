AutoFlowLeaker
===

## Python Style Guide

- Use 4 spaces per indentation level.
- Limit all lines to a maximum of 79 characters.
- Surround top-level function and class definitions with two blank lines.
- ([read more](https://www.python.org/dev/peps/pep-0008/))

## Requirements

### System Dependency

- python
- pip

### Python Packages

- PyGitHub
- evernote
- facebook-sdk
- envelopes
- httplib2
- python-twitter

On Mac OS X:

```bash
# install pip
$ sudo easy_install pip
$ sudo pip install --upgrade pip

# install python third-party packages
$ sudo pip install -r requirements.txt
```

On Ubuntu:

```bash
# install pip
# 1) for Ubuntu 10.10 Maverick and newer
$ sudo apt-get install python-pip python-dev build-essential
$ sudo pip install --upgrade pip
# 2) for older versions of Ubuntu
$ sudo apt-get install python-setuptools python-dev build-essential
$ sudo easy_install pip
$ sudo pip install --upgrade pip

# install python third-party packages
$ sudo pip install -r requirements.txt
```

## Web Services & Evaluation Status

| Service Name | Integrated? | Read (s) | Write (s) | Delete (s) |
|:------------:|:-----------:|:--------:|:---------:|:----------:|
|Dropbox       |&#10003;     |0.400     |1.213      |0.956       |
|Evernote      |&#10003;     |1.118     |1.150      |1.184       |
|Facebook      |&#10003;     |0.699     |1.479      |3.539       |
|RSS (Ghost)   |&#10003;     |0.386     |0.483      |0.378       |
|Github        |&#10003;     |1.091     |1.165      |1.143 (close)|
|Twitter       |&#10003;     |0.828     |0.902      |0.784       |
|Wordpress     |&#10003;     |0.286     |4.855      |3.629       |
|Yinxiang      |&#10003;     |0.319     |0.407      |0.412       |
|Weibo         |             |          |           |            |

## Notes

- "eva_rtt.py": measure the delay time of each automation service (e.g., IFTTT, Zapier)
- "eva\_rwd\_time": measure read/write/delete time of each channel
- Github does not support delete operation, because the state of the issue can only be "open" or "closed"
- "default.conf": configuration file, containing all the accounts, passwords and tokens
- "OurSystem.py": encoding and decoding (i.e., unranking and ranking) algorithm
- "cal\_rwd\_time.py": deprecated
- "capacity.py": deprecated
