from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.reactive import reactive
from textual.widgets import Input, Label, Static, RadioSet, RadioButton, Footer
from textual.containers import Vertical, ScrollableContainer, Container, Horizontal

from yamp.utils import splash
from yamp.fetch import Fetch
from yamp.player import Player


# The media player
# eventually vlc as the backend
player = Player()


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
                "Believer",
                "https://aac.saavncdn.com/248/a6b1b78b396245f712abda8f1daefee0_96.mp4",
            )
        ]
        menu = self.app.query_one(SelectionMenu)
        menu.data = song_data


class SelectionMenu(Widget):
    """
    Shows a selection menu on ui.
    For music selection.
    """

    data = reactive([], layout=True)

    def compose(self) -> ComposeResult:
        yield ScrollableContainer()

    @on(RadioSet.Changed)
    def radio_button_pressed(self, event: RadioSet.Changed) -> None:
        selected_index = event.index
        selected_song = self.data[selected_index]
        url = selected_song[1]
        playing = player.play(url)
        if not playing:
            self.app.query_one(NowPlaying).song_info = selected_song[0]
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


class NowPlaying(Static):

    song_info = reactive("", layout=True)
    player_status = reactive("", layout=True)

    def compose(self) -> ComposeResult:
        yield Label("Not Playing Anything...")

    def watch_song_info(self) -> None:
        if not self.song_info:
            return
        self.query_one(Label).update(f"|| | {self.song_info}")


class MainLayout(Static):
    """
    Main layout of the app
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True, priority=True),
    ]

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

    def action_quit(self):
        self.app.exit()
