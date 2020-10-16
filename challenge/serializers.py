# coding: utf-8

from rest_framework import serializers
from challenge.models import Artist, Album


class AlbumSerializer(serializers.ModelSerializer):
    """ Album model Serializer. """

    class Meta:
        model = Album
        fields = [
            "album_type",
            "type",
            "name",
            "release_date",
            "release_date_precision",
            "total_tracks",
        ]
        read_only_fields = fields  # nothing can be updated manually


class ArtistSerializer(serializers.ModelSerializer):
    """ Artist model Serializer. """

    # Adding albums
    albums = AlbumSerializer(source="album_set", many=True)

    class Meta:
        model = Artist
        fields = ["name", "artist_type", "albums"]
        read_only_fields = fields  # nothing can be updated manually
