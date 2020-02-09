One Time Sync
=============

Requirement
-----------
1. `python-2.7` for making this program works.
2. `open-ssh` set up on client and on remote server to set-up secure channels.
3. `keychain` set up in background (or any other ssh-agent ?) to manage identification and authentication by rsa keys.
4. `rsync` on client and on server to handle transfert file between server and client.
5. `sqlite3` to store sync status of files.
6. `vixie-cron` working to automate tasks.

Description
-----------
That utility help to download in a one time fashion remote files/folders to a target directory. It can be quite usefull
for people with *slow bandwith* who want to recover downloaded files from remote location in night for exemple.
The main advantages unlike using bare `rsync` is that every files/folders are tracked by name so they will be not
downloaded again even if you want to move them off the target directory.

How it works
------------
The tasks done of these program are quite simple :
1. List 'files'/'folders' from a remote directory.
2. Loop over list...
    2.1. Check if item has already been retreived fully previously...
        2.1.1 If not then it will download or resume transfert
        2.1.2 Else it will be skipped

If any signal is received (KILL, SIGINT), it will stop downloading.

Automation
----------
Set-up cron properly to run and kill the program at the wanted hours...
Samples are included along to show you how to make things

Install
-------
python2.7 setup.py install (or develop)


FreeBSD users
=============

Additional requirement
----------------------
It seems that the support of sqlite3 isn't bundled within `python-2.7` you may have to install `py-sqlite3` to make it
works.

Locale
------
If you use many foreign char don't forget to customise your `/etc/login.conf`
or `~/.login.conf`
see : https://www.freebsd.org/doc/handbook/using-localization.html
