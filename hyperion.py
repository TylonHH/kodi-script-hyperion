import xbmc, os, subprocess


class Remote:
    def __init__(self, hyperion_remote='hyperion-remote', priority='0'):
        self.hyperion_remote = hyperion_remote
        self.priority = priority
        self.state_file = os.path.join(xbmc.translatePath('special://temp/'), 'hyperion')

    def color(self, color, priority=None):
        self.run(priority=priority, args='--color ' + '"' + color + '"')

        if color == 'black':
            self.setState('off')
        else:
            self.setState('on')

    def effect(self, effect, priority=None):
        self.run(priority=priority, args='--effect ' + '"' + effect + '"')
        self.setState('on')

    def clear(self, priority=None):
        self.run(priority=priority, args='--clear')
        self.setState('on')

    def clearAll(self):
        self.run(args='--clearall')
        self.setState('on')

    def run(self, args=None, priority=None):

        if not args:
            return False

        if priority is None:
            priority = self.priority

        cmd = self.hyperion_remote + ' --priority ' + priority + ' ' + args

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        ret, err = p.communicate()

        print 'Hyperion.Remote: ' + str(ret)

        if p.returncode == 0:
            return ret
        else:
            return False

    def setState(self, state):
        if state == 'off':
            if os.path.exists(self.state_file):
                os.remove(self.state_file)
        else:
            open(self.state_file, 'a').close()

    def getState(self):
        return os.path.exists(self.state_file)
