from os import path
from pathlib import Path


LOG_DIR = Path("./logs")


def read_log_file(filename: str) -> str:
    """
    Read a log file and return its content.
    """

    filepath = LOG_DIR / filename

    if not path.exists(filepath):
        return f"Log file {filename} does not exist"

    with open(filepath) as f:
        return f.read()


def search_log_file(filename: str, search_term: str) -> str:
    """
    Search for a term in a log file and return the matching lines.
    """

    filepath = LOG_DIR / filename

    if not path.exists(filepath):
        return f"Log file {filename} does not exist"

    with open(filepath) as f:
        log_lines = f.readlines()
        matching_lines = [line for line in log_lines if search_term in line]
        return "".join(matching_lines)


def head_log_file(filename: str, lines: int = 10) -> str:
    """
    Read the first N lines of a log file and return its content.
    """

    filepath = LOG_DIR / filename

    if not path.exists(filepath):
        return f"Log file {filename} does not exist"

    with open(filepath) as f:
        log_lines = f.readlines()
        return "".join(log_lines[:lines])


def tail_log_file(filename: str, lines: int = 10) -> str:
    """
    Read the last N lines of a log file and return its content.
    """

    filepath = LOG_DIR / filename

    if not path.exists(filepath):
        return f"Log file {filename} does not exist"

    with open(filepath) as f:
        log_lines = f.readlines()
        return "".join(log_lines[-lines:])


def read_errors_log_file(filename: str) -> str:
    """
    Read a log file and return only the lines that contain errors.
    """

    filepath = LOG_DIR / filename

    if not path.exists(filepath):
        return f"Log file {filename} does not exist"

    with open(filepath) as f:
        log_lines = f.readlines()
        error_lines = [
            line for line in log_lines if "ERROR" in line or "Exception" in line
        ]
        return "".join(error_lines)


def count_log_lines(filename: str) -> int:
    """
    Count the number of lines in a log file and return the count.
    """

    filepath = LOG_DIR / filename

    if not path.exists(filepath):
        return 0

    with open(filepath) as f:
        log_lines = f.readlines()
        return len(log_lines)
