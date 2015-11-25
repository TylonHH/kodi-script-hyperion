import urlparse, sys
import xbmc, xbmcaddon


def main(isAutostart=False):
    print 'script.hyperion: Starting Hyperion script'

    settings = xbmcaddon.Addon(id='script.hyperion')

    try:
        params = urlparse.parse_qs('&'.join(sys.argv[1:]))
        command = params.get('command', None)
    except:
        command = None

    if command and command[0] == 'switch':
        script_switch = settings.getSetting("script_switch")
        xbmc.executebuiltin('RunScript(' + script_switch + ')')

        # elif command and command[0] == 'something':
        #	xbmc.executebuiltin('SomeCommand')


if __name__ == '__main__':
    main()
