import xbmc, os, json, socket

from resources.lib import webcolors


class Remote:
    def __init__(self, hyperion_host='127.0.0.1', hyperion_port='19444', priority='0'):
        self.hyperion_host = hyperion_host
        self.hyperion_port = hyperion_port
        self.priority = priority
        self.state_file = os.path.join(xbmc.translatePath('special://temp/'), 'hyperion')

    def color(self, color, priority=None):

        payload = {'command': 'color', 'color': webcolors.name_to_rgb(color), 'priority': priority}

        self.run(payload=payload)

        if color == 'black':
            self.setState('off')
        else:
            self.setState('on')

    def effect(self, effect, priority=None):
        payload = {'command': 'effect', 'effect': {'name': effect}, 'priority': priority}
        self.run(payload=payload)
        self.setState('on')

    def clear(self, priority=None):
        payload = {'command': 'clear', 'priority': priority}
        self.run(payload=payload)
        self.setState('on')

    def clearAll(self):
        payload = {'command': 'clearall'}
        self.run(payload=payload)
        self.setState('on')

    def serverinfo(self):
        payload = {'command': 'serverinfo'}
        self.run(payload=payload)

    def run(self, payload=None):

        if not payload:
            return False

        if payload['priority'] is None:
            payload['priority'] = int(self.priority)

        data = json.dumps(payload) + '\n'

        try:
            ret = self.nc(data)
        except Exception, e:
            print "Hyperion.Remote: " + str(e)
            return False

        print 'Hyperion.Remote: ' + str(ret)

        return ret

    def setState(self, state):
        if state == 'off':
            if os.path.exists(self.state_file):
                os.remove(self.state_file)
        else:
            open(self.state_file, 'a').close()

    def getState(self):
        return os.path.exists(self.state_file)

    def nc(self, data):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.connect((self.hyperion_host, int(self.hyperion_port)))

            s.sendall(data)

            data = s.recv(4096)

            s.close()

        except socket.error as exc:
            raise Exception(exc)

        return json.loads(data)
