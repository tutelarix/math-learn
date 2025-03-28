import logging
import sys
import time
import traceback
from functools import wraps
from pathlib import Path

__all__ = ["logger", "handle_exception"]


def _get_log_dir():
    logger_module_dir_depth = 2
    log_dir = Path(__file__).parents[logger_module_dir_depth]

    current_script_rel_dir = Path.cwd().relative_to(log_dir)
    # pylint: disable=no-member
    log_dir = log_dir.joinpath("logs", current_script_rel_dir)
    return log_dir


def _get_log_file_path():
    log_dir = _get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    file_name = Path(sys.argv[0]).stem
    log_file_path = log_dir.joinpath(f"log_{current_time}_{file_name}.log")
    return log_file_path


def _set_handlers(logger_param, log_level, handlers):
    for handler in handlers:
        logger_param.addHandler(handler)
    logger_param.setLevel(log_level)

    # There is function logging.shutdown() so that manual remove of handlers isn't required.
    # When the logging module is imported, it registers this function as an exit handler (see atexit),
    # so normally there’s no need to do that manually.


def _create_logger(log_level=logging.DEBUG, log_name=None):
    new_logger = logging.getLogger(log_name)
    new_logger.propagate = True

    # Simple formatter for console
    format_console = logging.Formatter(
        "%(asctime)s; %(levelname)8s;  %(filename)s->%(funcName)s():%(lineno)s:  %(message)s"
    )

    # Complex formatter for the file log
    format_file = logging.Formatter(
        "%(asctime)s; Process: %(process)d %(processName)s; Thread: %(thread)d %(threadName)s; %(levelname)8s;  %(filename)s->%(funcName)s():%(lineno)s:  %(message)s"
    )

    # Prepare stream handler to return log to the stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(format_console)

    # Prepare file handler to save logs in file
    file_handler = logging.FileHandler(_get_log_file_path())
    file_handler.setFormatter(format_file)

    _set_handlers(new_logger, log_level, [console_handler, file_handler])
    return new_logger


# Logger for all scripts
# Set log_name = None to get messages from all packages
logger = _create_logger(logging.DEBUG, "facial_python")


def handle_exception(func):
    """
    Decorator to catch and log exceptions

    :param func: function
    :return: inner decorator function
    """

    @wraps(func)
    def inner_func(*args, **kwargs):
        try:
            returned_value = func(*args, **kwargs)
        except Exception as e:
            logger.critical(f"Got exception in function {func}, exception: {e}")
            logger.critical(traceback.format_exc())

            raise e

        return returned_value

    return inner_func
