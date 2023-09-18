import uuid
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)


    def __str__(self):
        return self.name 


    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('Full name'), max_length=255)


    def __str__(self):
        return self.full_name


    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmworkType(models.TextChoices):
        MOVIE = 'MOVIE', _('Movie')
        TV_SHOW = 'TV_SHOW', _('Tv show')


    title = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    creation_date = models.DateField(_('Creation date'), blank=True, null=True)
    rating = models.FloatField(_('Rating'), null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(_('Type'), max_length=10, choices=FilmworkType.choices, default=FilmworkType.MOVIE)

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')


    def __str__(self):
        return self.title 


    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Genres')

        constraints = [
            models.UniqueConstraint('film_work', 'genre', \
                name='genre_film_work_film_work_genre_uniq'),
        ]


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('Role'), null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Persons')

        constraints = [
            models.UniqueConstraint('film_work', 'person', 'role', \
                name='person_film_work_film_work_person_role_uniq'),
        ]