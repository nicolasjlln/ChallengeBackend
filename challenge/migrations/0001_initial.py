# Generated by Django 3.1.2 on 2020-10-15 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.CharField(max_length=150, unique=True)),
                ("name", models.CharField(max_length=100)),
                ("artist_type", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.CharField(max_length=150, unique=True)),
                ("name", models.CharField(max_length=100)),
                ("album_type", models.CharField(max_length=50)),
                ("type", models.CharField(max_length=50)),
                ("release_date", models.CharField(max_length=50)),
                ("release_date_precision", models.CharField(max_length=20)),
                ("total_tracks", models.SmallIntegerField()),
                ("artists", models.ManyToManyField(to="challenge.Artist")),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
    ]
