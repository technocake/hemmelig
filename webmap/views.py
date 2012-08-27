from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseNotAllowed
from subprocess import Popen, PIPE
import shlex, sys, re, socket, simplejson, urllib2, json


def index(req):
    return TemplateResponse(req, 'map/index.html')


def traceroute(req, destination):
    """
                                        hop ctr  time
        Returns asyncronously a tuple: [1, 'NO', 5.23]
    """
    try:
        destination = str(socket.gethostbyname(destination))
        origin = str(socket.gethostbyname(req.ip))
    except:
        return HttpResponseNotAllowed('<b>!!</b>')
    #ip = '123.3.164.244'

    return HttpResponse(_traceroute(destination, origin))


def _traceroute(destination, origin):

    cmd = shlex.split(
        ('tracert -h 60 -d %s' % destination) if 'win' in sys.platform else
        ('traceroute %s -n -m 60' % destination)
    )
    route = Popen(cmd, stdout=PIPE)
    start, stop = _hop(_lookup(origin), _hop(_lookup(destination)))

    yield start
    yield stop
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
                yield _hop('dreamland', '')

                if I_HAVE_DREAMT:   # We have already been to dreamland.
                    yield _hop('destination', '')
                    break
                I_HAVE_DREAMT = True
            else:
                m = re.search(hoppat, hop)
                if m != None:
                    yield _hop(str(m.groups()), '')
        else:
            break


def _lookup(host):
    """ Looks up a ip/host's country """
    data = urllib2.urlopen('http://geoip.komsys.org/?ip=%s' % host).read()
    return simplejson.dumps(data)


def _hop(ctr, times):
    return json.dumps('{"ctr" : "%s", "times": "%s"}' % (ctr, times))


if __name__ == '__main__':
    print _lookup('hw.no')
