import threading
import time
from datetime import datetime
from main import stream, cfg
import calendar

class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1, timeout=10):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.start_time = datetime.now()
        self.interval = interval
        self.timeout = timeout
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
    @property
    def time_elapsed(self):
        return (datetime.now() - self.start_time).total_seconds()
        
    
    def run(self):
        """ Method that runs forever """
        start = True
        while start:
            if self.time_elapsed >= self.timeout:
                start = False
                return False
            stream()
            
            
            

t = ThreadingExample(interval=0, cfg["timeout"])
t.run()
