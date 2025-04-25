import logging

logger = logging.getLogger('valentine bot logger')
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(console_handler)
logger.info('sex must die')
