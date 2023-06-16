"""Utilities related to logging."""
from datetime import datetime

def log(message: str, file_path: str = None):
    """
    Write a log message to a file or print it to the console.

    Args:
        file_path (str): The path to the log file. If None, the message will be printed to the console.
        message (str): The log message to write.

    Note:
        If file_path is provided, the log file is opened in append mode and the log message is printed to the console.
        If file_path is None, the log message is printed to the console.
    """

    timestamp = datetime.now().strftime('%d-%m-%Y-%H-%M')
    log_message = f"Timestamp {timestamp}: {message}"

    if file_path is not None:
        with open(file_path, mode="a", encoding="utf-8") as file:
            file.write(log_message)
            file.write("\n")

       
    print(log_message)
    print("_" * 50)