# coding: utf-8

from datetime import datetime
from dateutils import relativedelta
from . import spotify_auth


class SpotifySession:
    def __init__(self, access_token, expires_in, refresh_token):
        self._refresh_session(
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
        )

    def _refresh_session(
        self, access_token: str, expires_in: int, refresh_token: str
    ):
        self.token = access_token
        self.expiry_date = datetime.utcnow() + relativedelta(seconds=expires_in)
        self.refresh_token = refresh_token

    def refresh_auth_token(self):
        session_infos = spotify_auth.refresh_token(self.refresh_token)
        self._refresh_session(**session_infos)
