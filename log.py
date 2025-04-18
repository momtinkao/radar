import logging
from logging.handlers import RotatingFileHandler
import time
from datetime import datetime
import os


class DynamicFileHandler(RotatingFileHandler):
    """
    Custom handler that allows changing the log file name dynamically
    """

    def change_file(self, new_filename):
        """Change the log file name"""
        # Close current file
        try:
            # Close current file
            self.close()

            # Ensure directory exists
            os.makedirs(os.path.dirname(new_filename) or '.', exist_ok=True)

            # Update the base filename
            self.baseFilename = new_filename

            # Create new file with updated name
            self.stream = self._open()
        except Exception as e:
            print(f"Error changing log file: {e}")


def setup_logger(log_dir='logs', max_bytes=0, backup_count=24, level=logging.INFO):
    """
    Set up a logger with rotating file handler

    Parameters:
    - initial_log_file: initial name of the log file
    - max_bytes: maximum size of each log file in bytes
    - backup_count: number of backup files to keep
    - level: logging level
    """
    # Create logger

    # Create logs directory
    os.makedirs(log_dir, exist_ok=True)

    # Generate initial log filename
    initial_log_file = os.path.join(
        log_dir, f'{datetime.now().strftime("%Y-%m-%d %H")}.log')

    logger = logging.getLogger('DynamicRotatingLogger')
    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(message)s'
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


def change_file_by_time(handler, interval_hours=3600):
    """
    Change log file based on time interval

    Parameters:
    - handler: the logging handler
    - base_name: base name for log files
    - interval_seconds: interval in seconds to change files
    """
    while True:
        try:
            time.sleep(interval_hours)
            new_filename = os.path.join(
                'logs',
                f'{datetime.now().strftime("%Y-%m-%d %H")}.log'
            )
            handler.change_file(new_filename)
            print(f"Rotated file to {new_filename}")
        except Exception as e:
            print(f"Error changing file: {e}")
            break

'''
# Example usage
if __name__ == '__main__':
    import threading

    # Set up logger
    logger, handler = setup_logger(
        log_dir='logs',
        max_bytes=0,
        backup_count=24
    )

    try:
        # Start file rotation thread (change file every minute)
        rotation_thread = threading.Thread(
            target=change_file_by_time,
            args=(handler, 60)
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

'''