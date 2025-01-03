import os
import sys
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
    """
    def on_created(self, event):
        if event.is_directory:
            logger.info(f"Directory created: {event.src_path}")
        else:
            logger.info(f"File created: {event.src_path}")

    def on_modified(self, event):
        if event.is_directory:
            logger.info(f"Directory modified: {event.src_path}")
        else:
            logger.info(f"File modified: {event.src_path}")

    def on_deleted(self, event):
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

    # Configure logging to file if specified
    if args.logfile:
        file_handler = logging.FileHandler(args.logfile)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

    directory_to_monitor = args.directory

    # Validate the directory
    if not os.path.exists(directory_to_monitor):
        logger.error(f"Directory does not exist: {directory_to_monitor}")
        sys.exit(1)
    if not os.path.isdir(directory_to_monitor):
        logger.error(f"Path is not a directory: {directory_to_monitor}")
        sys.exit(1)

    logger.info(f"Starting to monitor directory: {directory_to_monitor}")
    logger.info(f"Recursive monitoring: {'enabled' if args.recursive else 'disabled'}")

    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_monitor, recursive=args.recursive)

    try:
        observer.start()
        logger.info("Monitoring started. Press Ctrl+C to stop.")
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Stopping monitoring.")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()