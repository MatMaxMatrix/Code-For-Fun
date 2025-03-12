import csv

import sys



EXPECTED_COLUMNS = ["Genre", "Movie", "Release Date", "Year", "Oscar Winner", "Lead Actor"]



def read_file(file_path):

    try:

        with open(file_path, mode='r', newline='', encoding='utf-8') as file:

            reader = csv.DictReader(file, delimiter='|')

            if reader.fieldnames != EXPECTED_COLUMNS:

                raise ValueError("File does not contain the expected columns.")

            return list(reader)

    except FileNotFoundError:

        print(f"Error: The file '{file_path}' was not found.")

        sys.exit(1)

    except ValueError as e:

        print(f"Error: {e}")

        sys.exit(1)



def display_actors(data):

    actors = {row["Lead Actor"] for row in data}

    print("\nActors:")

    for actor in sorted(actors):

        print(actor)



def display_movies(data):

    movies = {row["Movie"] for row in data}

    print("\nMovies:")

    for movie in sorted(movies):

        print(movie)



def display_genres(data):

    genres = {row["Genre"] for row in data}

    print("\nGenres:")

    for genre in sorted(genres):

        print(genre)



def main():

    if len(sys.argv) != 2:

        print("Usage: python script.py <file_path>")

        sys.exit(1)



    file_path = sys.argv[1]

    data = read_file(file_path)



    while True:

        print("\nMenu:")

        print("1. Display Actors")

        print("2. Display Movies")

        print("3. Display Genres")

        print("4. Exit")



        choice = input("Enter your choice: ")



        if choice == '1':

            display_actors(data)

        elif choice == '2':

            display_movies(data)

        elif choice == '3':

            display_genres(data)

        elif choice == '4':

            print("Exiting...")

            break

        else:

            print("Invalid choice. Please try again.")



if __name__ == "__main__":

    main()