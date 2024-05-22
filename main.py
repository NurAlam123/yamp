from textual.app import App
from textual.widgets import Label, Input
from textual.containers import (
    Vertical,
    ScrollableContainer,
    Container,
    Horizontal,
    Grid,
)

from yamp.utils import splash


class YAMP(App):
    CSS_PATH = "./style.tcss"

    def compose(self):
        yield Label(splash())
        yield Input(placeholder="Type song name...")
        yield Horizontal(
            Vertical(
                Label("Songs", classes="sub-container-label", expand=True),
                ScrollableContainer(Label("No songs to display!")),
                classes="sub-container",
            ),
            Vertical(
                Label("Queue", classes="sub-container-label", expand=True),
                ScrollableContainer(Label("No songs to display!")),
                classes="sub-container",
            ),
            Vertical(
                Label("History", classes="sub-container-label", expand=True),
                ScrollableContainer(Label("No songs to display!")),
                classes="sub-container",
            ),
            id="interactive-container",
        )


if __name__ == "__main__":
    app = YAMP()
    app.run()
