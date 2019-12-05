import logging
import sys
import uuid
from time import sleep

import flask

import structlog
logger = structlog.get_logger('application')

app = flask.Flask('test')
app.version = '1.0.0'


@app.route("/health", methods=["GET"])
def some_route():
    log = logger.new(request_id=str(uuid.uuid4()))
    log.info("Health", foo=1, bar=2)

    return "health"


def add_app_version(logger, method, event_dict):
    event_dict['app'] = {
        'version': app.version
    }

    return event_dict


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s", stream=sys.stdout)

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            add_app_version,
            structlog.processors.JSONRenderer(sort_keys=True)
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    while True:
        some_route()
        sleep(1)
    # app.run()
