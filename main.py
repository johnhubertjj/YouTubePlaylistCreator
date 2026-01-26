from access_year_and_artists import GetArtists
from access_youtube import YoutubeClient

# date = input('Which Year do you want to travel to? Type the date in this format YYYY-MM-DD' )

date = '1978-02-04'
header = {'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                        'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15'}

artists = GetArtists(date, header)
artist_names = artists.get_all_artists()

print(artist_names)

# # Example input (song, artist)
# trackss = [
#     ("Stayin' Alive", "Bee Gees"),
#     ("Short People", "Randy Newman"),
#     ("Baby Come Back", "Player"),
# ]

tracks = list(zip(artist_names[0], artist_names[1]))

youtube_client = YoutubeClient(client_secret_file="client_secret.json", tracks=tracks,
                               playlist_title="Singles Chart 1978-02-04",
                               playlist_description="Auto-generated from extracted chart HTML.",
                               privacy="unlisted")

youtube_client.build_playlist_from_tracks()
