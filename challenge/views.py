# coding: utf-8

from django.shortcuts import redirect  # , render

from .utils import spotify_auth, SpotifySession, SpotifyConnector

from rest_framework import viewsets
from challenge.serializers import (
    ArtistSerializer,
)
from challenge.models import Artist

import logging

logger = logging.getLogger(__name__)


class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that retreive artists informations about its new releases on
    spotify.
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


def home(request):
    """ This is home page. User get to Spotify auth page directly. """
    return redirect(spotify_auth.get_user())


def spotify_callback(request):
    """
    This is the Spotify auth callback page.
    When the user is properly authenticated, data is fetched from Spotify API
    and user is redirected to the project API.
    """
    code = request.GET.get("code")

    if not code:
        logger.error("No code found in Spotify API callback. Retrying.")
        return redirect(spotify_auth.get_user())

    session_infos = spotify_auth.get_user_auth(code=code)
    session = SpotifySession(**session_infos)

    spotify_conn = SpotifyConnector(session=session)
    spotify_conn.get_new_releases()

    return redirect('/api/')
