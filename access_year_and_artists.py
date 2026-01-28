"""
Retrieve song titles and artists from the Music Charts Archive singles chart.

This module defines a small scraper that fetches the singles chart page for a
given date and extracts song titles and artist names from the chart table.
"""

import requests
from bs4 import BeautifulSoup


# pylint: disable=too-few-public-methods
class GetArtists:
    """
    Scrape song titles and artist names from Music Charts Archive.

    The scraper downloads the singles chart for a specific date and parses the
    chart table to extract titles and artists.
    """

    def __init__(self, date: str, header: dict[str, str]) -> None:
        """
        Initialize the scraper.

        Args:
            date:
                Date portion of the chart URL (e.g. "1997-01-05").
            header:
                HTTP headers to send with the request (usually includes
                a User-Agent).
        """
        self.date = date
        self.header = header

    def get_all_artists(self):
        """
        Fetch the chart page and return all song titles and artists.

        Returns:
            A tuple containing:
                - A list of song titles
                - A list of artist names
        """
        url = f"https://musicchartsarchive.com/singles-chart/{self.date}"
        response = requests.get(
            url,
            headers=self.header,
            timeout=30,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        all_song_titles: list[str] = []
        all_song_artists: list[str] = []

        for row in soup.select("table.chart-table tr"):
            tds = row.find_all("td")
            # Expected columns: position | title | artist | ...
            if len(tds) >= 3:
                all_song_titles.append(tds[1].get_text(strip=True))
                all_song_artists.append(tds[2].get_text(strip=True))

        return all_song_titles, all_song_artists
