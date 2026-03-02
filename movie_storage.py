import json


def get_movies():
    """
    Returns a list of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.
    Each movie is represented as a dictionary with the following keys:
        - title (str): The movie title
        - rating (float | int): The movie rating
        - year (int): The release year

    Returns:
        list[dict]: A list of movie dictionaries.

    Example return value:
        [
            {
                "title": "Titanic",
                "rating": 9,
                "year": 1999
            },
            {
                "title": "Inception",
                "rating": 8.8,
                "year": 2010
            }
        ]
        """
    try:
        with open("movie_data.json", "r", encoding="utf-8") as fileobj:
            movies = json.load(fileobj)
            return movies
    except FileNotFoundError:
        return []


def save_movies(movies):
    """
    Save the provided list of movie dictionaries to the JSON file.

    Args:
        movies (list[dict]): The complete movie database to persist.
    """
    with open("movie_data.json", "w", encoding="utf-8") as fileobj:
        fileobj.write(json.dumps(movies, indent=4))


def add_movie(title, rating, year):
    """
    Add a new movie to the JSON database.

    The function loads the current movie list, appends the new movie
    as a dictionary, and saves the updated list.

    Args:
        title (str): The movie title.
        year (int): The release year.
        rating (float | int): The movie rating.
    """
    movies = get_movies()
    movies.append({"title": title, "rating": rating, "year": year})
    save_movies(movies)


def delete_movie(title):
    """
    Remove a movie from the JSON database by its title.

    Args:
        title (str): The movie title to delete.

    Returns:
        - bool: True if deleted, False if not found
    """
    movies = get_movies()
    for movie in movies:
        if movie["title"] == title:
            movies.remove(movie)
            save_movies(movies)
            return True
    return False


def update_movie(title, rating):
    """
    Update the rating of a movie in the JSON database.

    Args:
        title (str): The movie title.
        rating (float | int): The new rating.

    Returns:
        - bool: True if updated
               False if rating invalid
               None if movie not found
    """
    movies = get_movies()
    for movie in movies:
        if movie["title"] == title:
            if 1 <= rating <= 10:
                movie["rating"] = rating
                save_movies(movies)
                return True
            return False
    return None  # Movie not found

