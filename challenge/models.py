# coding: utf-8

from django.db import models
from challenge.utils import slugify_model

#########
# It was not possible to use a `unique_together` Meta option for the models
# because the DB does not support it.
# Then unique `slug` seamed to be the proper way to make records unique.
#########


class AbstractSpotifyModel(models.Model):
    """
    Abstract model for data from Spotify API. Any data from Spotify API includes
    a `name` and an `id` fields.
    A `slug` field is built on both to differenciate records in database.

    The `id` from Spotify is supposed unique, then an artist with the same
    `name` AND `id` fields should be considered as a duplicate record.
    """

    # Slug field is based on the artist name and its spotiy id
    slug = models.CharField(max_length=150, unique=True, blank=False)
    name = models.CharField(max_length=100, blank=False)

    class Meta:
        abstract = True
        ordering = ["name"]


class Artist(AbstractSpotifyModel):
    """ Artist model """

    artist_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Album(AbstractSpotifyModel):
    """ Album model """

    album_type = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    release_date = models.CharField(max_length=50)
    release_date_precision = models.CharField(max_length=20)
    total_tracks = models.SmallIntegerField()

    # Many to many key with Artist model
    artists = models.ManyToManyField(Artist)

    @classmethod
    def save_albums(cls, albums):
        """ Identify albums and artists while redirecting data for storage. """
        for album in albums:
            artists_id = cls._save_artists(artists_data=album.get("artists"))
            cls._save_album(album_data=album, artists_by_name=artists_id)

    @classmethod
    def _save_artists(cls, artists_data: list) -> dict:
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

    @classmethod
    def _save_album(cls, album_data: dict, artists_by_name: dict):
        """ Extract albums from given data and store them in database. """
        album, _ = cls.objects.get_or_create(
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
