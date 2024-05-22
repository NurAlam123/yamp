from vlc import MediaPlayer, Media


class Player:
    def __init__(self) -> None:
        self.media_player = MediaPlayer()

    def play(self, stream_url: str) -> list:
        media = Media(stream_url)
        self.media_player.set_media(media)
        if self.media_player.is_playing():
            self.media_player.stop()
        self.media_player.play()
