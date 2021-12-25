
# -*- coding: utf-8 -*-
"""
Custom logger
Author: Knut Magnus Aasrud, from here: https://github.com/kmaasrud/doctor/blob/f6eea662de64dd2fa7a19548e71790ebd5084f3c/kodb/log.py
"""

import inspect
import shutil

LEVELS = {
    "DEBUG": 5,
    "D": 5,
    "INFO": 4,
    "I": 4,
    "SUCCESS": 3,
    "✓": 3,
    "WARNING": 2,
    "W": 2,
    "ERROR": 1,
    "E": 1,
    "CRITICAL": 0,
    "C": 0
}

class Message:
    def __init__(self, level):
        try:
            # Extract log level from string
            self.level = LEVELS[level.upper()]
        except (KeyError, AttributeError):
            # If key does not match, check if log_level is a valid int or else set the level to DEBUG
            self.level = level if type(level) == int and abs(level) < 5 else 4


    def set_level(self, level):
        self.__init__(level)


    def print_message(self, msg, level_name, *styles, file=None, lst = None):
        if self.level >= LEVELS[level_name]:
            if file:
                # If there's room, then first print the name of the calling file right aligned
                left_align_len = len(level_name) + 2 + len(msg)
                print(self.right_align(f"({file})", left_align_len=left_align_len), end="\r")

            # Then print the message with the message level styled
            print("[" + self.style(level_name, *styles) + "]" + ":", msg)

            if lst:
                # Then print the list
                leftlength = len("[" + level_name + "]" + ":") * " "
                for element in lst:
                    print(leftlength + str(element))
            

    def debug(self, msg, lst = None):
        from_frame = inspect.stack()[1]
        file = inspect.getfile(from_frame[0])
        self.print_message(msg, "DEBUG", "bold", file=file, lst=lst)


    def info(self, msg, lst = None):
        self.print_message(msg, "INFO", "bold", "blue", lst=lst)


    def success(self, msg, lst = None):
        self.print_message(msg, "SUCCESS", "bold", "green", lst=lst)


    def warning(self, msg, lst = None):
        self.print_message(msg, "WARNING", "bold", "yellow", lst=lst)


    def error(self, msg, lst = None):
        self.print_message(msg, "ERROR", "bold", "red", lst=lst)


    def critical(self, msg, lst = None):
        from_frame = inspect.stack()[1]
        file = inspect.getfile(from_frame[0])
        self.print_message(msg, "C", "bold", "red", "underline", file=file, lst=lst)

    def style(self, text, *styles):
        code = {
            'red': '31',
            'green': '32',
            'yellow': '33',
            'blue': '34',
            'magenta': '35',
            'cyan': '36',
            'bright red': '91',
            'bright green': '92',
            'bright yellow': '93',
            'bright blue': '94',
            'bright magenta': '95',
            'bright cyan': '96',
            'bold': '1',
            'faint': '2',
            'italic': '3',
            'underline': '4',
            'blink': '5',
            'strike': '9'
        }

        for style in styles:
            text = "\033[" + code[style] + "m" + text + "\033[0m"

        return text

    def right_align(self, text, left_align_len=0):
        columns = shutil.get_terminal_size()[0]
        if left_align_len + len(text) < columns:
            return(text.rjust(columns))

LOG = Message("INFO")