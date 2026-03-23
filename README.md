# My Movies Database (CLI)

A small, menu-driven command-line application to manage a personal movie database (Codio/MasterSchool project).  

Movies are stored in a SQLite database. The app supports CRUD operations and a few analytics and visualization features.

## Features

- List all stored movies
- Add a new movie (fetches data from the OMDb API)
- Delete an existing movie
- Update a movie rating
- Show statistics (average, median, best, worst)
- Pick a random movie
- Search movies (partial match + fuzzy matching)
- Sort movies by rating
- Generate and save a ratings histogram (PNG)
- Generate an HTML web page from the database entries

## Tech Stack

- Python 3
- SQLite (movie storage)
- OMDb API (movie metadata)

## Installation

(Optional but recommended: use a virtual environment.)

pip install -r requirements.txt

## Configuration (Environment Variables)

This project uses a .env file. Start from the provided .env.example:

macOS / Linux:

cp .env.example .env

Windows (PowerShell):

copy .env.example .env

Then edit .env and set the values:

URL=https://www.omdbapi.com/  

API_KEY=your_omdb_api_key  

APP_TITLE=My Movies Database

Note: Do not commit .env to version control (it contains credentials).

## Run

python [movies.py](http://movies.py)

## Usage

After starting the app, choose an option from the menu:

- 1 List movies
- 2 Add movie
- 3 Delete movie
- 4 Update movie
- 5 Stats
- 6 Random movie
- 7 Search movie
- 8 Movies sorted by rating
- 9 Draw histogram of rankings
- 10 Generate web page
- 0 Exit

## Data Model (SQLite)

Each movie entry contains:

- title (string)
- year (int)
- rating (float, 1–10)
- poster (string URL)

## Project Structure (high level)

- [movies.py](http://movies.py) — Main entry point (starts the CLI menu and handles user interaction)
- requirements.txt — Python dependencies
- data/ — Database + storage layer
    - **init**.py — Marks data as a Python package
    - [dictionaries.py](http://dictionaries.py) — UI strings and messages (prompts, errors, etc.)
    - movie_storage_[sql.py](http://sql.py) — SQLite CRUD operations (create, read, update, delete)
    - movies.db — SQLite database file (stored movie entries)
- web/ — HTML generation utilities
    - **init**.py — Marks web as a Python package
    - create_[webpage.py](http://webpage.py) — Generates index.html from a template and DB entries
- _static/
    - index_template.html — HTML template used to build the output page
- webpage/ — Generated website output
    - index.html — Generated HTML page
    - style.css — Stylesheet for the generated page
