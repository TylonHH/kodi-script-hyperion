import subprocess


class Remote:
    hyperion_remote = ''

    priority = ''

    def __init__(self, hyperion_remote='hyperion-remote', priority='0'):
        self.hyperion_remote = hyperion_remote
        self.priority = priority

    def color(self, color, priority=None):
        self.run(priority=priority, args='--color ' + '"' + color + '"')

    def effect(self, effect, priority=None):
        self.run(priority=priority, args='--effect ' + '"' + effect + '"')

    def clear(self, priority=None):
        self.run(priority=priority, args='--clear')

    def clearAll(self):
        self.run(args='--clearall')

    def run(self, args=None, priority=None):

        if not args:
            return False

        if priority == None:
            priority = self.priority

        cmd = self.hyperion_remote + ' --priority ' + priority + ' ' + args

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        ret, err = p.communicate()

        print 'Hyperion.Remote: ' + str(ret)

        if p.returncode == 0:
            return ret
        else:
            return False
