import json
import socket
import time
import xbmc

from resources.lib import webcolors


def log(txt):
    message = '%s: %s' % ('Hyperion.Remote', txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGNOTICE)


class Remote:
    def __init__(self, hyperion_host='127.0.0.1', hyperion_port='19444', priority='0'):
        self.hyperion_host = hyperion_host
        self.hyperion_port = hyperion_port
        self.priority = priority

        try:
            import StorageServer
        except:
            from resources.lib import storageserverdummy as StorageServer

        self.cache = StorageServer.StorageServer('hyperion', 8544)

    def color(self, color, priority=None):

        payload = {'command': 'color', 'color': webcolors.name_to_rgb(color), 'priority': priority}

        if color == 'black':
            self.setState('off')
        else:
            self.setState('on')

        return self.run(payload)

    def effect(self, effect, priority=None):
        payload = {'command': 'effect', 'effect': {'name': effect}, 'priority': priority}

        self.setState('on')

        return self.run(payload)

    def clear(self, priority=None):
        payload = {'command': 'clear', 'priority': priority}

        self.setState('on')

        return self.run(payload)

    def clearAll(self):
        payload = {'command': 'clearall'}
        self.setState('on')

        return self.run(payload)

    def serverinfo(self):
        payload = {'command': 'serverinfo'}

        return self.run(payload)

    def run(self, payload):

        if not payload:
            return False

        if 'priority' in payload and payload['priority'] is None:
            payload['priority'] = int(self.priority)

        data = json.dumps(payload) + '\n'

        try:
            ret = self.nc(data)
        except Exception as e:
            log(str(data))
            log(str(e))
            return False

        return ret

    def setState(self, state):
        self.cache.set('state', state)

    def getState(self):
        return self.cache.get('state')

    def nc(self, data):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.connect((self.hyperion_host, int(self.hyperion_port)))

            s.sendall(data)

            data = self._recv(s)

            s.close()

        except socket.error as e:
            raise Exception(e)

        return json.loads(data)

    def _recv(self, s, timeout=0.1):
        # make socket non blocking
        s.setblocking(0)

        # total data partwise in an array
        total_data = []
        data = ''

        # beginning time
        begin = time.time()
        while 1:
            # if you got some data, then break after timeout
            if total_data and time.time() - begin > timeout:
                break

            # if you got no data at all, wait a little longer, twice the timeout
            elif time.time() - begin > timeout * 2:
                break

            # recv something
            try:
                data = s.recv(8192)
                if data:
                    total_data.append(data)
                    # change the beginning time for measurement
                    begin = time.time()
                else:
                    # sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass

        # join all parts to make final string
        return ''.join(total_data)
