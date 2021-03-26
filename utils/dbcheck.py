from configuration import Config
import sys, os, time
import django
from django.core.management import call_command
from YAPO.wsgi import application
from utils.printing import Logger
log = Logger()

# First of all, check if the db is located in the old folder (root)
def boot():
    dest = os.path.join(Config().database_dir)
    okmoved = True

    SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
    compiled = False
    try:
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            SCRIPT_ROOT = os.path.dirname(sys.executable)
            compiled = True
    except AttributeError:
        SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
        compiled = False

    if not os.path.isfile(os.path.join(dest, "db.sqlite3")):
        print("\n")
        print("No database\n===========")
        print(f"There is no database installed at: {os.path.join(dest, 'db.sqlite3')}\nGenerating a new database...\n\n")
        time.sleep(4)
        a=call_command('makemigrations', interactive = False)
        b=call_command('migrate', interactive = False)
        return
    else:
        '''
        This needs to be modified to actually check for pending migrations.
        As it is now, migration is always performed on startup.
        '''
        #try:
        #    check = call_command('makemigrations','--check','--dry-run')
        #except Exception as e:
        #    print(e.args[0])
        #    #sys.exit(0)
        #if check is not None:
        #    log.info(f'DBCHK: Database needs an upgrade, migration commencing.')
        a=call_command('makemigrations', interactive = False)
        a=call_command('migrate', interactive = False)
        return