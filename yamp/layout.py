from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.reactive import reactive
from textual.widgets import Input, Label, Static, RadioSet, RadioButton, Footer
from textual.containers import Vertical, ScrollableContainer, Container, Horizontal
from time import sleep

from yamp.utils import splash
from yamp.fetch import Fetch
from yamp.player import Player


class InputBox(Input):
    """
    Input Box Handler

    It get the song name from user and search the song in [saavn](https://saavn.com/) with the [saavn unofficial](https://saavn.dev/) api
    and fetch the data. Afterward shows a selection menu on the display.
    """

    def compose(self) -> ComposeResult:
        return super().compose()

    @on(Input.Submitted)
    def submitted(self, event: Input.Submitted) -> None:
        if event.value.strip() == "":
            return

        event.control.clear()
        # song_data = Fetch().fetch_saavn(event.value)
        song_data = [
            (
                "Kiyu Dhunde",
                "./temp_file-ignore.wav",
            ),
            (
                "Believer",
                "./beliver-ignore.mp3",
            ),
            (
                "Lamhey",
                "https://aac.saavncdn.com/531/3f449bcec1c516adf33d8e2eb337407b_12.mp4",
            ),
        ]
        menu = self.app.query_one(SelectionMenu)
        menu.data = song_data


class SelectionMenu(Widget):
    """
    Shows a selection menu on ui.
    For music selection.
    """

    data = reactive([], layout=True)
    index = reactive(0, layout=True)

    def compose(self) -> ComposeResult:
        scrollable_container = ScrollableContainer()
        scrollable_container.can_focus = False
        yield scrollable_container

    @on(RadioSet.Changed)
    def radio_button_pressed(self, event: RadioSet.Changed) -> None:
        selected_index = event.index
        self.index = selected_index
        selected_song = self.data[selected_index]
        url = selected_song[1]
        is_playing = MainLayout.player.play_audio(url)
        if not is_playing:
            return
        now_playing = self.app.query_one(NowPlaying)
        now_playing.song_info = selected_song[0]
        now_playing.update_timer.resume()
        # self.

    def watch_data(self) -> None:
        if not self.data:
            return
        self.app.query_one("#song-container").query_one(Label).update(
            "\u2191 Up \u2193 Down\nEnter - Select\n"
        )
        container = self.query_one(ScrollableContainer)
        if len(container.children) >= 1:
            container.remove_children(RadioSet)
        radio_menu = RadioSet()
        for title, _ in self.data:
            radio_menu.mount(RadioButton(title))
        container.mount(radio_menu)
        radio_menu.focus()

    def watch_index(self):
        MainLayout.player.audio_player and (
            MainLayout.player.audio_player.is_alive()
            and MainLayout.player.stop_thread.set()
        )
        sleep(0.4)
        MainLayout.player = Player()


class NowPlaying(Static):

    song_info = reactive("", layout=True)
    player_status = reactive("", layout=True)
    current_position = reactive("", layout=True)

    def compose(self) -> ComposeResult:
        # yield Label("Volume: 50%", id="volume")
        yield Label("Not Playing Anything...", id="song")
        yield Label("00:00/00:00", id="position")

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(0.5, self.check_position, pause=True)

    def check_position(self) -> None:
        self.current_position = MainLayout.player.status()

    def watch_song_info(self) -> None:
        if not self.song_info:
            return
        self.query_one("#song", Label).update(f":pause_button: | {self.song_info}")

    def watch_current_position(self):
        if not self.current_position:
            return
        self.query_one("#position", Label).update(self.current_position)


class MainLayout(Static):
    """
    Main layout of the app
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True, priority=True),
        Binding("ctrl+p", "toggle_play", "Play/Pause", show=True),
    ]

    player = Player()

    def compose(self) -> ComposeResult:
        with Container(id="main-container"):
            yield Label(splash(), expand=True)
            yield InputBox(placeholder="Type song name")
            with NowPlaying(id="now-playing") as np:
                np.border_title = "Now Playing"
            with Horizontal(id="interactive-container"):
                with Vertical(classes="sub-container"):
                    yield Label("Songs", classes="sub-container-label", expand=True)
                    with Container(id="song-container"):
                        yield Label("No songs to display!")
                        yield SelectionMenu()
                with Vertical(classes="sub-container"):
                    yield Label("Queue", classes="sub-container-label", expand=True)
                    with ScrollableContainer():
                        yield Label("No queue to display!")
                with Vertical(classes="sub-container"):
                    yield Label("History", classes="sub-container-label", expand=True)
                    with ScrollableContainer():
                        yield Label("No history to display!")
        yield Footer()

    def action_toggle_play(self):
        if self.player.is_playing:
            self.player.pause()
        elif self.player.is_paused:
            self.player.resume()

    def action_quit(self):
        self.app.exit()
