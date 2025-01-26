
 #TODO #3 : Create loglevels with numeric values and only log messages with a level higher than the current level given if a level is set

from enum import Enum

class LogLevel(Enum):
    Debug = 0,
    Informational = 1, 
    Notice = 2,
    Warning = 3, 
    Error = 4, 
    Critical = 5,
    Emergency = 6,

class Logger:
    """
        Logger class that handles debugs and prints, as a way to centralize log information, 
        such that in the future we can easily access and control logs.
        
        The logger will default to the debug level, which is to say it will log all information
        at or above debug, as debug is the lowest level, this means all information will be logged.
        
    """
    def __init__(self, defaultLevel:LogLevel = LogLevel.Debug):
        self.level = LogLevel.Debug
        self.sepperator = "---------------------------------"

    def setLevel(self, logLevel:LogLevel = LogLevel.Debug):
        self.level = logLevel

    def log(self, message:str, includeSepperator=False, logLevel:LogLevel = LogLevel.Debug):
        if(logLevel.value >= self.level.value):
            print(message,end=f"{Logger.sepperator if includeSepperator else ''}")
    
    def logln(self, message:str, includeSepperator=False, logLevel:LogLevel = LogLevel.Debug):
        if(logLevel.value >= self.level.value):
            print(message,end=f"\n{(Logger.sepperator) if includeSepperator else ''}")
