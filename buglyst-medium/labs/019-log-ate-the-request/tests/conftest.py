import logging

import pytest
from django.test import Client


@pytest.fixture()
def client():
    return Client()


@pytest.fixture()
def capture_upload_logs():
    logger = logging.getLogger("upload")
    records: list[logging.LogRecord] = []

    class _Handler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            records.append(record)

    handler = _Handler()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    try:
        yield records
    finally:
        logger.removeHandler(handler)
