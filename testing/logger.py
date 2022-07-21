from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from testing.end_to_end.browser.browsers import TestsBrowser

import logging
from time import time
import shutil
import os
from tempfile import TemporaryDirectory
import pytz
from datetime import datetime


class Logger:
    create_dump: bool
    dir_path: str
    paths: dict
    file: Logger
    console: Logger
    level: int = logging.WARNING

    def __init__(self, dir_path: str = None) -> None:
        self.create_dump = False
        if dir_path is None:
            return
        self.dir_path = dir_path
        self.paths = self.paths(self.dir_path)
        self.file = self.create_file_logger(self.dir_path)
        self.console = self.create_console_logger()
        self.level = self.file.level

    def init_logger(self, dir_path: str) -> None:
        """used when the initiation needs to be delayed
        typically due to global variables not being set yet"""
        print(f"type(tmpdir): {type(dir_path)}")
        self.dir_path = dir_path
        self.paths = self.paths(self.dir_path)
        self.file = self.create_file_logger(self.dir_path)
        self.console = self.create_console_logger()
        self.level = self.file.level

    def create_file_logger(self, dir_path: str) -> logging.Logger:
        """
        creates a logger that writes to a file in the temporary directory

        :param tmpdir: The directory where the log file will be created
        """
        logger = logging.getLogger("FILE")
        logger.setLevel(os.environ.get("LOG_LEVEL"))
        path = os.path.join(dir_path, "dump.log")
        handler = logging.FileHandler(path, "a")
        format = logging.Formatter("[%(levelname)s]%(message)s")
        handler.setFormatter(format)
        logger.addHandler(handler)
        return logger

    def create_console_logger(self) -> logging.Logger:
        logger = logging.getLogger("CONSOLE")
        logger.setLevel(os.environ.get("LOG_LEVEL"))
        handler = logging.StreamHandler()
        format = logging.Formatter("[%(levelname)s]%(message)s")
        handler.setFormatter(format)
        logger.addHandler(handler)
        return logger

    def make_paths(self) -> None:
        if not os.path.exists(self.paths["logs"]):
            os.makedirs(self.paths["logs"])
        if not os.path.exists(self.paths["dir_date"]):
            os.makedirs(self.paths["dir_date"])

    def set_create_dump(self, level: int) -> None:
        if self.create_dump is False and not self.level > level:
            self.create_dump = True

    def _log(
        self,
        level: int,
        message: str,
        to_console: str,
        exc_info: bool,
        exc_to_console: bool,
    ):
        """
        Logs with the given level

        :param message: The message to log
        :param to_console: Message to be printed to the console (optional)
        :param exc_info: If True, Exception info is added to the logging message, defaults to False
        :param exc_to_console: If True, the exception will be printed to the console, defaults to False
        """
        self.set_create_dump(level)
        self._to_file(message, level, exc_info)
        if to_console is not None or exc_to_console:
            self._to_console(to_console, level, exc_to_console)

    def _to_file(self, message: str, level: int, exc_info: bool = False):
        self.set_create_dump(level)
        self.file.log(level=level, msg=message, exc_info=exc_info)

    def _to_console(self, message: str, level: int, exc_to_console: bool):
        self.console.log(level=level, msg=message, exc_info=exc_to_console)

    def debug(
        self,
        message: str,
        to_console: str = None,
        exc_info: bool = False,
        exc_to_console: bool = False,
    ):
        """
        Logs with the level DEBUG

        :param message: The message to log
        :param to_console: Message to be printed to the console (optional)
        :param exc_info: If True, Exception info is added to the logging message, defaults to False
        :param exc_to_console: If True, the exception will be printed to the console, defaults to False
        """
        self._log(logging.DEBUG, message, to_console, exc_info, exc_to_console)

    def info(
        self,
        message: str,
        to_console: str = None,
        exc_info: bool = False,
        exc_to_console: bool = False,
    ):
        """
        Logs with the level INFO

        :param message: The message to log
        :param to_console: Message to be printed to the console (optional)
        :param exc_info: If True, Exception info is added to the logging message, defaults to False
        :param exc_to_console: If True, the exception will be printed to the console, defaults to False
        """
        self._log(logging.INFO, message, to_console, exc_info, exc_to_console)

    def warning(
        self,
        message: str,
        to_console: str = None,
        exc_info: bool = False,
        exc_to_console: bool = False,
    ):
        """
        Logs with the level WARNING

        :param message: The message to log
        :param to_console: Message to be printed to the console (optional)
        :param exc_info: If True, Exception info is added to the logging message, defaults to False
        :param exc_to_console: If True, the exception will be printed to the console, defaults to False
        """
        self._log(logging.WARNING, message, to_console, exc_info, exc_to_console)

    def error(
        self,
        message: str,
        to_console: str = None,
        exc_info: bool = False,
        exc_to_console: bool = False,
    ):

        """
        Logs with the level ERROR

        :param message: The message to log
        :param to_console: Message to be printed to the console (optional)
        :param exc_info: If True, Exception info is added to the logging message, defaults to False
        :param exc_to_console: If True, the exception will be printed to the console, defaults to False
        """
        self._log(logging.ERROR, message, to_console, exc_info, exc_to_console)

    def critical(
        self,
        message: str,
        to_console: str = None,
        exc_info: bool = False,
        exc_to_console: bool = False,
    ):
        """
        Logs with the level CRITICAL

        :param message: The message to log
        :param to_console: Message to be printed to the console (optional)
        :param exc_info: If True, Exception info is added to the logging message, defaults to False
        :param exc_to_console: If True, the exception will be printed to the console, defaults to False
        """
        self._log(logging.CRITICAL, message, to_console, exc_info, exc_to_console)

    def screencap(self, browser: TestsBrowser, img_name: str = None, folder: str = ""):
        """
        It takes a screenshot of the browser and saves it to a folder

        :param browser: the browser to take a screenshot with
        :param img_name: The filename the image will be saved under
        :param folder: The folder to save the screenshot in. this will be appended to the root path
        """
        path = self.paths["tmp_screenshots"]
        if folder != "":
            path = os.path.join(path, folder)
        if not os.path.exists(os.path.abspath(path)):
            os.makedirs(os.path.abspath(path))
        if img_name is None:
            img_name = browser.name
        strtime = "".join(c if c.isalnum() else "" for c in str(time()))
        img_name += f"_{strtime}.png"
        browser.get_screenshot_as_file(os.path.abspath(os.path.join(path, img_name)))

    def dump_vars(self, locals: dict, globals: dict, others: dict[dict] = {}) -> None:

        border = "=" * 75
        dump = "\n" + border + "\nLOCAL VARIABLES:"
        for k, v in locals.items():
            dump += f"\n{k}: {v}"
        dump += "\nGLOBAL VARIABLES:"
        for k, v in globals.items():
            dump += f"\n{k}: {v}"
        for name, value in others.items():
            pass
            name: str
            value: dict
            dump += f"\n{name.upper()}:"
            for k, v in value.items():
                dump += f"\n{k}: {v}"
        try:
            self.file.debug(dump)
        except Exception as e:
            print(e)
            # This is here because attempting to log some characters will cause a traceback
            self.file.error("Unable to dump vars", exc_info=True)

    def commit(self, tmpdir: TemporaryDirectory):
        """
        creates a permanent directory and copies the contents of the tmpdir to it.

        :param tmpdir: the TemporaryDirectory
        """
        if self.create_dump is True:
            self.make_paths()
            shutil.copytree(tmpdir, self.paths["dir_time"])

    @staticmethod
    def paths(tmpdir: TemporaryDirectory) -> dict:
        """Creates the subdirectories inside of the temporary directory"""
        root = os.path.dirname(__file__) + os.environ.get("LOG_FILE_DIR")
        local: datetime = pytz.timezone(os.environ.get("TIMEZONE")).localize(
            datetime.now()
        )
        date = str(local.date())
        time = str(local.hour) + "_" + str(local.minute) + "_" + str(local.second)
        os.mkdir(os.path.join(tmpdir, "screenshots"))
        return {
            "logs": os.path.abspath(root),
            "dir_date": os.path.abspath(os.path.join(root, date)),
            "dir_time": os.path.abspath(os.path.join(root, date, time)),
            # "file": os.path.abspath(os.path.join(root, date, time, "dump.log")),
            "tmp_screenshots": os.path.join(tmpdir, "screenshots"),
        }
