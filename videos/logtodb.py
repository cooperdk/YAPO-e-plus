import logging
#from django_extensions import logging

import datetime
#import logging

class logtodb(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        from videos.models import LogEntry
        newLogEntry = LogEntry() # self.get_model('LogEntry')
        newLogEntry.timestamp = datetime.datetime.now()
        newLogEntry.string = record.getMessage()
        newLogEntry.severity = record.levelname

        newLogEntry.save()

