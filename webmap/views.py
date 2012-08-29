from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseNotAllowed
from subprocess import Popen, PIPE
import shlex, sys, re, socket, simplejson, urllib2, json
import webmap.settings as settings
from django_websocket import accept_websocket


def index(req):
    return TemplateResponse(req, 'map/index.html')


def traceroute(req, destination):
    """
                                        hop ctr  time
        Returns asyncronously a tuple: [1, 'NO', 5.23]
    """
    try:
        destination = str(socket.gethostbyname(destination))
        origin = str(socket.gethostbyname(_get_client_ip(req)))
    except Exception as e:
        if settings.DEBUG:
            print e
        return HttpResponseNotAllowed('<b>!!</b>')
    #ip = '123.3.164.244'

    return HttpResponse(_traceroute(destination, origin), mimetype='application/json')

@accept_websocket
def ws_traceroute(req, to):
    req.websocket.send(_traceroute(to))


######## Helpers:


def _traceroute(destination, origin):

    cmd = shlex.split(
        ('tracert -h 60 -d %s' % destination) if 'win' in sys.platform else
        ('traceroute %s -n -m 60' % destination)
    )
    route = Popen(cmd, stdout=PIPE)
    start, stop = _hop(_lookup(origin)), _hop(_lookup(destination))
    yield "["
    yield "%s," % start
    yield "%s," % stop
    #
    #   Read asyncronously (line-buffered) from the traceroute
    #   stdout
    #

    hoppat = re.compile(r'^(?P<hop>\d+)\s+(?P<ip>[^\s]+)\s+(?P<t1>[^\s]+)(\sms)?\s+(?P<t2>[^\s]+)(\sms)?\s+(?P<t3>[^\s]+)(\sms)?')
    dreamland = re.compile(r'\*\s+\*\s+\*')
    I_HAVE_DREAMT = False

    while 1:
        hop = route.stdout.readline().rstrip()
        if hop != '':
            #Do something
            #   if * * * x 1:  hop = dreamland
            #   if * * * x 2:  hop = destination
            #

            if re.search(dreamland, hop) != None:

                if I_HAVE_DREAMT:   # We have already been to dreamland.
                    yield "%s" % _hop('destination', '')
                    break

                yield "%s," % _hop('dreamland', '')
                I_HAVE_DREAMT = True
            else:
                m = re.search(hoppat, hop)
                if m != None:
                    yield "%s," % _hop(_lookup(str(m.group('ip'))), '')
        else:
            break
    yield "]"
    route.kill()


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _lookup(host):
    """ Looks up a ip/host's country """
    data = urllib2.urlopen('http://geoip.komsys.org/?ip=%s&type=CTR_ONLY' % host).read().rstrip().lstrip()
    return data


def _hop(ctr, times=''):
    return json.dumps(
        { "ctr" :ctr, "times" : times }
    )


if __name__ == '__main__':
    print _lookup('hw.no')
