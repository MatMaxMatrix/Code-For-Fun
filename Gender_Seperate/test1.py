import csv
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def process_genders(csv_file):
    genders_to_count = ["Male", "Female"]
    recognized_data = {gender: [] for gender in genders_to_count}
    unrecognized_data = []

    try:
        # Read the CSV file
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                try:
                    gender = row['Genere'].strip().capitalize()
                    if gender in genders_to_count:
                        recognized_data[gender].append(row)
                    else:
                        unrecognized_data.append(row)
                except KeyError as e:
                    logging.error(f"KeyError: Missing key in row: {e}")
                except Exception as e:
                    logging.error(f"Error processing row: {e}")

        # Remove duplicates based on the entire row content
        for gender, rows in recognized_data.items():
            recognized_data[gender] = [dict(t) for t in {tuple(row.items()) for row in rows}]

        unrecognized_data = [dict(t) for t in {tuple(row.items()) for row in unrecognized_data}]

        # Write recognized genders to separate CSV files
        for gender, rows in recognized_data.items():
            try:
                with open(f"{gender.lower()}.csv", "w", newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                logging.info(f"Written {len(rows)} rows for {gender}")
            except Exception as e:
                logging.error(f"Error writing {gender.lower()}.csv: {e}")

        # Write unrecognized genders to CSV
        try:
            with open("sconosciuti.csv", "w", newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(unrecognized_data)
            logging.info(f"Written {len(unrecognized_data)} rows to sconosciuti.csv")
        except Exception as e:
            logging.error(f"Error writing sconosciuti.csv: {e}")

        # Print counts
        for gender, rows in recognized_data.items():
            logging.info(f"{gender} count: {len(rows)}")

        logging.info(f"Unrecognized count: {len(unrecognized_data)}")

    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Specify the CSV file in the current directory
    csv_file = "./test_data.csv"  # Replace with your actual filename
    process_genders(csv_file)