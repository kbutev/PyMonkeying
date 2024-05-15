import threading
from typing import Protocol
from kink import inject
from datetime import datetime


def current_date():
    return datetime.today().strftime('%Y.%m.%d %H:%M:%S.%f')[:-3]


def get_current_thread_name():
    return threading.get_ident() if not threading.main_thread() else 'main'


def get_current_thread_description():
    return f'thread.{get_current_thread_name()}'


class LoggerProtocol(Protocol):
    def info(self, message): pass
    def warning(self, message): pass
    def error(self, message): pass
    def verbose_info(self, message): pass
    def debug(self, message): pass


@inject(alias=LoggerProtocol)
class Logger:
    
    DEBUG = True
    VERBOSE = False
    SHOW_THREAD = True
    
    def __init__(self):
        self.verbose_mode = Logger.VERBOSE
        self.debug_mode = Logger.DEBUG
        self.show_thread = Logger.SHOW_THREAD
    
    def info(self, message):
        timestamp = current_date()
        thread = f'|{get_current_thread_description()}' if self.show_thread else ''
        print(f'{timestamp}{thread}| {message}')
    
    def warning(self, message):
        timestamp = current_date()
        thread = f'|{get_current_thread_description()}' if self.show_thread else ''
        print(f'{timestamp}{thread}|WARN| {message}')
    
    def error(self, message):
        timestamp = current_date()
        thread = f'|{get_current_thread_description()}' if self.show_thread else ''
        print(f'{timestamp}{thread}|ERROR| {message}')
    
    def verbose_info(self, message):
        if self.verbose_mode:
            self.info(message)
    
    def debug(self, message):
        if self.debug_mode:
            self.info(message)
