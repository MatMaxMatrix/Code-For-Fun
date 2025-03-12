import csv
from typing import List, Dict
import sys


class MovieDatabase:
    EXPECTED_HEADERS = ['Genre', 'Movie', 'Release Date', 'Year', 'Oscar Winner', 'Lead Actor']

    def __init__(self, filename: str):
        self.movies = self.load_data(filename)

    def validate_headers(self, headers: List[str]) -> bool:
        """Validate if the file headers match the expected format."""
        return headers == self.EXPECTED_HEADERS

    def load_data(self, filename: str) -> List[Dict]:
        """Load and validate the movie data from the file."""
        try:
            with open(filename, 'r') as file:
                # Read the first line and split by '|' to get headers
                headers = [header.strip() for header in file.readline().split('|')]

                if not self.validate_headers(headers):
                    raise ValueError("Invalid file format. Expected headers: " +
                                    ", ".join(self.EXPECTED_HEADERS))

                # Read the rest of the file as CSV with '|' delimiter
                reader = csv.DictReader(file, fieldnames=headers, delimiter='|')
                return [row for row in reader]

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            sys.exit(1)

    def display_actors(self):
        """Display all unique actors in the database."""
        actors = sorted(set(movie['Lead Actor'].strip() for movie in self.movies))
        print("\nLead Actors in the Database:")
        print("-" * 30)
        for actor in actors:
            print(actor)

    def display_movies(self):
        """Display all movies with their details."""
        print("\nMovies in the Database:")
        for movie in sorted(self.movies, key=lambda x: x['Movie']):
            print(f"Title: {movie['Movie'].strip()}")

    def display_genres(self):
        """Display all unique genres in the database."""
        genres = sorted(set(movie['Genre'].strip() for movie in self.movies))
        print("\nMovie Genres:")
        for genre in genres:
            print(genre)


def display_menu():
    """Display the main menu options."""
    print("\nMovie Database Menu:")
    print("1. Display Actors")
    print("2. Display Movies")
    print("3. Display Genres")
    print("4. Exit")
    return input("Enter your choice (1-4): ")


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        db = MovieDatabase(filename)

        while True:
            choice = display_menu()

            if choice == '1':
                db.display_actors()
            elif choice == '2':
                db.display_movies()
            elif choice == '3':
                db.display_genres()
            elif choice == '4':
                print("Closing the program!")
                break
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()