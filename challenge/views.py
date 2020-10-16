# coding: utf-8

import logging

from rest_framework import viewsets
from django.shortcuts import redirect
from django.views.generic.base import RedirectView

from challenge.serializers import ArtistSerializer
from challenge.models import Artist
from .utils import spotify_auth, SpotifyConnector


logger = logging.getLogger(__name__)

USER_AUTH_URL = spotify_auth.get_user()


class HomeRedirect(RedirectView):
    """ This is home page. User get to Spotify auth page directly. """

    url = USER_AUTH_URL


def spotify_callback(request):
    """
    This is the Spotify auth callback page.
    When the user is properly authenticated, data is fetched from Spotify API
    and user is redirected to the project API.
    """
    code = request.GET.get("code")

    if not code:
        logger.error("No code found in Spotify API callback. Retrying.")
        return redirect(USER_AUTH_URL)

    spotify_conn = SpotifyConnector.from_usercode(code=code)
    spotify_conn.get_new_releases()

    return redirect("/api/")


class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that retreive artists informations about its new releases on
    spotify.
    """

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
