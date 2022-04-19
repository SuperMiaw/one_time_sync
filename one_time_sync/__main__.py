import argparse
import os
import signal
import sys
import traceback

from one_time_sync.util import db, client
from one_time_sync.util.app import Config


def main():
    """Run the whole program"""

    # ARGS
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configuration",
                        help="specify configuration file",
                        action="store",
                        required=True)
    args = parser.parse_args()

    # CONFIG FILE
    #
    cfg = Config(path=args.configuration)

    # LOCALE
    #
    if sys.stdout.encoding is None:
        print("Encoding for output seems missing... ", file=sys.stderr)
        "You should set env variable PYTHONIOENCODING=UTF-8. "
        "Example: running 'export PYTHONIOENCODING=UTF-8' before calling this program"
        exit(1)

    # PID LOCK
    #
    pid = str(os.getpid())

    if os.path.isfile(cfg.lock_file):
        if cfg.verbose:
            print("Lock file found (%s), canceling synchronisation..." % cfg.lock_file)
        sys.exit()
    else:
        if cfg.verbose:
            print("Starting synchronisation...")
            print("Creating lock file (%s)" % cfg.lock_file)
        with open(cfg.lock_file, 'w') as f:
            f.write(pid)

    # EXIT HANDLER
    #
    remote = None

    def handler(signum=None, frame=None):
        print("Exiting...")
        print(remote)

        if remote.process is not None:
            try:
                remote.process.terminate()
            except:
                print("Rsync subprocess interrupted")

        os.unlink(cfg.lock_file)
        exit(0)

    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sig, handler)

    # MAIN LOOP
    #
    try:
        remote = client.RemoteFileSystem(cfg)
        deluge = client.Deluge(cfg)
        context = db.Context(cfg)
        file_history = db.FileHistoryAccess(context)

        for filename in remote.get_filenames():
            if not file_history.is_synced(filename):
                limit_applied = deluge.set_max_upload_speed(cfg.deluge_max_upload_speed)
                if limit_applied and cfg.verbose:
                    print("Deluge: Apply max upload speed.")
                print("Trying to fetch : %s" % filename)
                sync_succeed = remote.retrieve_file(filename)
                if sync_succeed:
                    file_history.set_synced(filename)
                    print("SUCCESS !")
                else:
                    print("!! ERROR !! Cannot fetch '" + filename + "' (Skipped)")
            elif cfg.verbose:
                print("File flagged as synchronised")
                print("skipping : %s" % filename)

        if cfg.verbose:
            print("Synchronisation ended")
            print("Cleaning database")

        file_history.cleanup()
    except:
        print("Fatal error")
        traceback.print_exc()
    finally:
        if deluge is not None:
            limit_applied = deluge.unset_max_upload_speed()
            if limit_applied and cfg.verbose:
                print("Deluge: unset max upload speed.")

    if os.path.isfile(cfg.lock_file):
        if cfg.verbose:
            print("Removing lock file (%s)" % cfg.lock_file)

        os.unlink(cfg.lock_file)

    exit(0)


if __name__ == '__main__':
    main()
