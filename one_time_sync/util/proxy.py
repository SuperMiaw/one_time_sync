import subprocess

import paramiko


# FIXME Encoding problem happening when trying to call '_escape_quote' ('_source_dir' and '_target_dir')
class RemoteHost:
    """Run commands on remote host"""
    def __init__(self, config):
        """Run commands on remote host over SSH
        :type config: `~app.Configuration`
        """
        self._source_username = config.src_username
        self._source_hostname = config.src_host
        self._source_dir = config.src_dir
        self._target_dir = config.tgt_dir
        self._is_verbose = config.verbose

        self._process = None

    @property
    def process(self):
        """Retrieve background process that is used for fetching files"""
        return self._process

    def get_filenames(self):
        """Retrieve files and folders names from remote host"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(self._source_hostname, username=self._source_username)

        cmd_ls = "ls {path}".format(path=self._source_dir)
        stdin, stdout, stderr = ssh.exec_command(cmd_ls)

        if self._is_verbose:
            print('exec (over ssh) : %s' % cmd_ls)

        remote_file_names = [filename.strip("\n") for filename in stdout.readlines()]
        ssh.close()

        return remote_file_names

    def retrieve_file(self, filename):
        """Attempt to retrieve one file or folder from remote host
        :param filename: filename or folder to retrieve
        """

        # noinspection PyListCreation
        cmd = ["rsync"]
        # Uncomment this line if your target directory or machine is listening on a port other than 22.
        # cmd.append("--rsh=ssh -p22222")

        # REMOTE SHELL - CONFIG
        cmd.append('-e')
        cmd.append('/usr/bin/ssh -q')

        if self._is_verbose:
            cmd.append("--verbose")
            cmd.append("--progress")

        cmd.append("--chmod=755")
        # cmd.append("--perms")
        cmd.append("--delay-updates")
        cmd.append("--recursive")

        # TODO Escape properly specials chars like double quote (doesn't seems to work with source_dir and target_dir)
        # source directory ARG
        cmd.append("{user}@{host}:'{directory}/{filename}'".format(
                user=self._source_username,
                host=self._source_hostname,
                directory=self._source_dir,
                filename=self._escape_quote(filename)
        ))

        # destination directory ARG
        cmd.append("{path}/".format(
                path=self._target_dir
        ))

        if self._is_verbose:
            print("exec : %s" % " ".join(cmd))

        self._process = subprocess.Popen(cmd, shell=False)

        if self._process.wait() == 0:
            self._process = None
            return True
        else:
            self._process = None
            return False

    @staticmethod
    def _escape_quote(name):
        """Escape single quote char to avoid broken directory and filename path
        :param name:
        :return:
        """
        return name.replace("'", "'\\''")


# Bootstrapping
# NOTE There is a bug with 'paramiko' when log_to_file isn't set
paramiko.util.log_to_file("/dev/null", paramiko.util.logging.FATAL)
