import datetime
from enum import Enum

class Logger(Enum):
  ERROR = 1
  WARNING = 2
  INFO = 3
  DEBUG = 4
  TRACE = 5

class Log():
  def __init__(self, level=1):
    self.level = level

  def set_level(self, level):
    self.level = level

  def log_msg(self, type, msg):
    if (type == Logger.ERROR and self.level > 0):
      print(str(datetime.datetime.now()) + '\t' + 'ERROR' + '\t' + msg)
    elif (type == Logger.WARNING and self.level > 1):
      print(str(datetime.datetime.now()) + '\t' + 'WARNING' + '\t' + msg)
    elif (type == Logger.INFO and self.level > 2):
      print(str(datetime.datetime.now()) + '\t' + 'INFO' + '\t' + msg)
    elif (type == Logger.DEBUG and self.level > 3):
      print(str(datetime.datetime.now()) + '\t' + 'DEBUG' + '\t' + msg)
    elif (type == Logger.TRACE and self.level > 4):
      print(str(datetime.datetime.now()) + '\t' + 'TRACE' + '\t' + msg)