from pyfiglet import Figlet
from . import __title__, __sub_title__, __version__, __description__
from typing import Optional


def splash() -> str:
    fig = Figlet(font="big")
    fig_text = fig.renderText(__title__)
    heading = f"[#0000ff]{fig_text}[/]\n[#ffaf00]{__sub_title__}[/]\n"
    sub_heading = f"[b]{__title__}[/b] @ {__version__}"
    ps = "[#808080]An online music player that no one asked for. :)\nThough Enjoy![/]\n"
    text = f"{heading}\n{sub_heading}\n{ps}\n"
    return text


def time_formatter(time: Optional[str | int]) -> str:
    # time = ms // 1000
    sec = time % 60
    minute = time // 60
    if sec < 10:
        sec = "0" + str(sec)
    else:
        sec = str(sec)

    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)

    return f"{minute}:{sec}"
