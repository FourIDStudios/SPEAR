
 #TODO #3 : Create loglevels with numeric values and only log messages with a level higher than the current level given if a level is set
 
class Logger:
    debug = False
    sepperator = "---------------------------------"
    
    def log(message, includeSepperator=False):
        if Logger.debug:
            print(message,end=f"{Logger.sepperator if includeSepperator else ''}")
    
    def logln(message, includeSepperator=False):
        if Logger.debug:
            print(message,end=f"\n{(Logger.sepperator) if includeSepperator else ''}")