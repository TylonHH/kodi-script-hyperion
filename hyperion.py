import xbmc, os, json, socket


class Remote:
    def __init__(self, hyperion_host='127.0.0.1', hyperion_port='19444', priority='0'):
        self.hyperion_host = hyperion_host
        self.hyperion_port = hyperion_port
        self.priority = priority
        self.state_file = os.path.join(xbmc.translatePath('special://temp/'), 'hyperion')

    def color(self, color, priority=None):

        payload = {'command': 'color', 'color': color, 'priority': priority}

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
        self.setState('on')

    def run(self, payload=None):

        if not payload:
            return False

        if not payload['priority']:
            payload['priority'] = self.priority

        print json.dumps(payload)

        try:
            ret = Client().connect(self.hyperion_host, self.hyperion_port).send(payload).recv()
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


class Client(object):
    socket = None

    def __del__(self):
        self.close()

    def connect(self, host, port, timeout=5):
        self.socket = socket.socket()
        self.socket.settimeout(timeout)
        try:
            self.socket.connect((host, int(port)))
        except socket.error, exc:
            raise Exception(exc)

        return self

    def send(self, data):
        if not self.socket:
            raise Exception('You have to connect first before sending data')
        self._send(data)
        return self

    def recv(self):
        data = self.recv()
        self.close()
        return data

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def _send(self, data):
        try:
            serialized = json.dumps(data)
        except (TypeError, ValueError), e:
            raise Exception('You can only send JSON-serializable data')
        self.socket.send(serialized)

    def _recv(self):
        # read the length of the data, letter by letter until we reach EOL
        length_str = ''
        char = self.socket.recv(1)
        while char != '\n':
            length_str += char
            char = self.socket.recv(1)
        total = int(length_str)
        # use a memoryview to receive the data chunk by chunk efficiently
        view = memoryview(bytearray(total))
        next_offset = 0
        while total - next_offset > 0:
            recv_size = self.socket.recv_into(view[next_offset:], total - next_offset)
            next_offset += recv_size
        try:
            deserialized = json.loads(view.tobytes())
        except (TypeError, ValueError), e:
            raise Exception('Data received was not in JSON format')
        return deserialized
