# coding: utf-8

from django.shortcuts import redirect  # , render

from .utils import spotify_auth, SpotifySession, SpotifyConnector

# from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from challenge.serializers import (
    # UserSerializer,
    # GroupSerializer,
    ArtistSerializer,
)
from challenge.models import Artist


class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that retreive artists informations about its new releases on
    spotify.
    """

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    # permission_classes = [permissions.IsAuthenticated]


def home(request):
    return redirect(spotify_auth.get_user())


def spotify_callback(request):
    code = request.GET.get("code")

    if not code:
        pass

    session_infos = spotify_auth.get_user_auth(code=code)
    session = SpotifySession(**session_infos)

    spotify_conn = SpotifyConnector(session=session)
    spotify_conn.get_new_releases()

    return redirect("http://localhost:5000/api/")
