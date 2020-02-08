import pytest

from tkimgloader import project_logger

def test_logging():
    project_logger.setup_logger(R'tkimgloader\logs\test_log.txt')
    project_logger.test_logging()
