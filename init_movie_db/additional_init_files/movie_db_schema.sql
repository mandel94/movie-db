CREATE TABLE movie
(
  movie_id INT NOT NULL,
  title VARCHAR(100) NOT NULL,
  release_date DATE NOT NULL,
  movie_url VARCHAR(200) NOT NULL,
  lang VARCHAR(2) NOT NULL,
  budget INT,
  grossed INT,
  runtime INT,
  movie_status INT,
  tagline VARCHAR(100),
  movie_source VARCHAR(200) NOT NULL,
  poster_img_url VARCHAR(200),
  global_movie_id INT,
  product_type VARCHAR(50),
  PRIMARY KEY (movie_id)
);