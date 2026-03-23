"""Contains all dictionary ressources for movies.py"""
def print_messages():
    """Returns a dictionary of console.print and console.input messages"""
    messages = {
        # --------------------
        # INPUTS
        # --------------------
        "input_choice": (
            "[bold bright_cyan]Enter choice (0-10): [/bold bright_cyan]"
        ),
        "input_name": "\nEnter movie name: ",
        "input_rating": "Enter new movie rating (1-10): ",
        "input_year": "Enter release year: ",
        "input_histo_name": (
            "\n[green]Please enter the filename for the histogram: [/green]"
        ),
        # --------------------
        # SUCCESS / INFO
        # --------------------
        "continue": "\n[dim]Press enter to continue[/dim]",
        "exit": "[bold red]Exiting My Movies Database... Goodbye![/bold red]",
        "similar_movie": "[green]Similar movies found: [/green]",
        "index_html": "[green]Webpage successfully generated[/green]",
        "movie_added": "[green]Movie successfully added![/green]",
        "movie_deleted": "[green]Movie successfully deleted![/green]",
        "movie_updated": "[green]Movie successfully updated![/green]",
        # --------------------
        # ERRORS (MOVIES)
        # --------------------
        "no_movies_error": "[red]No movies in the DB available![/red]",
        "error_no_movie": "[red]Could not find your movie in the DB![/red]",
        "error_movie_exists": "[red]Movie already exists![/red]",
        "error_no_sim_movie": "[red]No similar movies found.[/red]",
        # --------------------
        # ERRORS (INPUT VALIDATION)
        # --------------------
        "error_not_valid": "[red]Your entry is not valid![/red]",
        "error_rating": "[red]Rating must be between 1 and 10![/red]",
        "error_valid_year": "[red] No valid year available![/red]",
        "error_valid_rating": "[red] No valid rating available![/red]",
        # --------------------
        # ERRORS (TECHNICAL)
        # --------------------
        "error_add_db": "[red]Could not add movie to DB![/red]",
        "error_del_db": "[red]Could not delete movie from DB![/red]",
        "error_update_db": "[red]Could not update movie in DB![/red]",
        "error_db": "[red]Could not interact with Database correctly![/red]",
        "error_get_response": "[red]Unexpected response from API-request[/red]",
        "error_html_preparation": "[red]Could not create HTML![/red]",
        "error_index_html": "[red]Could not generate web page![/red]",
    }
    return messages