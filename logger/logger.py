from logging import StreamHandler, Formatter
import sys
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

log_handler = StreamHandler(stream=sys.stdout)
log_handler.setFormatter(Formatter(fmt='%(asctime)s: %(levelname)s %(message)s'))
log.addHandler(log_handler)