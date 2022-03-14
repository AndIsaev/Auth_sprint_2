-- Create schema for content
CREATE SCHEMA IF NOT EXISTS auth;

-- Create tables with content
CREATE TABLE IF NOT EXISTS auth.users (
    id uuid PRIMARY KEY,
    username text UNIQUE NOT NULL,
    password text NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS auth.history (
    id uuid PRIMARY KEY,
    username text UNIQUE NOT NULL,
    user_activity text,
    created_at timestamp with time zone
);


CREATE TABLE IF NOT EXISTS auth.userhistory (
    id uuid PRIMARY KEY,
    username text UNIQUE NOT NULL,
    user_activity text,
    created_at timestamp with time zone
);

