"""
Codio Project: My Movies Database – Extended CLI Application

This module implements a menu-driven command-line application for
managing a personal movie database as a MasterSchool project.

The application supports full CRUD functionality (Create, Read,
Update, Delete) as well as analytical and visualization features.
Each movie is represented as a dictionary containing the following
attributes:

    - title (str): The movie title
    - rating (float): The user-defined rating (1–10)
    - year (int): The release year

Features
--------
- List all stored movies
- Add new movies
- Delete existing movies
- Update movie ratings
- Display statistical insights (average, median, best, worst)
- Select a random movie
- Search movies (including fuzzy matching)
- Sort movies by rating
- Generate and save a histogram of ratings

"""

import movie_storage

import difflib
import random
import statistics

import matplotlib.pyplot as plt
from rich.console import Console
from rich.panel import Panel


console = Console()  # fits nicer in snake_case


def start_screen():
    """
    Displays the application start screen and menu options.

    Returns:
        str: The user's menu selection as a string.
    """
    console.print(
        Panel(
            "[bold_magenta]My Movies Database[/bold_magenta]",
            expand=False,
            border_style="magenta",
        )
    )
    menu = (
        "[cyan]0. Exit\n"
        "1. List movies\n"
        "2. Add movie\n"
        "3. Delete movie\n"
        "4. Update movie\n"
        "5. Stats\n"
        "6. Random movie\n"
        "7. Search movie\n"
        "8. Movies sorted by rating\n"
        "9. Draw histogram of rankings[/cyan]"
    )
    console.print(
        Panel(
            menu,
            title="[bold cyan]Menu[bold cyan]",
            expand=False,
            border_style="cyan"
        )
    )
    choice = console.input(
        "[bold bright_cyan]Enter choice (0-9): [/bold bright_cyan]"
    )
    return choice


def movie_db_function_list():
    """
    Displays all movies stored in the database.

    Returns:
        None
    """
    movies = movie_storage.get_movies()
    print(f"\n{len(movies)} movies in total")
    for movie in movies:
        print(f"{movie['title']}: {movie['rating']} ({movie['year']})")
    console.input("\n[dim]Press enter to continue[/dim]")


def check_rating(rating):
    """Checks if rating is valid."""
    if 1 <= rating <= 10:
        return True
    return False


def check_double_titles(title):
    """Checks if the movie title is a double title.

    Returns:
        bool: True if double, else False.
        """
    movies = movie_storage.get_movies()
    for movie in movies:
        if movie.get('title').lower() == title.lower():
            return True
    return False


def movie_db_function_add():
    """CLI wrapper to add a movie with user input."""
    while True:
        title = console.input("\nEnter new movie name: ").strip()
        if not title:
            console.print("[red]Please enter a valid movie name![/red]")
        elif check_double_titles(title):
            console.print("[red]Movie already exists![/red]")
        else:
            break

    while True:
        try:
            rating = float(console.input("Enter new movie rating (1-10): "))
            if check_rating(rating):
                break
            console.print("[red]Rating must be between 1 and 10![/red]")
        except ValueError:
            console.print(
                "[red]Invalid rating input! Please enter a number.[/red]"
            )
    while True:
        try:
            year = int(console.input("Enter release year: "))
            break
        except ValueError:
            console.print(
                "[red]Invalid year input! Please enter a number.[/red]"
            )
    movie_storage.add_movie(title, rating, year)
    console.print(f"[green]Movie {title} successfully added![/green]")
    console.input("\n[dim]Press enter to continue[/dim]")


def movie_db_function_del():
    """CLI wrapper to delete a movie."""
    while True:
        title = console.input("\nEnter movie name to delete: ")
        if title:
            break
        else:
            console.print("[red]Please enter a valid movie name![/red]")
    success = movie_storage.delete_movie(title)
    if success:
        print(f"Movie {title} successfully deleted")
    else:
        print(f"Movie {title} doesn't exist!")
    console.input("\n[dim]Press enter to continue[/dim]")


def movie_db_function_update():
    """CLI wrapper to update a movie rating."""
    while True:
        title = console.input("\nEnter movie name: ").strip()
        if title:
            break
        console.print("[red]Please enter a valid movie name![/red]")
    while True:
        try:
            new_rating = float(console.input("Enter new movie rating (1-10): "))
            if 1 <= new_rating <= 10:
                break
            console.print("[red]Rating must be between 1 and 10![/red]")
        except ValueError:
            console.print("[red]Invalid rating input! Please enter a number.[/red]")
    success = movie_storage.update_movie(title, new_rating)
    if success:
        console.print(f"[green]Movie {title} successfully updated![/green]")
    else:
        console.print(f"[red]Movie {title} doesn't exist![/red]")
    console.input("\n[dim]Press enter to continue[/dim]")


def sort_movies_logic(movies):
    """Return movies sorted by rating descending and title ascending."""
    sorted_to_ratings = sorted(
        movies,
        key=lambda m: (-m["rating"], m["title"])
    )
    return sorted_to_ratings


def stats_logic(movies):
    """Compute average, median, best and worst movies. Gets sorted movie list
    from sort_movies_logic()"""
    #In case of empty movie database:
    if not movies:
        return None, None, [], []
    ratings = [movie["rating"] for movie in movies]
    avg = statistics.mean(ratings)
    med = statistics.median(ratings)

    sorted_movies = sort_movies_logic(movies)
    highest_rating = sorted_movies[0]["rating"]
    lowest_rating = sorted_movies[-1]["rating"]
    best_movies = []
    worst_movies = []
    for movie in sorted_movies:
        if movie["rating"] == highest_rating:
            best_movies.append(movie)
        if movie["rating"] == lowest_rating:
            worst_movies.append(movie)

    return avg, med, best_movies, worst_movies


def movie_db_function_stats():
    """CLI wrapper to display stats."""
    movies = movie_storage.get_movies()
    avg, med, best, worst = stats_logic(movies)
    # Taking care of empty database return values from stats_logic():
    if avg is None:
        console.print("[red]No movies stored in database![/red]")
        console.input("\n[dim]Press enter to continue[/dim]")
        return
    console.print(f"[green]Average rating: {avg:.1f}[/green]")
    console.print(f"[green]Median rating: {med:.1f}[/green]")
    for movie in best:
        console.print(
            f"[green]Best movie: {movie['title']}, {movie['rating']}[/green]"
        )
    for movie in worst:
        console.print(
            f"[green]Worst movie: {movie['title']}, {movie['rating']}[/green]"
        )
    console.input("\n[dim]Press enter to continue[/dim]")


def get_random_logic():
    """Select a random movie dictionary from the list of movies in
    movie_data.json via get_movies() in movie_storage.py and returns it."""
    movies = movie_storage.get_movies()
    if not movies:
        return None
    random_movie = random.choice(movies)
    return random_movie


def movie_db_function_random():
    """
    Displays a random movie from the database selected by random_logic().

    Returns:
        None
    """
    random_movie = get_random_logic()
    if not random_movie:
        console.print("[red]No movies available in database![/red]")
    else:
        console.print(
            f"\n[green]Your movie for tonight: {random_movie['title']}, "
            f"it's rated {random_movie['rating']} "
            f"({random_movie['year']})[/green]"
        )
    console.input("\n[dim]Press enter to continue[/dim]")


def search_movie_logic(what_to_search, movies):
    """
    Search for movies by partial title match and fuzzy similarity.

    Args:
        what_to_search (str): The term to search for.
        movies (list[dict]): The movie database.

    Returns:
        tuple:
            - list[dict]: Exact/partial matches
            - list[str]: Similar movie titles (fuzzy matches)
    """
    what_to_search = what_to_search.lower()
    # Normal partial match
    exact_matches = [
        movie for movie in movies
        if what_to_search in movie["title"].lower()
    ]
    if exact_matches:
        return exact_matches, []
    # Fuzzy matching
    movie_titles = [movie["title"] for movie in movies]
    close_matches = difflib.get_close_matches(
        what_to_search,
        movie_titles,
        n=3,
        cutoff=0.4
    )
    return [], close_matches


def movie_db_function_search():
    """
    CLI wrapper for searching movies.
    """
    movies = movie_storage.get_movies()
    while True:
        what_to_search = console.input("\nEnter part of movie name: ")
        if what_to_search:
            break
        else:
            console.print("[red]Please enter a valid search term![/red]")
            continue
    exact_matches, close_matches = search_movie_logic(what_to_search, movies)

    if exact_matches:
        for movie in exact_matches:
            console.print(
                f"[green]{movie['title']}, "
                f"{movie['rating']} "
                f"({movie['year']})[/green]"
            )
    else:
        console.print("\n[magenta]Movie not found![/magenta]")
        if close_matches:
            console.print("[green]Similar movies found: [/green]")
            for similar_name in close_matches:
                for movie in movies:
                    if movie["title"] == similar_name:
                        console.print(
                            f"[green]  - {movie['title']}, "
                            f"{movie['rating']} "
                            f"({movie['year']})[/green]"
                        )
        else:
            console.print("[red]No similar movies found.[/red]")
    console.input("\n[dim]Press enter to continue[/dim]")


def movie_db_function_sort():
    """
    Displays all movies sorted by rating in descending order and
    alphabetically by title as a secondary criterion. Gets sorted
    movie list from sort_movies_logic().

    Returns:
        None
    """
    movies = movie_storage.get_movies()
    sorted_to_ratings = sort_movies_logic(movies)
    for movie in sorted_to_ratings:
        console.print(
            f"[green]{movie['title']}: "
            f"{movie['rating']} "
            f"({movie['year']})[/green]"
        )
    console.input("\n[dim]Press enter to continue[/dim]")


def movie_db_function_histo():
    """
    Generates and saves a histogram visualization of movie ratings.

    Returns:
        None
    """
    movies = movie_storage.get_movies()
    if not movies:
        console.print("[red]No movies available to create histogram.[/red]")
        console.input("\n[dim]Press enter to continue[/dim]")
        return
    # Brauche hier eine Liste von allen Rankings
    all_rankings_list = [movie["rating"] for movie in movies]
    # Erstellung Histogramm, skaliert automatisch den x-Achsenbereich,
    # erstellt 10 bins mit 1 Schrittweite
    set_binwidth = list(range(1, 12))
    plt.clf() # Clear current figure to avoid graphical overlay of figures
    plt.hist(all_rankings_list,
             bins=set_binwidth,
             edgecolor="black",
             color="red")
    plt.title("Movie Ranking Histogram")
    plt.xlabel("Ranking distribution")
    plt.ylabel("Frequency")
    # Dateinamen abfragen und das Histogram als .png in den
    # Projektspeicherplatz speichern
    while True:
        file_name = console.input(
            "\n[green]Please enter the filename for the histogram: [/green]"
        )
        if file_name:
            break
        else:
            console.print("[red]Please enter a valid filename![/red]")
    plt.savefig(f"{file_name}.png", dpi=150)
    console.input("\n[dim]Press enter to continue[/dim]")


def movie_db_function_quit():
    """
    Terminates the application gracefully.

    Returns:
        None
    """
    console.print("[bold red]Exiting My Movies Database... Goodbye![/bold red]")
    exit()


def get_functions_dictionary():
    """Returns functions_dictionary."""
    # Dictionary zum Speichern der Filmtitel und Ratings
    functions_dictionary = {
        "1": movie_db_function_list,
        "2": movie_db_function_add,
        "3": movie_db_function_del,
        "4": movie_db_function_update,
        "5": movie_db_function_stats,
        "6": movie_db_function_random,
        "7": movie_db_function_search,
        "8": movie_db_function_sort,
        "9": movie_db_function_histo,
        "0": movie_db_function_quit,
    }
    return functions_dictionary


def main():
    functions_dictionary = get_functions_dictionary()
    while True:
        choice = start_screen()
        if choice not in functions_dictionary:
            console.print("[red]Invalid choice![/red]")
            continue
        functions_dictionary[choice]()


if __name__ == "__main__":
    main()
