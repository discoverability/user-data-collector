# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, ForeignKeyConstraint, Index, String, Table, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Country(Base):
    __tablename__ = 'countries'

    id = Column(INTEGER(11), primary_key=True)
    code = Column(String(2), nullable=False)

    moviess = relationship(u'Movie', secondary=u'movies_has_countries')


class Director(Base):
    __tablename__ = 'directors'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    gender = Column(TINYINT(4))
    birthdate = Column(DateTime)
    nationality = Column(String(45))

    moviess = relationship(u'Movie', secondary=u'movies_has_directors')
    nationalitiess = relationship(u'Nationality', secondary=u'directors_has_nationalities')


class FilmGender(Base):
    __tablename__ = 'film_genders'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255))


class FilmNationality(Base):
    __tablename__ = 'film_nationalities'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255))

    filmss = relationship(u'Film', secondary=u'films_has_film_nationalities')


class Filmmaker(Base):
    __tablename__ = 'filmmakers'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), nullable=False)
    gender = Column(INTEGER(11), nullable=False)
    nationality = Column(String(255))

    filmss = relationship(u'Film', secondary=u'filmmakers_has_films')


class MovieType(Base):
    __tablename__ = 'movie_types'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)


class Nationality(Base):
    __tablename__ = 'nationalities'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))


t_directors_has_nationalities = Table(
    'directors_has_nationalities', metadata,
    Column('directors_id', ForeignKey(u'directors.id'), primary_key=True, nullable=False, index=True),
    Column('nationalities_id', ForeignKey(u'nationalities.id'), primary_key=True, nullable=False, index=True)
)


class Festival(Base):
    __tablename__ = 'festivals'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    year = Column(DateTime, nullable=False)
    countries_id = Column(ForeignKey(u'countries.id'), primary_key=True, nullable=False, index=True)

    countries = relationship(u'Country')
    filmss = relationship(u'Film', secondary=u'films_has_festivals')


class Film(Base):
    __tablename__ = 'films'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    title_fr = Column(String(255), nullable=False)
    title_inter = Column(String(45))
    retrospective = Column(TINYINT(4), server_default=text("'0'"))
    year = Column(DateTime)
    language = Column(String(45))
    filmscol = Column(String(45))
    film_genders_id = Column(ForeignKey(u'film_genders.id'), primary_key=True, nullable=False, index=True)

    film_genders = relationship(u'FilmGender')


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(INTEGER(11))
    description = Column(String(45))
    released_at = Column(DateTime)
    duration = Column(INTEGER(11))
    image = Column(LONGTEXT)
    movie_types_id = Column(ForeignKey(u'movie_types.id'), primary_key=True, nullable=False, index=True)
    netflix_id = Column(INTEGER(11))
    imdb_id = Column(INTEGER(11))

    movie_types = relationship(u'MovieType')


class FestivalSelectionName(Base):
    __tablename__ = 'festival_selection_names'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    festivals_id = Column(ForeignKey(u'festivals.id'), primary_key=True, nullable=False, index=True)

    festivals = relationship(u'Festival')


t_filmmakers_has_films = Table(
    'filmmakers_has_films', metadata,
    Column('filmmakers_id', ForeignKey(u'filmmakers.id'), primary_key=True, nullable=False, index=True),
    Column('films_id', INTEGER(11), primary_key=True, nullable=False),
    Column('films_film_genders_id', INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(['films_id', 'films_film_genders_id'], [u'films.id', u'films.film_genders_id']),
    Index('fk_filmmakers_has_films_films1_idx', 'films_id', 'films_film_genders_id')
)


t_films_has_festivals = Table(
    'films_has_festivals', metadata,
    Column('films_id', ForeignKey(u'films.id'), primary_key=True, nullable=False, index=True),
    Column('festivals_id', ForeignKey(u'festivals.id'), primary_key=True, nullable=False, index=True)
)


t_films_has_film_nationalities = Table(
    'films_has_film_nationalities', metadata,
    Column('films_id', INTEGER(11), primary_key=True, nullable=False),
    Column('films_film_genders_id', INTEGER(11), primary_key=True, nullable=False),
    Column('film_nationalities_id', ForeignKey(u'film_nationalities.id'), primary_key=True, nullable=False, index=True),
    ForeignKeyConstraint(['films_id', 'films_film_genders_id'], [u'films.id', u'films.film_genders_id']),
    Index('fk_films_has_film_nationalities_films1_idx', 'films_id', 'films_film_genders_id')
)


t_movies_has_countries = Table(
    'movies_has_countries', metadata,
    Column('movies_id', ForeignKey(u'movies.id'), primary_key=True, nullable=False, index=True),
    Column('countries_id', ForeignKey(u'countries.id'), primary_key=True, nullable=False, index=True)
)


t_movies_has_directors = Table(
    'movies_has_directors', metadata,
    Column('movies_id', ForeignKey(u'movies.id'), primary_key=True, nullable=False, index=True),
    Column('directors_id', ForeignKey(u'directors.id'), primary_key=True, nullable=False, index=True)
)


class FilmsHasFestivalSelectionName(Base):
    __tablename__ = 'films_has_festival_selection_names'

    films_id = Column(ForeignKey(u'films.id'), primary_key=True, nullable=False, index=True)
    festival_selection_names_id = Column(ForeignKey(u'festival_selection_names.id'), primary_key=True, nullable=False, index=True)
    total_awards = Column(String(45))

    festival_selection_names = relationship(u'FestivalSelectionName')
    films = relationship(u'Film')
