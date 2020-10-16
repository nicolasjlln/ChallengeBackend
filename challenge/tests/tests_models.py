# coding: utf-8

from django.test import TestCase
from django.db.utils import IntegrityError
from challenge.models import Artist, Album
from django.db import transaction


class ArtistTestCase(TestCase):
    """ Tests about Artist model. """

    def setUp(self):
        Artist.objects.create(
            name="any_artist", slug="slug-test-12345", artist_type="artist"
        )

    def test_only_one_artist(self):
        """Only one artist created."""
        self.assertEqual(Artist.objects.count(), 1)

    def test_artist_str(self):
        """Artists are properly represented."""
        artist = Artist.objects.get(name="any_artist")
        self.assertEqual(str(artist), "any_artist")

    def test_slug_unicity(self):
        """ Checks records are actually unique. """
        with self.assertRaises(IntegrityError):
            # otherwise other queries won't work because of the thrown exception
            with transaction.atomic():
                Artist.objects.create(
                    slug="slug-test-12345",  # same slug
                    name="other_artist",  # different name
                    artist_type="artist",
                )

        try:
            Artist.objects.create(
                slug="other slug",  # different slug
                name="other_artist",  # different name
                artist_type="artist",
            )
        except Exception as e:
            self.fail(e)

    def tearDown(self):
        Artist.objects.all().delete()


class AlbumsTestCase(TestCase):
    """ Tests about Album model. """

    def test_album_creation_from_artist(self):
        artist = Artist.objects.create(
            name="any_artist", slug="slug-test-12345", artist_type="artist"
        )
        album = Album(
            slug="slug-test-12345",
            album_type="album_type",
            type="type",
            name="name",
            release_date="any",
            release_date_precision="any",
            total_tracks=1,
        )
        album.save()

        try:
            # artist<->album link creation
            album.artists.add(artist)
        except Exception as e:
            self.fail(e)

        # Assert insertion succeed
        self.assertEquals(Album.objects.count(), 1)

        # Assert artists properly linked
        self.assertEquals(album.artists.count(), 1)
        self.assertEquals(album.artists.first().id, artist.id)

        # Try to check album->artist link exists
        albums = Artist.objects.get(id=artist.id).album_set.all()
        self.assertEquals(len(albums), 1)
        self.assertEquals(albums[0].id, album.id)

    def test_slug_unicity(self):
        """ Checks records are actually unique. """
        slug = "any-slug"
        Album.objects.create(
            slug=slug,
            album_type="album_type",
            type="type",
            name="name",
            release_date="any",
            release_date_precision="any",
            total_tracks=1,
        )
        with self.assertRaises(IntegrityError):
            # otherwise other queries won't work because of the thrown exception
            with transaction.atomic():
                Album.objects.create(
                    slug=slug,  # same slug
                    name="other name",  # different name
                    album_type="album_type",
                    type="type",
                    release_date="any",
                    release_date_precision="any",
                    total_tracks=1,
                )

        try:
            Album.objects.create(
                slug="other slug",  # different slug
                name="other name",  # different name
                album_type="album_type",
                type="type",
                release_date="any",
                release_date_precision="any",
                total_tracks=1,
            )
        except Exception as e:
            self.fail(e)

    def remove_all(self):
        Artist.objects.all().delete()
        Album.objects.all().delete()

    def tearDown(self):
        self.remove_all()
