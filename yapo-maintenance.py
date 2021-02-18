import sys
from django.conf import settings
from django.apps import AppConfig
from django.core.management import call_command
from django.core.management import execute_from_command_line
import django
from YAPO.wsgi import application
django.setup()
import YAPO.settings
from videos.models import *
#call_command('dumpdata','document_manager.%s' % model_name,format='json',indent=3,stdout=output)
argnum = len (sys.argv)-1

if argnum == 0:
    print("\nYAPO maintenance tool\n=====================\n\nExecuting migrations and migrating the database...")
    x = call_command('makemigrations')
    print(x)
    y = call_command('migrate')
    print(y)

if argnum != 0 and any(
    [
        'shell' in str(sys.argv),
        'get-clean-titles' in str(sys.argv),
        'convert-tags' in str(sys.argv),
        'mark-scenes' in str(sys.argv),
        'dumpdata' in str(sys.argv),
        'loaddata' in str(sys.argv),
    ]
):
    x = execute_from_command_line(sys.argv)
    print(x)