# coding: utf-8

from django.utils.text import slugify


def slugify_model(model):
    """
    Slugify model with its name and spotify id (this id is supposed unique).
    """
    to_slugify = f"{model.get('name')} {model.get('id')}"
    return slugify(to_slugify)
