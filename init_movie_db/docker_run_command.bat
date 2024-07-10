docker run -d ^
    --name init_db_movie ^
    -p 5432:5432 ^
    -e POSTGRES_DB=movie_db ^
    -e POSTGRES_USER=postgres ^
    -e POSTGRES_PASSWORD=123456789 ^
    -v movie_db_volume:/var/lib/postgresql/data ^
    init_db_movie

