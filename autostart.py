import xbmc
import xbmcaddon

settings = xbmcaddon.Addon(id='script.hyperion')

autostart = settings.getSetting('autostart')


class HyperionWatch(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)

    def onPlayBackStarted(self):
        if xbmc.Player().isPlayingVideo():
            # TODO
            xbmc.executebuiltin('RunScript(/usr/local/bin/hyperion-clear.py)')  # clear all effect

        if xbmc.Player().isPlayingAudio():
            # TODO
            xbmc.executebuiltin('RunScript(/usr/local/bin/hyperion-effect-rainbow-swirl.py)')  # start effect

    def onPlayBackEnded(self):
        # TODO
        xbmc.executebuiltin('RunScript(/usr/local/bin/hyperion-effect-rainbow-swirl.py)')  # start effect

    def onPlayBackStopped(self):
        # TODO
        xbmc.executebuiltin('RunScript(/usr/local/bin/hyperion-effect-rainbow-swirl.py)')  # start effect

    def onPlayBackPaused(self):
        if xbmc.Player().isPlayingVideo():
            # TODO
            xbmc.executebuiltin('RunScript(/usr/local/bin/hyperion-effect-rainbow-swirl.py)')  # start effect

    def onPlayBackResumed(self):
        if xbmc.Player().isPlayingVideo():
            # TODO
            xbmc.executebuiltin('RunScript(/usr/local/bin/hyperion-clear.py)')  # clear all effect


if (autostart == "true"):
    HyperionWatch()

    # TODO ??
    # while(1):
    #     if xbmc.Player().isPlayingVideo():
    #         VIDEO = 1
    #     else:
    #         VIDEO = 0
    #
    #     xbmc.sleep(3000)
