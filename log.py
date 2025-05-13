import logging
from logging.handlers import RotatingFileHandler
import time
from datetime import datetime, timedelta
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
    - log_dir: directory for log files
    - max_bytes: maximum size of each log file in bytes (0 for no rotation by size)
    - backup_count: number of backup files to keep (if max_bytes > 0)
    - level: logging level
    """
    # Create logs directory
    os.makedirs(log_dir, exist_ok=True)

    # Generate initial log filename based on the current hour (整點)
    now = datetime.now()
    initial_log_file = os.path.join(
        log_dir, f'{now.strftime("%Y-%m-%d %H")}.log')

    logger = logging.getLogger('DynamicRotatingLogger')
    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(message)s'
    )

    # Create handler
    # Note: max_bytes and backup_count from RotatingFileHandler are less relevant
    # if we are primarily rotating based on time by changing the filename.
    # If max_bytes is set to 0, size-based rotation is disabled.
    handler = DynamicFileHandler(
        filename=initial_log_file,
        mode='a+',
        maxBytes=max_bytes, # 設定為 0 以禁用基於大小的輪替，如果主要依賴時間
        backupCount=backup_count,
        encoding='utf-8'
    )

    # Add formatter to handler
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger, handler


def change_file_by_time(handler, log_dir='logs'):
    """
    Change log file at the beginning of every hour.

    Parameters:
    - handler: the logging handler
    - log_dir: directory for log files
    """
    while True:
        try:
            now = datetime.now()
            # 計算下一個整點
            next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            
            # 計算到下一個整點的秒數
            wait_seconds = (next_hour - now).total_seconds()
            
            print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}. Waiting for {wait_seconds:.0f} seconds until next hour ({next_hour.strftime('%Y-%m-%d %H')}:00:00) for log rotation.")
            time.sleep(wait_seconds)
            
            # 到達整點，準備新的檔案名稱
            new_filename_time = datetime.now() # 應該非常接近 next_hour
            new_filename = os.path.join(
                log_dir,
                f'{new_filename_time.strftime("%Y-%m-%d %H")}.log'
            )
            handler.change_file(new_filename)
            print(f"Rotated log file to {new_filename} at {new_filename_time.strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            print(f"Error in change_file_by_time: {e}")
            # 發生錯誤時，等待一段時間再試，避免快速連續失敗
            time.sleep(60)
        except KeyboardInterrupt:
            print("Log rotation thread stopped by user.")
            break


if __name__ == '__main__':
    import threading

    # 設定日誌
    logger, handler = setup_logger(
        log_dir='logs_test', # 使用測試目錄
        max_bytes=0,      # 禁用基於大小的輪替，主要依賴時間
        backup_count=0    # 如果 max_bytes 為 0，此參數無效
    )

    try:
        # 啟動日誌檔案輪替執行緒
        rotation_thread = threading.Thread(
            target=change_file_by_time,
            args=(handler, 'logs_test'), # 傳遞日誌目錄
            daemon=True # 設置為守護執行緒，這樣主程式結束時它也會結束
        )
        rotation_thread.start()

        logger.info('開始記錄，日誌檔案將在每個整點更新。')
        print("主程式開始記錄，按 Ctrl+C 停止。")

        count = 0
        while True:
            current_time_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f'日誌記錄 {count} at {current_time_log}')
            count += 1
            time.sleep(10) # 每 10 秒記錄一次

    except KeyboardInterrupt:
        print('主程式記錄停止。')
