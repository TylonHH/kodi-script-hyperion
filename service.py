import xbmc, xbmcaddon, xbmcgui
import hyperion

__addon__ = xbmcaddon.Addon()
__title__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
__language__ = __addon__.getLocalizedString


class HyperionService(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)

        hyperion_remote = __addon__.getSetting('hyperion_remote')
        priority = __addon__.getSetting('priority')

        if not hyperion_remote:
            print 'Hyperion.Service: ' + __language__(20000)
            xbmcgui.Dialog().notification(__title__, __language__(20000), __icon__, 5000)
            return

        self.hyperion = hyperion.Remote(hyperion_remote=hyperion_remote, priority=priority)

    def onPlayBackStarted(self):
        print 'Hyperion.Service: onPlayBackStarted : ' + str(__addon__.getSetting('clear_on_video_playback'))
        if __addon__.getSetting('clear_on_video_playback') and xbmc.Player().isPlayingVideo():
            self.hyperion.clear()

        if __addon__.getSetting('effect_on_playback_audio') and xbmc.Player().isPlayingAudio():
            self.hyperion.effect(__addon__.getSetting('effect_on_playback_audio'))

    def onPlayBackResumed(self):
        if __addon__.getSetting('clear_on_video_playback') and xbmc.Player().isPlayingVideo():
            self.hyperion.clear()

    def onPlayBackPaused(self):
        if __addon__.getSetting('effect_on_playback_paused') and xbmc.Player().isPlayingVideo():
            self.hyperion.effect(__addon__.getSetting('effect_on_playback_paused'))

    def onPlayBackStopped(self):
        if __addon__.getSetting('effect_on_playback_stopped'):
            self.hyperion.effect(__addon__.getSetting('effect_on_playback_stopped'))

    def onPlayBackEnded(self):
        self.onPlayBackStopped()


print 'Hyperion.Service: autostart included'

if __addon__.getSetting('autostart') == 'true':
    print 'Hyperion.Service: autostart enabled'
    HyperionService()
    print 'Hyperion.Service: autostart executed'

while not xbmc.abortRequested:
    # print 'Hyperion.Service: %s' % time.time()
    xbmc.sleep(5000)
