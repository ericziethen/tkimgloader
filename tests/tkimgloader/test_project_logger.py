import os

from tkimgloader import project_logger


def test_logging():
    log_dir = R'tkimgloader\logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    project_logger.setup_logger(R'tkimgloader\logs\test_log.txt')
    project_logger.test_logging()
