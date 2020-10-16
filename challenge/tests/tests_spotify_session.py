# coding: utf-8

from datetime import datetime
from dateutils import relativedelta
from freezegun import freeze_time
from unittest.mock import patch, MagicMock
from copy import copy

from django.test import TestCase
from challenge.utils import SpotifySession


class SpotifySessionTestCase(TestCase):
    """ Tests about SpotifySession object. """

    def setUp(self):
        self.now = datetime.utcnow()
        with freeze_time(self.now):
            self.session = SpotifySession(
                access_token="access_token",
                expires_in=3600,
                refresh_token="refresh_token",
            )

    def test_expiry_converted_properly(self):
        expected_expiry = self.now + relativedelta(seconds=3600)
        self.assertEquals(self.session.expiry_date, expected_expiry)

    @patch("challenge.utils.spotify_session.spotify_auth")
    def test_token_refresh(self, fake_auth):
        """Only one artist created."""
        now = datetime.utcnow()

        fake_auth.refresh_auth = MagicMock(
            return_value={
                "access_token": "any",
                "expires_in": 0,
                "refresh_token": "any",
            }
        )

        # save session
        session = copy(self.session)

        # refresh token
        with freeze_time(now):
            session.refresh_auth_token()

        # check results
        fake_auth.refresh_auth.assert_called_once_with(
            refresh_token=self.session.refresh_token
        )
        self.assertEquals(session.token, "any")
        self.assertEquals(session.expiry_date, now)
        self.assertEquals(session.refresh_token, "any")
