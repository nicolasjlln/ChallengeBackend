# coding: utf-8

import base64
import json
import requests
import os


class SpotifyAuth(object):
    SPOTIFY_URL_AUTH = "https://accounts.spotify.com/authorize/"
    SPOTIFY_URL_TOKEN = "https://accounts.spotify.com/api/token/"
    RESPONSE_TYPE = "code"
    HEADER = "application/x-www-form-urlencoded"
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    CALLBACK_URL = "http://localhost:5000/auth/callback"
    SCOPE = "user-read-email user-read-private"

    def _get_auth_url(self, client_id, redirect_uri, scope):
        return (
            f"{self.SPOTIFY_URL_AUTH}"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope={scope}"
            f"&response_type={self.RESPONSE_TYPE}"
        )

    def _get_token(self, code, client_id, client_secret, redirect_uri):
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        headers = self._get_headers()

        post = requests.post(
            self.SPOTIFY_URL_TOKEN, params=body, headers=headers
        )
        return self._handle_token(json.loads(post.text))

    def _handle_token(self, response):
        if "error" in response:
            return response
        return {
            key: response[key]
            for key in ["access_token", "expires_in", "refresh_token"]
        }

    def _get_headers(self):
        encoded = base64.b64encode(
            f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()
        ).decode()

        return {
            "Content-Type": self.HEADER,
            "Authorization": f"Basic {encoded}",
        }

    def refresh_auth(self, refresh_token):
        body = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        headers = self._get_headers()

        post_refresh = requests.post(
            self.SPOTIFY_URL_TOKEN, data=body, headers=headers
        )
        p_back = json.dumps(post_refresh.text)

        return self._handle_token(p_back)

    def get_user(self):
        return self._get_auth_url(
            client_id=self.CLIENT_ID,
            redirect_uri=self.CALLBACK_URL,
            scope=self.SCOPE,
        )

    def get_user_auth(self, code):
        return self._get_token(
            code=code,
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            redirect_uri=self.CALLBACK_URL,
        )
