import sys


class config:
    REMOTE_HOST_URI = "technocake@marte.komsys.org:/srv/webmap/"
    REMOTE_WEB_URI = "http://webmap.technocake.net/" if not 'win' in sys.platform else "http://localhost:8000"
    LOCAL_DIR = "/Users/technocake/django/webmap/"
