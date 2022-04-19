[global]
database_file = string()
lock_file = string()
verbose = boolean(default=False)

[source]
username = string()
host = string()
directory = string()

[target]
directory = string()

[deluge]
enabled = boolean(default=False)
host = string()
port = integer(default=58846)
username = string()
password = string()
max_upload_speed = float(default=-1)
