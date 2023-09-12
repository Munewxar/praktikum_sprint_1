CREATE SCHEMA content;

CREATE TABLE "content"."film_work" (
    "created" timestamp with time zone NOT NULL, 
    "modified" timestamp with time zone NOT NULL, 
    "id" uuid NOT NULL PRIMARY KEY, 
    "title" varchar(255) NOT NULL, 
    "description" text NOT NULL, 
    "creation_date" date NOT NULL, 
    "rating" double precision NOT NULL, 
    "type" varchar(10) NOT NULL
    );

CREATE TABLE "content"."genre" (
    "created" timestamp with time zone NOT NULL, 
    "modified" timestamp with time zone NOT NULL, 
    "id" uuid NOT NULL PRIMARY KEY, 
    "name" varchar(255) NOT NULL, 
    "description" text NOT NULL
    );

CREATE TABLE "content"."person" (
    "created" timestamp with time zone NOT NULL, 
    "modified" timestamp with time zone NOT NULL, 
    "id" uuid NOT NULL PRIMARY KEY, 
    "full_name" varchar(255) NOT NULL
    );

CREATE TABLE "content"."person_film_work" (
    "id" uuid NOT NULL PRIMARY KEY, 
    "role" text NULL, 
    "created" timestamp with time zone NOT NULL, 
    "film_work_id" uuid NOT NULL, 
    "person_id" uuid NOT NULL
    );

CREATE TABLE "content"."genre_film_work" (
    "id" uuid NOT NULL PRIMARY KEY, 
    "created" timestamp with time zone NOT NULL, 
    "film_work_id" uuid NOT NULL, 
    "genre_id" uuid NOT NULL
    );


ALTER TABLE "content"."person_film_work" 
    ADD CONSTRAINT "person_film_work_film_work_id_1724c536_fk_film_work_id" 
    FOREIGN KEY ("film_work_id") REFERENCES "content"."film_work" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "content"."person_film_work" 
    ADD CONSTRAINT "person_film_work_person_id_196d24de_fk_person_id" 
    FOREIGN KEY ("person_id") REFERENCES "content"."person" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "person_film_work_film_work_id_1724c536" ON "content"."person_film_work" ("film_work_id");
CREATE INDEX "person_film_work_person_id_196d24de" ON "content"."person_film_work" ("person_id");

ALTER TABLE "content"."genre_film_work" 
    ADD CONSTRAINT "genre_film_work_film_work_id_65abe300_fk_film_work_id" 
    FOREIGN KEY ("film_work_id") REFERENCES "content"."film_work" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "content"."genre_film_work" 
    ADD CONSTRAINT "genre_film_work_genre_id_88fbcf0d_fk_genre_id" 
    FOREIGN KEY ("genre_id") REFERENCES "content"."genre" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "genre_film_work_film_work_id_65abe300" ON "content"."genre_film_work" ("film_work_id");
CREATE INDEX "genre_film_work_genre_id_88fbcf0d" ON "content"."genre_film_work" ("genre_id");

ALTER TABLE "content"."genre_film_work"
    ADD CONSTRAINT "genre_film_work_film_work_id_genre_id_uniq"
    UNIQUE ("film_work_id", "genre_id");

ALTER TABLE "content"."genre"
    ADD CONSTRAINT "genre_name_uniq"
    UNIQUE ("name");
