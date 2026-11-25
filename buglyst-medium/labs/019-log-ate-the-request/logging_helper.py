"""Request logging helpers."""

import logging

logger = logging.getLogger("upload")


def log_upload(body: bytes) -> None:
    logger.debug("upload received body=%s", body)
