import urlparse, sys
import xbmc, xbmcaddon, xbmcgui
import hyperion

__addon__ = xbmcaddon.Addon()
__title__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
__language__ = __addon__.getLocalizedString


def Main():
    hyperion_remote = __addon__.getSetting('hyperion_remote')
    priority = __addon__.getSetting('priority')

    hp = hyperion.Remote(hyperion_remote=hyperion_remote, priority=priority)

    # hyperion-remote binary not definied, throw error message
    if not hyperion_remote:
        print 'Hyperion.JSONRPC: ' + __language__(20000)
        xbmcgui.Dialog().notification(__title__, __language__(20000), __icon__, 5000)
        return

    params = urlparse.parse_qs('&'.join(sys.argv[1:]))

    command = params.get('command', None)[0]

    if not command:
        print 'Hyperion.JSONRPC: no command given?!'
        return False

    print 'Hyperion.JSONRPC: command %s found' % command

    if command == 'effect':

        effect = params.get('effect', None)[0]

        if not effect:
            return False

        hp.effect(effect)
        xbmcgui.Dialog().notification(__title__, effect, __icon__, 3000)

    elif command == 'color':

        color = params.get('color', None)[0]

        if not color:
            return False

        hp.color(color)
        xbmcgui.Dialog().notification(__title__, color, __icon__, 3000)

    elif command == 'switch':
        # TODO
        script_switch = __addon__.getSetting("script_switch")
        xbmc.executebuiltin('RunScript(' + script_switch + ')')

    elif command == 'clear':

        hp.clear()
        xbmcgui.Dialog().notification(__title__, __language__(20001), __icon__, 3000)


if __name__ == '__main__':
    Main()
