from __future__ import annotations

import time
from typing import Iterable, Optional

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube"]  # manage playlists

class YoutubeClient:
    def __init__(self, client_secret_file: str,
                 tracks: Iterable[tuple[str, str]],
                 playlist_title: str,
                 playlist_description: str, privacy: str) -> None:
        self.client_secret_file = client_secret_file
        self.playlist_title = playlist_title
        self.tracks = tracks
        self.playlist_description = playlist_description
        self.privacy = privacy
        self.yt = self._youtube_client()

    def _youtube_client(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secret_file, SCOPES)
        creds = flow.run_local_server(port=0)
        return build("youtube", "v3", credentials=creds)

    def _search_video_id(self, query: str) -> Optional[str]:
        """
        Returns the first matching YouTube videoId for a query like:
        'Bee Gees Stayin' Alive official audio'
        """
        resp = self.yt.search().list(
            part="id",
            q=query,
            type="video",
            maxResults=1,
            safeSearch="none",
        ).execute()

        items = resp.get("items", [])
        if not items:
            return None
        return items[0]["id"]["videoId"]

    def _create_playlist(self, title: str, description: str = "", privacy: str = "private") -> str:
        resp = self.yt.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {"title": title, "description": description},
                "status": {"privacyStatus": privacy},  # private / unlisted / public
            },
        ).execute()
        return resp["id"]

    def _add_video_to_playlist(self, video_id: str, playlist_id) -> None:
        self.yt.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            },
        ).execute()

    def build_playlist_from_tracks(self):

        playlist_id = self._create_playlist(self.playlist_title,
                                           self.playlist_description,
                                           self.privacy)

        print("Created playlist:", playlist_id)

        missing = []
        for song, artist in self.tracks:
            # You can tweak this query string to improve matches
            q = f'{artist} "{song}" official audio'
            try:
                vid = self._search_video_id(q)
                if not vid:
                    missing.append((song, artist))
                    print("No match:", artist, "-", song)
                    continue

                self._add_video_to_playlist(vid, playlist_id)
                print("Added:", artist, "-", song, "->", vid)

                # small pause to be polite / reduce rate limit issues
                time.sleep(0.1)

            except HttpError as e:
                # If quota or transient error, you can log and continue
                print("Error on:", artist, "-", song, ":", e)
                missing.append((song, artist))

        print("\nDone. Missing:", len(missing))
        for song, artist in missing[:10]:
            print("  -", artist, "-", song)

        return playlist_id, missing

# Example input (song, artist)
trackss = [
    ("Stayin' Alive", "Bee Gees"),
    ("Short People", "Randy Newman"),
    ("Baby Come Back", "Player"),
]

