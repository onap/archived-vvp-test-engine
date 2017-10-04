import logging


class LoggingServiceFactory(object):
    __logger = None

    def __init__(self):
        if self.__logger is None:
            self.__set_logger()

    @classmethod
    def __set_logger(cls):
        if cls.__logger is None:
            cls.__logger = logging.getLogger('vvp-ci.logger')

    @classmethod
    def get_logger(cls):
        if cls.__logger is None:
            cls.__set_logger()
        return cls.__logger
