import os
import json
import logging.config

import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)


def setup_logging(
    default_path="logging.json", default_level=logging.INFO, env_key="LOG_CFG"
):
    """
    Setup logging configuration
    """
    sentry_sdk.init(
        "https://c6def2d3c54745ada097c34bb2a30263@o424226.ingest.sentry.io/5434056",
        traces_sample_rate=1.0,
        integrations=[AioHttpIntegration(), sentry_logging],
    )
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
