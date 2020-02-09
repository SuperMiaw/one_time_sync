import os

import sqlite3
from enum import Enum


class Revision(Enum):
    """Existing database version"""
    none = -1
    v0 = 0
    v1 = 1


class Context:
    """Define how to connect to database and manage upgrades"""

    def __init__(self, config):
        """Define how to connect to database and manage upgrades
        :type config: `~app.Configuration`
        """
        self._path = config.database_file
        self._conn = None

    @property
    def path(self):
        """Indicate where is stored database (sqlite)"""
        return self._path

    @property
    def conn(self):
        """Connection to current database
        :rtype: sqlite3.Connection
        """
        if self._conn is None:
            self._conn = sqlite3.connect(self.path)

        return self._conn

    def get_version(self):
        """Guesss which version is used for the sofware database"""
        if not os.path.exists(self.path):
            print("Context: Database not found !")
            return Revision.none

        c = self.conn.cursor()
        c.execute("SELECT EXISTS"
                  "("
                  " SELECT NULL "
                  " FROM sqlite_master "
                  " WHERE type='table' "
                  "  AND name='history'"
                  ")")
        history_exist = c.fetchone()[0]
        c.close()

        if not history_exist:
            return Revision.v0

        return self._get_max_revision()

    def upgrade(self, version):
        """Apply incremental upgrade to the current database (if required)
        :param version:
        """
        if version == Revision.none:
            print "upgrade: %s to %s" % (version, Revision.v0)

            self.conn.execute("CREATE TABLE syncedRemoteHostFiles"
                              "("
                              "  filename VARCHAR NOT NULL,"
                              "  exist BOOLEAN NOT NULL DEFAULT 1"
                              ")")
            self.conn.commit()
            version = Revision.v0

        if version == Revision.v0:
            print "upgrade: %s to %s" % (version, Revision.v1)

            self.conn.execute("ALTER TABLE syncedRemoteHostFiles RENAME TO synced_remote_file")
            self.conn.execute("CREATE TABLE history"
                              "("
                              "  revision INT NOT NULL, "
                              "  comment TEXT NOT NULL"
                              ")")
            self._add_version(Revision.v1, "Introducing maintenance table. Change table naming convention.")
            self.conn.commit()
            version = Revision.v1

    def _get_max_revision(self):
        c = self.conn.cursor()
        c.execute("SELECT MAX(revision) FROM history")
        max_rev = (c.fetchone())[0]
        c.close()

        return Revision(max_rev)

    def _add_version(self, version, comment):
        self.conn.execute("INSERT INTO history(revision, comment) VALUES(?,?)", (version.value, comment))
        self.conn.commit()


class Access(object):
    """Template used for database access classes"""

    def __init__(self, context):
        """
        :type context: Context
        :return:
        """
        version = context.get_version()
        context.upgrade(version)

        self.context = context

    @property
    def conn(self):
        """Open connection to current database
        :return
        """
        return self.context.conn


class FileHistoryAccess(Access):
    """Manage sync files status"""

    def __init__(self, context):
        super(FileHistoryAccess, self).__init__(context)
        self.conn.execute("UPDATE synced_remote_file SET exist=0")
        self.conn.commit()

    def is_synced(self, filename):
        """Check if a file is synced, each time called the filename is tagged as existing"""
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM synced_remote_file WHERE filename=?", (filename,))
        match_count = (c.fetchone())[0]
        c.close()

        if match_count > 0:
            self.conn.execute('UPDATE synced_remote_file SET exist=1 WHERE filename=?', (filename,))
            self.conn.commit()
            return True
        else:
            return False

    def set_synced(self, filename):
        """Tag a file as synced
        :param filename:
        """
        self.conn.execute('INSERT INTO synced_remote_file(filename) VALUES(?)', (filename,))
        self.conn.commit()

    def cleanup(self):
        """Delete non existing files from database"""
        self.conn.execute('DELETE FROM synced_remote_file WHERE exist=0')
        self.conn.commit()

