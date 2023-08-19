import logging
import os
import sys


class Logger:
    """
    Logger class provides us to modify logging object
    with more simple syntax and more simple definitions,
    especially for the definitions of paths and log files.

    """
    def __init__(self,
                 name: str = None,
                 file_name: str = None,
                 path: str = None,
                 extra: dict = None):

        self.name = name or __name__
        self.file_name = file_name or "main.log"
        self.path = path or get_src_path("src\\logs\\")

        # Main Attributes
        self.logger = None
        self.formatter = None
        self.file_handler = None

        # Formats.
        self.extra = extra or dict()
        self.formats = list()

        # Level Attribute
        self._level = logging.WARNING

        # Define handlers and main attributes
        self._define_handlers()

    def _define_format(self) -> str:
        self.formats = [
            "levelname", "asctime", "name"
        ] + list(self.extra.keys()) + [
            "message"
        ]
        fmt = ""
        for format_str in self.formats:
            fmt += f"%({format_str})s: "
        fmt = fmt.rstrip().rstrip(":")
        return fmt

    def _define_handlers(self):
        # Define main logging object.
        self.logger = logging.getLogger(name=self.name)

        # Define formatter.
        fmt = self._define_format()
        self.formatter = logging.Formatter(fmt)

        # Define file handler.
        self.file_handler = logging.FileHandler(self.path + self.file_name)
        self.file_handler.setFormatter(self.formatter)

        # Configure main logging object with above definitions.
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(level=self._level)
        self.logger = logging.LoggerAdapter(self.logger, self.extra)
        return self

    def update_logger_attr(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self._define_handlers()

    def get_logger(self) -> logging.Logger:
        self.update_logger_attr(file_name="main.log")
        return self.logger

    def get_robot_logger(self):
        self._level = logging.INFO
        self.update_logger_attr(file_name="robot.log")
        return self.get_logger()


def get_src_path(append_src: str = None,
                 include_src: bool = False,
                 include_sys_path: bool = True) -> str:
    """
    The function returns the path of src file in the directory
    without depending on current working directory. It will be
    not applicable if the current working directory is out of the
    project file, as the main algorithm of the function is appending
    parent directory up to obtaining src directory it-self.

    Example usage can be, get_src_path(append_src='src/logs/')

    :param str append_src: Append new directory from src file.
    :param include_src: Include 'src/' in the obtained path string.
    :param bool include_sys_path: Append sys path list with obtained src path.
    :return: Resulting path string.
    """
    current_path = os.getcwd()
    max_iter = len(str(current_path).split("\\"))

    path = None
    iteration = 0
    while path is None and iteration < max_iter:
        candidate_path, candidate_directory = os.path.split(current_path)
        current_path = os.path.abspath(candidate_path)
        if candidate_directory == "src":
            path = current_path
            if include_sys_path:
                sys.path.append(path)
            break
        iteration += 1

    if path is None:
        path = os.getcwd()
    if include_src:
        path = os.path.join(path, "src")
    if append_src:
        path = os.path.join(path, append_src)
    if not os.path.isdir(path):
        os.makedirs(name=path)

    return path


if __name__ == "__main__":
    pass
