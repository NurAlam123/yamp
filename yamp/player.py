from vlc import MediaPlayer, Media
import os


class Player:
    # for not to show logs on screen
    os.environ["VLC_VERBOSE"] = str("-1")

    media_player = MediaPlayer()

    def play(self, stream_url: str) -> list:
        media = Media(stream_url)
        self.media_player.set_media(media)
        if self.media_player.is_playing():
            self.media_player.stop()
        playing = self.media_player.play()
        return playing
