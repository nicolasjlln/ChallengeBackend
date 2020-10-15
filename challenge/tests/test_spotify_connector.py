# coding: utf-8

import json
from pathlib import Path
from datetime import datetime
from dateutils import relativedelta

from django.test import TestCase
from unittest.mock import patch, MagicMock
from challenge.utils import SpotifyConnector, SpotifySession
from challenge.models import Album, Artist


TESTS_PATH = Path().cwd() / "challenge" / "tests"


@patch("challenge.utils.spotify_connector.requests")
class SpotifyConnectorTestCase(TestCase):
    """ Tests about SpotifyConnector object. """

    def setUp(self):
        self.session = SpotifySession(
            access_token="access_token",
            expires_in=3600,
            refresh_token="refresh_token",
        )
        self.FAKE_DATA = json.loads(
            (TESTS_PATH / "new_releases_data.json").read_text()
        )

    def test_get_new_releases(self, fake_requests):
        """ Checks if objects are properly inserted from raw data. """
        conn = SpotifyConnector(session=self.session)

        # Mocking requests response
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json = MagicMock(return_value=self.FAKE_DATA)
        fake_requests.get = MagicMock(return_value=fake_response)

        conn.get_new_releases()

        fake_requests.get.assert_called_once()

        self.assertEquals(Artist.objects.count(), 5)
        self.assertEquals(Album.objects.count(), 2)

    def test_get_new_releases_token_expired(self, fake_requests):
        """ Checks if session token is properly handled. """
        fake_session = MagicMock()
        fake_session.expiry_date = datetime.utcnow()  # Token should be expired
        conn = SpotifyConnector(session=fake_session)

        # Mocking requests response
        fake_response = MagicMock()
        fake_response.json = MagicMock(return_value=self.FAKE_DATA)
        fake_response.status_code = 200
        fake_requests.get = MagicMock(return_value=fake_response)

        # Assert logs at WARNING level if token is expired
        with self.assertLogs(level="WARNING"):
            conn.get_new_releases()

        fake_session.refresh_auth_token.assert_called_once()
        fake_requests.get.assert_called_once()

        self.assertEquals(Artist.objects.count(), 5)
        self.assertEquals(Album.objects.count(), 2)

    def test_get_new_releases_exception_happens(self, fake_requests):
        """ Checks if session token is properly handled. """
        with patch.object(SpotifyConnector, "_get_new_releases") as fake_meth:
            fake_meth = MagicMock(side_effets=[Exception("any")])  # NOQA
            conn = SpotifyConnector(session=self.session)

        # Assert connector logs at ERROR level if token is expired
        with self.assertLogs(level="ERROR"):
            conn.get_new_releases()
