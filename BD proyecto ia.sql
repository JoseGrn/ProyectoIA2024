-- Crear la base de datos
CREATE DATABASE MovieReviewDB;
GO

-- Usar la base de datos recién creada
USE MovieReviewDB;
GO

-- Crear la tabla tb_user
CREATE TABLE tb_user (
    userid INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    [user] VARCHAR(255) NOT NULL,
    [password] VARCHAR(255) NOT NULL,
    [level] INT NOT NULL,
    createdate DATE NOT NULL
);
GO

-- Crear la tabla tb_movie
CREATE TABLE tb_movie (
    movieid INT IDENTITY(1,1) PRIMARY KEY,
    rotten_tomatoes_link VARCHAR(MAX),
    movie_title VARCHAR(MAX),
    movie_info VARCHAR(MAX),
    critics_consensus VARCHAR(MAX),
    content_rating VARCHAR(MAX),
    genres VARCHAR(MAX),
    directors VARCHAR(MAX),
    authors VARCHAR(MAX),
    actors VARCHAR(MAX),
    original_release_date DATE,
    streaming_release_date DATE,
    runtime INT,
    production_company VARCHAR(MAX),
    tomatometer_status VARCHAR(MAX),
    tomatometer_rating INT,
    tomatometer_count INT,
    audience_status VARCHAR(MAX),
    audience_rating INT,
    audience_count INT,
    tomatometer_top_critics_count INT,
    tomatometer_fresh_critics_count INT,
    tomatometer_rotten_critics_count INT
);
GO

-- Crear la tabla tb_review
CREATE TABLE tb_review (
    reviewid INT IDENTITY(1,1) PRIMARY KEY,
    userid INT FOREIGN KEY REFERENCES tb_user(userid),
    movieid INT FOREIGN KEY REFERENCES tb_movie(movieid),
    score INT NOT NULL,
    comment VARCHAR(MAX),
    reviewdate DATE NOT NULL,
	tomatometer NVARCHAR(MAX)
);
GO