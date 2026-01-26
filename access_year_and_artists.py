import requests
from bs4 import BeautifulSoup
# date = input('Which Year do you want to travel to? Type the date in this format YYYY-MM-DD' )

class GetArtists:
    def __init__(self, date, header):
        self.date = date
        self.header = header


    def get_all_artists(self):
        url = f'https://musicchartsarchive.com/singles-chart/{self.date}'
        response = requests.get(url, headers=self.header)
        soup = BeautifulSoup(response.text, 'html.parser')

        all_song_titles = []
        all_song_artists = []
        for row in soup.select("table.chart-table tr"):
            tds = row.find_all("td")
            if len(tds) >= 2:
                all_song_titles.append(tds[1].get_text(strip=True))
                all_song_artists.append(tds[2].get_text(strip=True))

        return all_song_titles, all_song_artists