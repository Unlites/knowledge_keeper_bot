from logging import StreamHandler, Formatter
import sys
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_handler = StreamHandler(stream=sys.stdout)
log_handler.setFormatter(Formatter(fmt='%(asctime)s: %(levelname)s %(message)s'))
logger.addHandler(log_handler)