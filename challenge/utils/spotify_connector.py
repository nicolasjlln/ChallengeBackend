# coding: utf-8

from datetime import datetime
import requests
import threading
from functools import wraps
import time

from challenge.models import Artist, Album
from challenge.utils import SpotifySession, spotify_auth, slugify_model

import logging

logger = logging.getLogger(__name__)


def check_token_expiry(func: callable):
    """ Wrapper checking token expiry date and refresh it if needed."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        session = args[0].session
        if datetime.now() >= session.expiry_date:
            logger.warning("User session token expired, refreshing.")
            session.refresh_auth_token()

        return func(*args, **kwargs)

    return wrapper


class SpotifyConnector:
    """
    Spotify Connector.
    Retreive and save data from spotify API with user session.
    """

    # Spotify API entry to get new releases
    NEW_RELEASES_URL = "https://api.spotify.com/v1/browse/new-releases"

    def __init__(self, session: SpotifySession):
        """ Inits connector with user session. """
        self.session = session

    @classmethod
    def from_usercode(cls, code):
        session_infos = spotify_auth.get_user_auth(code=code)
        session = SpotifySession(**session_infos)
        return cls(session=session)

    @check_token_expiry
    def get_new_releases(self):
        """ Safely get new releases. """
        try:
            self._get_new_releases()
        except Exception as e:
            logger.error(
                "Something wrong happened while getting new releases. "
                f"Exception: {e}"
            )

    def _get_new_releases(self):
        """
        Requests new releases (albums) from Spotify API and store it in
        database.
        """
        next_url = self.NEW_RELEASES_URL
        threads = list()
        while next_url:
            albumns_infos = self._retreive_new_releases(url=next_url)

            next_url = albumns_infos.pop("next")

            # Async data import
            thread = threading.Thread(
                target=self._extract_albums_data,
                kwargs={'albums': albumns_infos.get("items")}
            )
            thread.start()
            threads.append(thread)

        # Wait until all imports are done
        for thread in threads:
            thread.join()

    def _retreive_new_releases(self, url: str):
        response = self.__perform_request(url=url, limit=50)

        if response.status_code != 200:
            raise RuntimeError(
                "Error while retreiving new releases. "
                f"Status code -> {response.status_code}"
            )

        return response.json().get("albums")

    def __perform_request(self, url: str, **params):
        """ Performs requests with right authentication headers. """
        return requests.get(
            url=url,
            params=params,
            headers={"Authorization": f"Bearer {self.session.token}"},
        )

    def _extract_albums_data(self, albums: list):
        """ Identify albums and artists while redirecting data for storage. """
        for album in albums:
            artists_id = self._save_artists(artists_data=album.get("artists"))
            self._save_album(album_data=album, artists_by_name=artists_id)

    def _save_artists(self, artists_data: list) -> dict:
        """ Extract artists from given data and store them in database. """
        artists = dict()
        for artist_data in artists_data:
            artist, _ = Artist.objects.get_or_create(
                slug=slugify_model(model=artist_data),
                name=artist_data.get("name"),
                artist_type=artist_data.get("type"),
            )

            # Storing artist id by name
            artists[artist.name] = artist.id

        return artists

    def _save_album(self, album_data: dict, artists_by_name: dict):
        """ Extract albums from given data and store them in database. """
        album, _ = Album.objects.get_or_create(
            slug=slugify_model(model=album_data),
            name=album_data.get("name"),
            album_type=album_data.get("album_type"),
            type=album_data.get("type"),
            release_date=album_data.get("release_date"),
            release_date_precision=album_data.get("release_date_precision"),
            total_tracks=album_data.get("total_tracks"),
        )
        album.artists.add(
            *[
                artists_by_name[artist["name"]]
                for artist in album_data.get("artists", [])
            ]
        )
