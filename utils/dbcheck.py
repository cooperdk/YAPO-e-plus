from configuration import Config
import sys, os, time
from django.core.management import call_command
from YAPO.wsgi import application

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
        call_command('makemigrations')
        call_command('migrate')
        return


