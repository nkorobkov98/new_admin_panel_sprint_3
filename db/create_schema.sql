CREATE SCHEMA IF NOT EXISTS content;


CREATE TABLE IF NOT EXISTS content.film_work (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid PRIMARY KEY,
    title VARCHAR (200) NOT NULL,
    description TEXT NOT NULL,
    creation_date DATE NOT NULL,
    rating FLOAT,
    type VARCHAR(15) NOT NULL
);


CREATE TABLE IF NOT EXISTS content.person (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL
);


CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    role VARCHAR(15),
    created timestamp with time zone NOT NULL,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    person_id uuid NOT NULL REFERENCES content.person(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS content.genre (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    id uuid PRIMARY KEY,
    name VARCHAR (100) NOT NULL UNIQUE,
    description TEXT
);


CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    created timestamp with time zone NOT NULL,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    genre_id uuid NOT NULL REFERENCES content.genre(id) ON DELETE CASCADE,
);

