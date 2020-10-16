# coding: utf-8

import requests
from datetime import datetime
from functools import wraps

from challenge.utils import SpotifySession, spotify_auth

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
        from challenge.models import Album

        next_url = self.NEW_RELEASES_URL
        while next_url:
            albumns_infos = self._retreive_new_releases(url=next_url)
            next_url = albumns_infos.pop("next")
            Album.save_albums(albums=albumns_infos.get("items"))

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
