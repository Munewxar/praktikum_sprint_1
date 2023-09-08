CREATE SCHEMA content;

CREATE TABLE IF NOT EXISTS content.film_work (
id uuid PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
creation_date DATE,
rating FLOAT,
type TEXT not null,
created timestamp with time zone,
modified timestamp with time zone
);

CREATE INDEX film_work_title_index ON content.film_work (title);
CREATE INDEX film_work_creation_date_index ON content.film_work (creation_date);
CREATE INDEX film_work_rating_index ON content.film_work (rating);

CREATE TABLE IF NOT EXISTS content.genre (
id uuid PRIMARY KEY,
name TEXT NOT NULL,
description TEXT,
created timestamp with time zone,
modified timestamp with time zone
);

CREATE UNIQUE INDEX genre_name_index ON content.genre (name);

CREATE TABLE IF NOT EXISTS content.person (
id uuid PRIMARY KEY,
full_name TEXT NOT NULL,
created timestamp with time zone,
modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
id uuid PRIMARY KEY,
genre_id uuid references content.genre (id) ON DELETE CASCADE,
film_work_id uuid references content.film_work (id) ON DELETE CASCADE,
created timestamp with time zone);

CREATE INDEX genre_film_work_index ON content.genre_film_work (genre_id, film_work_id);

CREATE TABLE IF NOT EXISTS content.person_film_work (
id uuid PRIMARY KEY,
person_id uuid references content.person (id) ON DELETE CASCADE,
film_work_id uuid references content.film_work (id) ON DELETE CASCADE,
role text NOT NULL,
created timestamp with time zone);

CREATE INDEX gperson_film_work_index ON content.person_film_work (person_id, film_work_id);

