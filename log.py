import logging
from logging.handlers import RotatingFileHandler
import time
from datetime import datetime


class DynamicFileHandler(RotatingFileHandler):
    """
    Custom handler that allows changing the log file name dynamically
    """

    def change_file(self, new_filename):
        """Change the log file name"""
        # Close current file
        self.close()

        # Update the base filename
        self.baseFilename = new_filename

        # Create new file with updated name
        self.stream = self._open()


def setup_logger(initial_log_file='app.log', max_bytes=0, backup_count=24, level=logging.INFO):
    """
    Set up a logger with rotating file handler

    Parameters:
    - initial_log_file: initial name of the log file
    - max_bytes: maximum size of each log file in bytes
    - backup_count: number of backup files to keep
    - level: logging level
    """
    # Create logger
    logger = logging.getLogger('DynamicRotatingLogger')
    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create handler
    handler = DynamicFileHandler(
        filename=initial_log_file,
        mode='a+',
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )

    # Add formatter to handler
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger, handler


def change_file_by_time(handler, interval_hours=30):
    """
    Change log file based on time interval

    Parameters:
    - handler: the logging handler
    - base_name: base name for log files
    - interval_seconds: interval in seconds to change files
    """
    while True:
        try:
            # Create new filename with timestamp
            new_filename = f'{datetime.now().strftime("%Y-%m-%d %H")}.log'
            handler.change_file(new_filename)
            time.sleep(interval_hours)
        except Exception as e:
            print(f"Error changing file: {e}")
            break


# Example usage
if __name__ == '__main__':
    import threading

    # Set up logger
    logger, handler = setup_logger(
        initial_log_file="{}.log".format(
            datetime.now().strftime("%Y-%m-%d %H")),
        max_bytes=0,
        backup_count=24
    )

    try:
        # Start file rotation thread (change file every minute)
        rotation_thread = threading.Thread(
            target=change_file_by_time,
            args=(handler, 1)
        )
        rotation_thread.start()

        # Simulate logging
        logger.info('Starting logging with time-based file changes')

        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f'Log entry at {current_time}')
            time.sleep(1)  # Log every second

    except KeyboardInterrupt:
        print('Logging stopped')

# Alternative usage without threading


def manual_file_change_example():
    logger, handler = setup_logger('app.log')

    try:
        while True:
            # Log for a minute
            for _ in range(60):
                logger.info('Log message')
                time.sleep(1)

            # Change file after a minute
            new_filename = f'app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
            handler.change_file(new_filename)
            logger.info(f'Changed to new file: {new_filename}')

    except KeyboardInterrupt:
        print('Logging stopped')
