import sys


class config:
    REMOTE_HOST_URI = "marte.komsys.org:/srv/webmap/"
    REMOTE_WEB_URI = "http://webmap.technocake.net:8000" if 'win' in sys.platform else "http://localhost:8000"
    LOCAL_DIR = r'/cygdrive/c/Users/technocake/django/webmap/' if 'win' in sys.platform else "/Users/technocake/django/webmap/"
    DELAY = 1
