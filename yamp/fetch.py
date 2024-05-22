from requests import get
from requests.exceptions import ConnectionError


class Fetch:
    _saavn_url = "https://saavn.dev/api"

    # Fetch from saavn
    def fetch_saavn(self, query: str) -> list:
        songs = []
        search_url = self._saavn_url + f"/search/songs?query={query}"
        try:
            res = get(search_url)
            res_data = res.json()

        except ConnectionError:
            error_text = "[bold][red]Connection Error[/red][/b] - Check Your Internet"
            return [error_text]

        results = res_data["data"]["results"]
        # Append songs info such as stream url, song name and artist name - in the songs list
        for result in results:
            stream_url = result["downloadUrl"][-2]
            song_name = result["name"]
            song_artist = result["artists"]["primary"][0]["name"]
            title = f"{song_artist} - {song_name}"
            stream_info = {
                "name": song_name,
                "artist": song_artist,
                "url": stream_url["url"],
            }
            data_tuple = (title, stream_info)
            songs.append(data_tuple)

        return songs
