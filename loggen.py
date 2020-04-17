import time
import random
import uuid
import logging
import structlog
from logitems import CreateLogItem


structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logging.basicConfig(
    format="%(message)s", level=logging.INFO, filename="./struct.log", filemode="w"
)

logger = structlog.get_logger()


if __name__ == "__main__":
    logitems = CreateLogItem()

    while True:
        item = logitems.create_random_log_item()
        log = logger.bind(**item.fields)
        getattr(log, item.level)(item.event)

        time.sleep(1)
