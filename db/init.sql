-- Create the database
CREATE DATABASE evetoolsdb;

-- Connect to the database
\c evetoolsdb;

-- Create the Characters table
CREATE TABLE characters (
    character_id SERIAL PRIMARY KEY,
    access_token VARCHAR(255),
    refresh_token VARCHAR(255),
    creation_time DOUBLE PRECISION,
    access_token_expiration_time DOUBLE PRECISION,
    character_name VARCHAR(255),
    character_portrait VARCHAR(255)
);

-- Create the UserSessions table
CREATE TABLE user_sessions (
    session_token VARCHAR(255) PRIMARY KEY,
    character_id INTEGER REFERENCES characters(character_id)
);

