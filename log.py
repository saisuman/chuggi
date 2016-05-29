import logging

_FORMAT = '%(asctime)-15s %(filename)s %(funcName)-8s %(message)s'
logging.basicConfig(format=_FORMAT, level=10)

LOGGER = logging.getLogger('command_processor')
