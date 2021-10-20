import logging
from os import path
from platform import node as getHostname

default_logging_format = '%(asctime)s:%(levelname)s: %(message)s'
default_logging_file_path = path.dirname(__file__) + '\\' + __name__ +'.log'
default_logging_level = logging.DEBUG
# Custom formatter
class MyFormatter(logging.Formatter):

    #dflt_fmt = '%(asctime)s:%(levelname)s: %(message)s' # use in constructor?  probably can't...
    #err_fmt  = "ERROR: %(msg)s"
    #dbg_fmt  = "DBG: %(module)s: %(lineno)d: %(msg)s"
    info_fmt = '%(asctime)s:%(levelname)s:  %(message)s'

    def __init__(self):
        super().__init__(fmt='%(asctime)s:%(levelname)s: %(message)s', datefmt=None, style='%')  
    
    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.INFO:
            self._style._fmt = MyFormatter.info_fmt
        # No other custom formats necessary right now.
        #elif record.levelno == logging.DEBUG:
        #    self._style._fmt = MyFormatter.dbg_fmt
        #
        #elif record.levelno == logging.ERROR:
        #    self._style._fmt = MyFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result
logger = logging.getLogger(__name__)
# Sapping formatter with custom class which allows to alter formatting depending on log level
#formatter = logging.Formatter(default_logging_format)
formatter = MyFormatter()
def configureLogging(logFilePath=default_logging_file_path, logLevel=default_logging_level):
    logger.setLevel(logLevel)
    file_handler = logging.FileHandler(logFilePath)
    #file_handler.setLevel(default_logging_level) # necessary? might not be since already did logger.setLevel()
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def _log_DEBUG(msg):
    logger.debug(msg)

def _log_INFO(msg):
    logger.info(msg)

def _log_WARNING(msg):
    logger.warning(msg)

def _log_ERROR(msg):
    logger.error(msg)

def _log_CRITICAL(msg):
    logger.critical(msg)

logging_function_switch = {
    10        : _log_DEBUG,
    "DEBUG"   : _log_DEBUG,
    20        : _log_INFO,
    "INFO"    : _log_INFO,
    30        : _log_WARNING,
    "WARNING" : _log_WARNING,
    40        : _log_ERROR,
    "ERROR"   : _log_ERROR,
    50        : _log_CRITICAL,
    "CRITICAL": _log_CRITICAL,
}

def log(string="", logging_level="DEBUG"):
    try: logging_function_switch.get(logging_level, logging.WARNING)(string)
    except: print("Logging failed")