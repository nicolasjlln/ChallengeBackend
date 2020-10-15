# coding: utf-8

from django.db import models

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
        ordering = ['name']


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
