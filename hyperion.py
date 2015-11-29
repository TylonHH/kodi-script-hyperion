import subprocess


class Remote:
    hyperion_remote = ''

    priority = ''

    def __init__(self, hyperion_remote='hyperion-remote', priority='0'):
        self.hyperion_remote = hyperion_remote
        self.priority = priority

    def color(self, color):
        self.run('--color ' + '"' + color + '"')

    def effect(self, effect):
        self.run('--effect ' + '"' + effect + '"')

    def clear(self):
        self.run('--clear')

    def run(self, args):
        cmd = self.hyperion_remote + ' --priority ' + self.priority + ' ' + args

        self.debug(cmd)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        self.debug(p.communicate())

    def debug(self, echo):
        print 'Hyperion.Remote: ' + str(echo)
