from textual.app import App, ComposeResult
from textual.app import ComposeResult
from textual.widgets import Footer

from yamp.layout import MainLayout


class YAMP(App[None]):
    CSS_PATH = "./style/global.tcss"
    

    def compose(self) -> ComposeResult:
        yield MainLayout()


if __name__ == "__main__":
    app = YAMP()
    app.run()
