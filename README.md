One Time Sync
=============

Requirement
-----------
1. `python3` for making this program works.
2. `open-ssh` set up on client and on remote server to set-up secure channels.
3. `keychain` set up in background (or any other ssh-agent ?) to manage identification and authentication by rsa keys.
4. `rsync` (>= 3.2.4) on client and on server to handle transfert file between server and client.
5. `sqlite3` to store sync status of files.
6. `vixie-cron` working to automate tasks.

Description
-----------
That utility help to download in a one-way fashion remote files/folders to a target directory.<br/>
The main advantages over bare `rsync` is that every files/folders will only be downloaded once even if they are move out of target directory.<br/>

If any signal is received (KILL, SIGINT), it will stop downloading. Partially downloaded files or folder will be resumed on next start.

Can optionally throttle temporaly deluge to ensure faster file retrieval.

Automation
----------
- Set-up cron properly to run and kill the program at the wanted hours.
- Samples are included along side to demonstrate usage.

Install
-------
```bash
python3 setup.py install # (or develop)
````

FreeBSD users
=============

- The support of `sqlite3` isn't bundled within `python3` you will also need to install `py-sqlite3`.
- Ensure local are properly configured on client and server side. Hint : Customize your `/etc/login.conf` or `~/.login.conf`.<br/>See: https://www.freebsd.org/doc/handbook/using-localization.html
