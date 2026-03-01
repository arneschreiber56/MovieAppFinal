"""
Codio Project: My Movies Database – Extended Version

Overview
This version expands the previous CLI-based movie application, which
implemented two main command categories:
	•	CRUD operations: Create, Read, Update, Delete
	•	Analysis features: highest-rated movies, lowest-rated movies, etc.

The project now integrates more advanced concepts and improvements.

New Features
	1.	Enhanced Data Structure
The simple dictionary structure (title → rating) has been replaced
with a more complex data model that stores multiple attributes per movie,
such as title, rating, and release year.
	2.	Persistent Storage
Previously, all data was stored in memory and lost when the application
terminated. This version introduces persistent storage, ensuring that
added or modified movies remain available after restarting the program.
	3.	Improved Robustness
The application is hardened against unexpected user input.
Invalid entries no longer cause crashes. Instead, the user is
prompted again, improving stability and overall user experience.

The program remains menu-driven and continues to provide CRUD
and analytical functionality within a structured CLI environment.
"""

import statistics
import random
import difflib
import matplotlib.pyplot as plt
# for a little bit more design and style:
from rich.console import Console
console = Console() #fits nicer in in snake.case
from rich.panel import Panel


def start_screen():
    """
    Gibt den Startscreen mit dem Auswahlmenü aus.
    :return: Gibt die Auswahl des Users wieder
    """
    console.print(Panel(
            "[bold_magenta]My Movies Database[/bold_magenta]",
        expand=False,
        border_style="magenta"
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
    console.print(Panel(
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


def movie_db_function_list(movies):
    """
    Gibt die Filme in der Film-DB-Liste aus
    :param movies: Film-DB-Liste
    :return: None
    """
    print(f"\n{len(movies)} movies in total")
    for movie in movies:
        print(f"{movie['title']}: {movie['rating']} ({movie['year']})")
    console.input("\n[dim]Press enter to continue[/dim]")
    return


def movie_db_function_add(movies):
    """
    Ergänzt einen neuen Film in der Film-DB-Liste. User gibt Filmtitel, Rating
    und Erscheinungsjahr an.
    :param movies: Film-DB-Liste
    :return: aktualisierte Film-DB-Liste
    """
    new_movie_name = input("\nEnter new movie name: ")
    new_movie_rating_float = float(input("Enter new movie rating(0-10): "))
    new_movie_year = int(input("Enter release year: "))
    if 1 <= new_movie_rating_float <= 10:
        movies.append({
            "title": new_movie_name,
            "rating": new_movie_rating_float,
            "year": new_movie_year
        })
        console.input("\n[dim]Press enter to continue[/dim]")
        return movies
    else:
        print(f"Rating {new_movie_rating_float} is invalid")
        console.input("\n[dim]Press enter to continue[/dim]")
        return movies


def movie_db_function_del(movies):
    """
    Löscht einen Film aus dem Film-DB-Dictionary. User muss korrekten Filmtitel
    angeben.
    :param movies: Film-DB-Dictionary
    :return: Aktualisiertes Film-DB-Dictionary
    """
    movie_to_del = input("\nEnter movie name to delete: ")
    for movie in movies:
        if movie["title"] == movie_to_del:
            movies.remove(movie)
            print(f"Movie {movie_to_del} successfully deleted")
            return movies
    else:
        print(f"Movie {movie_to_del} doesn't exist!")
        return movies


def movie_db_function_update(movies):
    """
    Aktualisiert einen Filmeintrag in der Film-DB-Liste. User muss
    Filmtitel korrekt angeben und dann auf Nachfrage das aktualisierte Rating
    eingeben.
    :param movies: Film-DB-Liste
    :return: Aktualisierte Film-DB-Liste
    """
    movie_to_update = input("\nEnter movie name: ")
    for movie in movies:
        if movie["title"] == movie_to_update:
            new_rating = float(input("Enter new movie rating (1-10): "))
            if 1 <= new_rating <= 10:
                movie["rating"] = new_rating
                print(f"Movie {movie_to_update} successfully updated")
                return movies
            else:
                print(f"Rating {new_rating} is invalid")
                return movies
    else:
        print(f"Movie {movie_to_update} doesn't exist!")
        return movies


def movie_db_function_stats(movies):
    """
    Sortiert die Datenbank primär nach Rating und sekundär alphabetisch.
    Gibt durchschnittliche und mediane Bewertung wieder, sowie die Filme mit
    der besten und der schlechtesten Bewertung. Benutzt für Average und Median
    die statistics library.
    :param movies: Film-DB-Dictionary
    :return: None
    """
    average_rating = statistics.mean(movie["rating"] for movie in movies)
    median_rating = statistics.median(movie["rating"] for movie in movies)
    print(f"Average rating: {average_rating:.2f}")
    print(f"Median rating: {median_rating}")
    sorted_to_ratings = sorted(
        movies,
        key=lambda m: (m["rating"], m["title"]),
        reverse=True
    )
    best_movie = sorted_to_ratings[0]
    worst_movie = sorted_to_ratings[-1]

    print(f"Best movie: {best_movie['title']}, {best_movie['rating']}")
    print(f"Worst movie: {worst_movie['title']}, {worst_movie['rating']}")
    console.input("\n[dim]Press enter to continue[/dim]")
    return


def movie_db_function_random(movies):
    """
    Die Funktion wählt einen zufälligen Film mithilfe der random library aus und
    gibt diesen samt Rating und Erscheinungsjahr aus.
    :param movies: Film-DB-Liste
    :return: None
    """
    random_movie = random.choice(movies)
    print(
        f"\nYour movie for tonight: {random_movie['title']}, "
        f"it's rated {random_movie['rating']} ({random_movie['year']})"
    )
    console.input("\n[dim]Press enter to continue[/dim]")
    return


def movie_db_function_search(movies):
    """
    Sucht mithilfe der difflib library und Fuzzy Matching einen Film in der
    Datenbank, auch wenn der Titel nicht ganz korrekt eingegeben wird.
    Gibt exakten Treffer wieder. Wenn kein exakter Treffer gefunden wurde,
    wird mittels Fuzzy Matching ähnliche Treffer ausgegeben, sofern gefunden.
    :param movies: Film-DB-Liste
    :return: None
    """
    # zum Fuzzy Matching
    what_to_search = input("\nEnter part of movie name: ").lower()
    # normale Suche
    found_any = False
    for movie in movies:
        if what_to_search in movie["title"].lower():
            print(f"{movie['title']}, {movie['rating']} ({movie['year']})")
            found_any = True
    if found_any:
        console.input("\n[dim]Press enter to continue[/dim]")
        return
    # nun zum Fuzzy Matching, falls die Normale suche nicht ergeben hat
    print("\nMovie not found!")
    # Mit der get_close_matches-Funktion von difflib ähnliche Einträge
    # in movielist finden und als Liste ausgeben
    # Fuzzy Matching vorbereiten mit einer Liste von Filmtiteln:
    movie_titles = [movie["title"] for movie in movies]
    close_matches = difflib.get_close_matches(
        what_to_search,
        movie_titles,
        # Anzahl der maximalen Ausgabe ähnlicher Filmnamen
        n=3,
        # Sensitivtät der Suche 0.1 → können total unterschiedlich sein,
        # 1 → Müssen exakt gleich sein
        cutoff=0.4
    )
    if close_matches:
        print("Similar movies found:")
        print(close_matches)
        for similar_name in close_matches:
            for movie in movies:
                if movie["title"] == similar_name:
                    print(f"  - {movie['title']}, "
                          f"{movie['rating']} "
                          f"({movie['year']})"
                          )
    else:
        print("No similar movies found.")
    console.input("\n[dim]Press enter to continue[/dim]")
    return


def movie_db_function_sort(movies):
    """
    Sortiert Filme absteigend nach primär nach Rating und sekundär alphabetisch
    :param movies: Film-DB-Liste
    :return: None
    """
    sorted_to_ratings = sorted(
        movies,
        key=lambda m: (-m["rating"], m["title"])
    )
    for movie in sorted_to_ratings:
        print(f"{movie['title']}: {movie['rating']} ({movie['year']})")
    console.input("\n[dim]Press enter to continue[/dim]")
    return


def movie_db_function_histo(movies):
    """
    Erstellt mittels matplotlib.pyplot ein Histogramm der Filmratings.
    User wird nach Filename für Histogramm gefragt und das Histogramm wird unter
    dem Filename als .png-File im Working Directory gespeichert.
    :param movies: Film-DB-Liste
    :return: None
    """
    # Brauche hier eine Liste von allen Rankings
    all_rankings_list = [movie["rating"] for movie in movies]
    # Erstellung Histogramm, skaliert automatisch den x-Achsenbereich,
    # erstellt 10 bins mit 1 Schrittweite
    set_binwidth = list(range(1, 10))
    plt.hist(all_rankings_list,
             bins=set_binwidth,
             edgecolor="black",
             color="red")
    plt.title("Movie Ranking Histogram")
    plt.xlabel("Ranking distribution")
    plt.ylabel("Frequency")
    # Dateinamen abfragen und das Histogram als .png in den
    # Projektspeicherplatz speichern
    file_name = input("\nPlease enter the filename for the histogram: ")
    plt.savefig(f"{file_name}.png", dpi=150)
    console.input("\n[dim]Press enter to continue[/dim]")
    return


def movie_db_function_quit(_):
    """
    Beendet das Programm.
    :param _: Film-DB-Dictionary, wird nicht benutzt
    :return: None
    """
    console.print("[bold red]Exiting My Movies Database... Goodbye![/bold red]")
    exit()


def main():
    # Dictionary zum Speichern der Filmtitel und Ratings
    movies = [
        {"title": "The Shawshank Redemption", "rating": 9.5, "year": 1994},
        {"title": "Pulp Fiction", "rating": 8.8, "year": 1994},
        {"title": "The Room", "rating": 3.6, "year": 2003},
        {"title": "The Godfather", "rating": 9.2, "year": 1972},
        {"title": "The Godfather: Part II", "rating": 9.0, "year": 1974},
        {"title": "The Dark Knight", "rating": 9.0, "year": 2008},
        {"title": "12 Angry Men", "rating": 8.9, "year": 1957},
        {"title": "Everything Everywhere All At Once", "rating": 8.9,
         "year": 2022},
        {"title": "Forrest Gump", "rating": 8.8, "year": 1994},
        {"title": "Star Wars: Episode V", "rating": 8.7, "year": 1980},
    ]
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
    while True:
        choice = start_screen()
        try:
            function_choice = functions_dictionary[choice]
            function_choice(movies)
        except KeyError:
            console.print("[red]No a valid entry! Please choose again.[/red]")


if __name__ == "__main__":
    main()
