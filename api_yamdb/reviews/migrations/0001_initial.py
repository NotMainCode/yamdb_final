# Generated by Django 2.2.28 on 2022-12-28 06:10

import django.core.validators
import django.db.models.deletion
import reviews.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="Enter a category",
                        max_length=256,
                        verbose_name="Category",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Enter the category URL",
                        unique=True,
                        verbose_name="Category URL",
                    ),
                ),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
                "ordering": ("name", "slug"),
            },
        ),
        migrations.CreateModel(
            name="Comment",
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
                (
                    "text",
                    models.TextField(
                        help_text="Enter the comment text",
                        verbose_name="Comment text",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Comment date",
                    ),
                ),
            ],
            options={
                "verbose_name": "comment",
                "verbose_name_plural": "comments",
                "ordering": ("pub_date",),
            },
        ),
        migrations.CreateModel(
            name="Genre",
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
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="Enter the genre",
                        max_length=256,
                        verbose_name="Genre",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Enter the genre URL",
                        unique=True,
                        verbose_name="Genre URL",
                    ),
                ),
            ],
            options={
                "verbose_name": "genre",
                "verbose_name_plural": "genres",
                "ordering": ("name", "slug"),
            },
        ),
        migrations.CreateModel(
            name="Review",
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
                (
                    "text",
                    models.TextField(
                        help_text="Write the review",
                        verbose_name="Review text",
                    ),
                ),
                (
                    "score",
                    models.PositiveSmallIntegerField(
                        help_text="Rate the creation from 1 to 10",
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, "Enter a rating from 1 to 10"
                            ),
                            django.core.validators.MaxValueValidator(
                                10, "Enter a rating from 1 to 10"
                            ),
                        ],
                        verbose_name="Rating",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Review date",
                    ),
                ),
            ],
            options={
                "verbose_name": "review",
                "verbose_name_plural": "reviews",
                "ordering": ("pub_date",),
            },
        ),
        migrations.CreateModel(
            name="Title",
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
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        help_text="Enter the title",
                        max_length=256,
                        verbose_name="Title",
                    ),
                ),
                (
                    "year",
                    models.PositiveIntegerField(
                        help_text="Enter the release year",
                        validators=[reviews.validators.validate_year],
                        verbose_name="Release year",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Enter a description (not necessary)",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Select a category",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="reviews.Category",
                        verbose_name="Category",
                    ),
                ),
                (
                    "genre",
                    models.ManyToManyField(
                        help_text="Select a genre",
                        to="reviews.Genre",
                        verbose_name="Genres",
                    ),
                ),
            ],
            options={
                "verbose_name": "title",
                "verbose_name_plural": "titles",
                "ordering": ("name",),
            },
        ),
    ]
