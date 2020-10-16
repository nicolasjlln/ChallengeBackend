# coding: utf-8

from django.test import TestCase
from challenge.utils.models import slugify_model


class ModelsUtilsFunctionsTestCase(TestCase):
    """ Tests about Models utils functions. """

    def test_slugify_model(self):
        """ Checks if object is properly 'slugified' from its name and id. """
        name = "Name F4Millynam€"
        id_ = "IDfromSP0TIFY"
        expectation = "name-f4millynam-idfromsp0tify"

        self.assertEquals(expectation, slugify_model({"name": name, "id": id_}))
