def test_movies_new_section(movies_new_section):
    assert movies_new_section.totalSize == 4, "Incorrect number of movies found."
    assert len(movies_new_section.all(container_start=0, container_size=1, maxresults=1)) == 1,\
        "Incorrect number of movies found."


def test_movies_imdb_section(movies_imdb_section):
    assert movies_imdb_section.totalSize == 4, "Incorrect number of movies found."
    assert len(movies_imdb_section.all(container_start=0, container_size=1, maxresults=1)) == 1, \
        "Incorrect number of movies found."


def test_movies_themoviedb_section(movies_themoviedb_section):
    assert movies_themoviedb_section.totalSize == 4, "Incorrect number of movies found."
    assert len(movies_themoviedb_section.all(container_start=0, container_size=1, maxresults=1)) == 1, \
        "Incorrect number of movies found."


def test_tv_shows_section(tv_shows_section):
    show = tv_shows_section.get("Game of Thrones")
    assert show, "Show not found."


def test_tv_shows_tmdb_section(tv_shows_tmdb_section):
    show = tv_shows_tmdb_section.get("Game of Thrones")
    assert show, "Show not found."


def test_tv_shows_tvdb_section(tv_shows_tvdb_section):
    show = tv_shows_tvdb_section.get("Game of Thrones")
    assert show, "Show not found."


def test_music_section(music_section):
    artist = music_section.get("Broke For Free")
    assert artist, "Artist not found."


def test_photo_section(photo_section):
    try:
        photo = photo_section.get("Cats")
    except Exception:
        photo = photo_section.get("photo_album1")
    assert photo, "Photo not found."
