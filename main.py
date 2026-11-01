import os
import sys
import time
import logging
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FileChangeHandler(FileSystemEventHandler):
    """
    Handles file system events such as file creation, modification, and deletion.
    Events for the log file itself are excluded, so a log file placed
    inside the monitored directory never reports itself.
    """
    def __init__(self, excluded_path=None):
        super().__init__()
        self.excluded_path = os.path.realpath(excluded_path) if excluded_path else None

    # The comparison resolves the event path fresh on every
    # event. Watchdog hands me paths in the spelling of the
    # directory argument I was scheduled with, and realpath is
    # what brings the two spellings together, at the cost of a
    # filesystem lookup per event in a busy directory.
    def _is_excluded(self, event):
        return self.excluded_path and os.path.realpath(event.src_path) == self.excluded_path

    # There is no on_moved in this handler, and watchdog reports
    # renames as move events, not as a delete plus a create. A
    # file renamed into the watched directory, out of it, or
    # within it is therefore invisible to me, which is a real
    # gap for a monitor whose subject is file changes: the
    # cheapest way to place a file here leaves no trace in my log.
    def on_created(self, event):
        if self._is_excluded(event):
            return
        if event.is_directory:
            logger.info(f"Directory created: {event.src_path}")
        else:
            logger.info(f"File created: {event.src_path}")

    def on_modified(self, event):
        if self._is_excluded(event):
            return
        if event.is_directory:
            logger.info(f"Directory modified: {event.src_path}")
        else:
            # One save from an editor often arrives as several modified
            # events, and I log every one of them. There is no settling
            # window and no coalescing, so my log counts event bursts,
            # not saves, and a reader counting lines overstates how
            # often a file really changed.
            logger.info(f"File modified: {event.src_path}")

    def on_deleted(self, event):
        if self._is_excluded(event):
            return
        if event.is_directory:
            logger.info(f"Directory deleted: {event.src_path}")
        else:
            logger.info(f"File deleted: {event.src_path}")

def setup_argparse():
    """
    Set up command-line argument parsing.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Monitors specified directories for file changes (creation, modification, deletion)."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Directory to monitor for file changes."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Monitor directories recursively."
    )
    parser.add_argument(
        "--logfile",
        type=str,
        default=None,
        help="Optional log file to write monitoring events."
    )
    return parser.parse_args()

def main():
    """
    Main function to monitor file changes in the specified directory.
    """
    args = setup_argparse()

    directory_to_monitor = args.directory

    # Validate the directory before building any log file handler
    if not os.path.exists(directory_to_monitor):
        logger.error(f"Directory does not exist: {directory_to_monitor}")
        sys.exit(1)
    if not os.path.isdir(directory_to_monitor):
        logger.error(f"Path is not a directory: {directory_to_monitor}")
        sys.exit(1)

    # Configure logging to file if specified
    if args.logfile:
        watched_resolved = os.path.realpath(directory_to_monitor)
        logfile_resolved = os.path.realpath(args.logfile)
        if logfile_resolved == watched_resolved or logfile_resolved.startswith(watched_resolved + os.sep):
            logger.warning(f"Warning: log file {args.logfile} is inside the monitored directory; events for the log file itself will be excluded.")
        try:
            file_handler = logging.FileHandler(args.logfile)
        except OSError as e:
            logger.error(f"Error: could not open log file '{args.logfile}': {e}")
            sys.exit(1)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

    logger.info(f"Starting to monitor directory: {directory_to_monitor}")
    logger.info(f"Recursive monitoring: {'enabled' if args.recursive else 'disabled'}")

    event_handler = FileChangeHandler(excluded_path=args.logfile)
    observer = Observer()
    # I never reconcile what is on disk against anything. A
    # change made while this process is not running is simply
    # not part of my record, and there is no startup scan that
    # would notice the directory differs from when I last ran.
    observer.schedule(event_handler, directory_to_monitor, recursive=args.recursive)

    try:
        observer.start()
        logger.info("Monitoring started. Press Ctrl+C to stop.")
        while True:
            # Death is detected by polling once a second inside the same
            # loop that sleeps, so a dead observer and a healthy one look
            # identical for up to a second, and the exit that follows is
            # the only signal: nothing distinguishes a monitor that
            # stopped from one still running unless this error line
            # was written.
            if not observer.is_alive():
                logger.error("Monitoring stopped: the observer is no longer running.")
                sys.exit(1)
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping monitoring.")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()