"""
YouTube playlist builder.

This module provides `YoutubeClient`, a small wrapper around the YouTube Data API v3
that authenticates a user, creates a playlist, searches for track videos, and adds
them to the playlist.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterable, Optional

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import Resource

SCOPES = ["https://www.googleapis.com/auth/youtube"]  # manage playlists


@dataclass(frozen=True, slots=True)
class YoutubePlaylistConfig:
    """
    Configuration for building a playlist from tracks.

    Args:
        client_secret_file:
            Path to the OAuth client secrets JSON file downloaded from
            Google Cloud Console.
        playlist_title:
            Title of the playlist to create.
        playlist_description:
            Description text for the playlist.
        privacy:
            Playlist privacy status: "private", "unlisted", or "public".
    """

    client_secret_file: str
    playlist_title: str
    playlist_description: str
    privacy: str


# pylint: disable=too-few-public-methods
class YoutubeClient:
    """
    Client for creating and populating a YouTube playlist from a list of tracks.

    This class handles OAuth authentication, playlist creation, video searching,
    and adding videos to a playlist using the YouTube Data API v3.

    Returns:
        Calling `build_playlist_from_tracks` returns a tuple containing:
            - The created playlist ID
            - A list of (song, artist) pairs that could not be added
    """

    def __init__(self, config: YoutubePlaylistConfig, tracks: Iterable[tuple[str, str]] ) -> None:
        """Initialize the client from a `YoutubePlaylistConfig` and authenticate."""
        self.config = config
        self.tracks = tracks
        self.yt: Resource = self._youtube_client()

    def _youtube_client(self) -> Resource:
        """Authenticate via OAuth and build a YouTube Data API client."""
        flow = InstalledAppFlow.from_client_secrets_file(
            self.config.client_secret_file, SCOPES
        )
        creds = flow.run_local_server(port=0)
        return build("youtube", "v3", credentials=creds)

    def _search_video_id(self, query: str) -> Optional[str]:
        """
        Search YouTube and return the first matching video ID.

        Returns None if no matching video is found.
        """
        # googleapiclient discovery resources are dynamic; pylint can't statically see members.
        resp = (
            self.yt.search()  # pylint: disable=no-member
            .list(
                part="id",
                q=query,
                type="video",
                maxResults=1,
                safeSearch="none",
            )
            .execute()
        )

        items = resp.get("items", [])
        if not items:
            return None
        return items[0]["id"]["videoId"]

    def _create_playlist(
        self,
        title: str,
        description: str = "",
        privacy: str = "private",
    ) -> str:
        """Create a new YouTube playlist and return its ID."""
        resp = (
            self.yt.playlists()  # pylint: disable=no-member
            .insert(
                part="snippet,status",
                body={
                    "snippet": {"title": title, "description": description},
                    "status": {"privacyStatus": privacy},
                },
            )
            .execute()
        )
        return resp["id"]

    def _add_video_to_playlist(self, video_id: str, playlist_id: str) -> None:
        """Add a video to an existing YouTube playlist."""
        (
            self.yt.playlistItems()  # pylint: disable=no-member
            .insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video_id},
                    }
                },
            )
            .execute()
        )

    def build_playlist_from_tracks(self):
        """
        Create the playlist and populate it using the configured tracks.

        Each track is searched on YouTube and the first matching result
        is added to the playlist. Tracks that cannot be matched or fail
        due to API errors are collected and returned.
        """
        cfg = self.config
        playlist_id = self._create_playlist(
            cfg.playlist_title,
            cfg.playlist_description,
            cfg.privacy,
        )

        print("Created playlist:", playlist_id)

        missing: list[tuple[str, str]] = []
        for song, artist in self.tracks:
            q = f'{artist} "{song}" official audio'
            try:
                vid = self._search_video_id(q)
                if not vid:
                    missing.append((song, artist))
                    print("No match:", artist, "-", song)
                    continue

                self._add_video_to_playlist(vid, playlist_id)
                print("Added:", artist, "-", song, "->", vid)

                time.sleep(0.1)

            except HttpError as exc:
                print("Error on:", artist, "-", song, ":", exc)
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

# Example config:
# config = YoutubePlaylistConfig(
#     client_secret_file="client_secret.json",
#     tracks=trackss,
#     playlist_title="My Playlist",
#     playlist_description="Created via API",
#     privacy="private",
# )
# client = YoutubeClient(config)
# playlist_id, missing = client.build_playlist_from_tracks()
