import sys, os, xbmcaddon, xbmcgui, xbmc
import hyperion
from urlparse import parse_qsl

__addon__ = xbmcaddon.Addon()
__title__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
__language__ = __addon__.getLocalizedString
__hyperion__ = None


def log(txt):
    message = '%s: %s' % (__title__, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


class Main:
    def __init__(self):
        hyperion_remote = __addon__.getSetting('hyperion_remote')
        priority = __addon__.getSetting('priority')

        global __hyperion__

        if not hyperion_remote:
            print 'Hyperion.Script: ' + __language__(20000)
            xbmcgui.Dialog().notification(__title__, __language__(20000), __icon__, 5000)
            return

        __hyperion__ = hyperion.Remote(hyperion_remote=hyperion_remote, priority=priority)

        self.params = dict(parse_qsl('&'.join(sys.argv)))

        if not self.params:
            xbmc.executebuiltin('Addon.OpenSettings(script.hyperion)')

        command = self.params.get('command', None)

        log('Script: command: %s' % command)

        if command is None:
            log('Script: no command given?!')

        elif command == 'effect':
            self._effect()

        elif command == 'color':
            self._color()

        elif command == 'clear':
            self._clear()

        elif command == 'clearall':
            self._clearAll()

        elif command == 'switch':
            self._switch()

    def _effect(self):
        effect = self.params.get('effect', None)
        priority = self.params.get('priority', None)

        if not effect:
            return

        xbmcgui.Dialog().notification(__title__, effect, __icon__, 3000)
        __hyperion__.effect(effect, priority)

    def _color(self):
        color = self.params.get('color', None)
        priority = self.params.get('priority', None)

        if not color:
            return

        xbmcgui.Dialog().notification(__title__, color, __icon__, 3000)
        __hyperion__.color(color, priority)

    def _clear(self):
        priority = self.params.get('priority', None)

        xbmcgui.Dialog().notification(__title__, __language__(20001), __icon__, 3000)
        __hyperion__.clear(priority)

    def _clearAll(self):
        xbmcgui.Dialog().notification(__title__, __language__(20001), __icon__, 3000)
        __hyperion__.clearAll()

    def _switch(self):
        temp_file = os.path.join(xbmc.translatePath('special://temp/'), __title__)
        priority = self.params.get('priority', None)

        if os.path.exists(temp_file):
            if __addon__.getSetting('switch_type') == '0':
                __hyperion__.effect(__addon__.getSetting('switch_effect'), priority)
            else:
                __hyperion__.clearAll()

            os.remove(temp_file)
        else:
            __hyperion__.color('black', priority)
            open(temp_file, 'a').close()

    # TODO
    def _multiSwitch(self):
        pass


if __name__ == '__main__':
    log('Script: execute')
    Main()
