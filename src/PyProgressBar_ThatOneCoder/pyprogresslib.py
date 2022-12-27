import os
import time
import sys
import json
import threading
from termcolor import colored as coloured

if os.name == 'nt':
  import msvcrt
  import ctypes
  class _CursorInfo(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int),("visible", ctypes.c_byte)]

class progressBar:
  def __init__(self,completeColour="green",incompleteColour="red", barLength=30, timeDelay=0.01, roundPercentTo=1):

    if completeColour not in ["grey","red","green","yellow","blue", "magenta","cyan","white"]:
      raise ValueError("Accepted colours for completeColour are: grey, red, green, yellow, blue, magenta, cyan and white")
    if incompleteColour not in ["grey","red","green","yellow","blue", "magenta","cyan","white"]:
      raise ValueError("Accepted colours for incompleteColour are: grey, red, green, yellow, blue, magenta, cyan and white")
    self.completeColour = completeColour
    self.incompleteColour = incompleteColour
    self.increments = self._percentage = 0
    self._barThread = threading.Thread(target=self.bar, args=(None,))
    self.done = False
    self.progress_bar = ""
    self.timeDelay = timeDelay
    self.barLength = barLength
    self.progress_bar_done = ""
    if self.barLength <= 0:
      raise ValueError("Length of progress bar cannot be 0 or less.")
    for i in range(self.barLength):
      self.progress_bar_done += "▇"
    self.toLog = ""
    if roundPercentTo < 0:
      raise ValueError("Percentage cannot be rounded to a negative number of decimal places.")
    self.percentRound = roundPercentTo

    if sys.platform == "win32":
      self.clear = "cls"
    elif sys.platform == "cygwin":
      self.clear = "cmd /c cls"
    else:
      self.clear = "clear"

  def __repr__(self) -> str:
    return f"Progress Bar using thread: {self._barThread}, {self._percentage}% complete."
      
  def updateBar(self, log:str = "", withDelay:float = 0) -> bool:
    if log != "":
      self.toLog = log
    self.increments += 1
    self.progress_bar += "▇"
    self.progress_bar_done = self.progress_bar_done[1:]
    time.sleep(withDelay)
    if len(self.progress_bar) == self.barLength:
      self.done = True
      return True
    return False

  def run(self) -> None:
    self._barThread.start()
    if os.name == 'posix':
      sys.stdout.write("\033[?25l")
      sys.stdout.flush()
    
    if os.name == 'nt':
      ci = _CursorInfo()
      handle = ctypes.windll.kernel32.GetStdHandle(-11)
      ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
      ci.visible = False
      ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))

  def bar(self, *args) -> None:
    while not self.done:
      print(coloured("Progress: " + self.progress_bar, self.completeColour), end = "")
      print(coloured(self.progress_bar_done, self.incompleteColour), end = "")
      try:
        self._percentage = str(round(100*(len(self.progress_bar)/self.barLength),self.percentRound))
      except:
        self._percentage=0
      print(f" {self._percentage}%")
      if self.toLog != "":
        print(self.toLog)
      os.system(self.clear)
    if self.done:
      try:
        self._barThread._stop()
        if os.name == 'nt':
          ci = _CursorInfo()
          handle = ctypes.windll.kernel32.GetStdHandle(-11)
          ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
          ci.visible = True
          ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        elif os.name == 'posix':
          sys.stdout.write("\033[?25h")
          sys.stdout.flush()
        return
      except AssertionError:
        return

  def forceEndBar(self) -> bool:
    try:
      self.done = True
      return True
    except AssertionError: pass # getting an error from threading, unaware on how to fix it.

  def isDone(self):
    return self.done

class progressIcon:
  def __init__(self, symbolVersion, textColour:str = "white",finishedTextColour:str="white", timeDelay:float = 0.01):
    self.loadFromJson()
    self.version = str(symbolVersion)
    self._iconThread = threading.Thread(target=self.show, args=(None,))
    self.done = False
    
    if timeDelay < 0:
      raise ValueError("Time delay cannot be smaller than 0.")
    if textColour not in ["grey","red","green","yellow","blue", "magenta","cyan","white"]:
      raise ValueError("Accepted colours for textColour are: grey, red, green, yellow, blue, magenta, cyan and white")
    if finishedTextColour not in ["grey","red","green","yellow","blue", "magenta","cyan","white"]:
      raise ValueError("Accepted colours for finishedTextColour are: grey, red, green, yellow, blue, magenta, cyan and white")

    self.timeDelay = timeDelay
    self.textColour = textColour
    self.finishedTextColour = finishedTextColour
    self.newLogInCue = False
    self.toLog = ""

    if sys.platform == "win32":
      self.clear = "cls"
    elif sys.platform == "cygwin":
      self.clear = "cmd /c cls"
    else:
      self.clear = "clear"

  def run(self):
    self._iconThread.start()
    if os.name == 'posix':
      sys.stdout.write("\033[?25l")
      sys.stdout.flush()
    
    if os.name == 'nt':
      ci = _CursorInfo()
      handle = ctypes.windll.kernel32.GetStdHandle(-11)
      ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
      ci.visible = False
      ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))

  def finish(self):
    self.done = True
    if os.name == 'nt':
      ci = _CursorInfo()
      handle = ctypes.windll.kernel32.GetStdHandle(-11)
      ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
      ci.visible = True
      ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
      sys.stdout.write("\033[?25h")
      sys.stdout.flush()

  def addCustomIcon(self,symbols)->int:
    index = int(max(list(self.__symbols.keys()))) + 1
    self.__symbols[str(index)] = symbols
    self.serializeToJSON()
    return index

  def show(self, *args):
    current = 0
    while not self.done:
      os.system(self.clear)
      print(coloured(self.__symbols[self.version][current], self.textColour))
      if self.newLogInCue:
        print(self.toLog)
        self.newLogInCue = False
      time.sleep(0.1)
      current += 1
      if current == len(self.__symbols[self.version])-1:
        current = 0
    try:
      os.system(self.clear)
      print(coloured(self.__symbols[self.version][-1], self.finishedTextColour))
      self._iconThread._stop()
    except AssertionError:
      pass
  
  def serializeToJSON(self):
    with open("waitingSymbols.json","w") as f:
      f.write(json.dumps(self.__symbols))
  def loadFromJson(self):
    with open("waitingSymbols.json") as f:
      self.__symbols = dict(json.loads(f.read()))

  def log(self, text):
    self.toLog = text
    self.newLogInCue = True