AutoFlowLeaker
===

## Python Style Guide

- Use 4 spaces per indentation level.
- Limit all lines to a maximum of 79 characters.
- Surround top-level function and class definitions with two blank lines.
- ([read more](https://www.python.org/dev/peps/pep-0008/))

## Quick Start

### System Dependencies

- python
- pip
- liberasurecode: <https://github.com/openstack/liberasurecode>
- isa-l: <https://github.com/01org/isa-l>
- libarchive

### Python Packages

(see `requirements.txt`)

### Install Pre-requisites

1. Install dependency libraries

    1. Install `isa-l`, see <https://github.com/01org/isa-l#building-isa-l> for detail.

        Ubuntu only

        ```bash
        $ git clone https://github.com/01org/isa-l.git
        $ cd isa-l
        $ ./autogen.sh
        $ ./configure --prefix=/usr --libdir=/usr/lib
        $ make
        $ sudo make install
        ```

        On Mac OS X:

        ```bash
        $ brew install liberasurecode
        ```

        On Ubuntu:

        ```bash
        $ sudo apt-get install liberasurecode-dev libjerasure-dev libarchive-dev
        ```

    2. Install others:

        On Ubuntu:

        ```bash
        $ sudo apt-get install libmysqlclient-dev
        ```

2. Install dependency Python packages

    On Mac OS X:

    ```bash
    # install pip
    $ sudo easy_install pip
    $ sudo pip install --upgrade pip

    $ sudo pip install -r requirements.txt
    ```

    On Ubuntu:

    ```bash
    # install pip
    # 1) for Ubuntu 10.10 Maverick and newer
    $ sudo apt-get install python-pip
    # 2) for older versions of Ubuntu
    $ sudo apt-get install python-setuptools
    $ sudo easy_install pip

    $ sudo pip install --upgrade pip
    $ sudo apt-get install python-dev build-essential autoconf automake libtool
    $ sudo pip install -r requirements.txt
    ```

## Web Services & Evaluation Status

| Service Name | Integrated? | Read (s) | Write (s) | Delete (s) |
|:------------:|:-----------:|:--------:|:---------:|:----------:|
|Dropbox       |&#10003;     |0.400     |1.213      |0.956       |
|Email         |&#10003;     |          |           |            |
|Evernote      |&#10003;     |1.118     |1.150      |1.184       |
|Facebook      |&#10003;     |0.699     |1.479      |3.539       |
|RSS (Ghost)   |&#10003;     |0.386     |0.483      |0.378       |
|Github        |&#10003;     |1.091     |1.165      |1.143 (close)|
|Gmail         |&#10003;     |          |           |            |
|Google Drive  |             |          |           |            |
|Medium        |             |          |           |            |
|Twitter       |&#10003;     |0.828     |0.902      |0.784       |
|Weibo         |             |          |           |            |
|Wordpress     |&#10003;     |0.286     |4.855      |3.629       |
|Yinxiang      |&#10003;     |0.319     |0.407      |0.412       |

## Web Service API Domain

| Service Name | API Domain |
|:------------:|:----------:|
|Dropbox       |            |
|Email         |(not applicable?)|
|Evernote      |            |
|Facebook      |            |
|RSS (Ghost)   |            |
|Github        |            |
|Gmail         |(not applicable?)|
|Google Drive  |            |
|Medium        |            |
|Twitter       |            |
|Weibo         |            |
|Wordpress     |            |
|Yinxiang      |            |

## Notes

- "eva_rtt.py": measure the delay time of each automation service (e.g., IFTTT, Zapier)
- "eva\_rwd\_time": measure read/write/delete time of each channel
- Github does not support delete operation, because the state of the issue can only be "open" or "closed"
- "default.conf": configuration file, containing all the accounts, passwords and tokens
- "OurSystem.py": encoding and decoding (i.e., unranking and ranking) algorithm
- "cal\_rwd\_time.py": deprecated
- "capacity.py": deprecated
