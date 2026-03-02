CREATE DATABASE practica;

\c practica

CREATE EXTENSION postgis;

CREATE SCHEMA IF NOT EXISTS data;

CREATE TABLE data.buildings (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    area DOUBLE PRECISION,
    height DOUBLE PRECISION,
    category TEXT,
    visitedAt DATE,
    geom GEOMETRY(POLYGON, 25830)
);

CREATE TABLE data.streets (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    length DOUBLE PRECISION,
    lanes INTEGER,
    category TEXT,
    visitedAt DATE,
    geom GEOMETRY(LINESTRING, 25830)
);

CREATE TABLE data.poi (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    category TEXT,
    rating INTEGER,
    priority INTEGER,
    visitedAt DATE,
    geom GEOMETRY(POINT, 25830)
);