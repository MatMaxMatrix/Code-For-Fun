import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def process_genders(csv_file: str, genders_to_count: list[str]) -> None:
    # Load the CSV file
    df = pd.read_csv(csv_file)
    df['Genere'] = df['Genere'].str.strip().str.capitalize()

    # Save recognized genders to separate CSV files
    for gender in genders_to_count:
        df[df['Genere'] == gender].to_csv(f"{gender.lower()}.csv", index=False)

    # Save unrecognized genders
    unrecognized_df = df[~df['Genere'].isin(genders_to_count)]
    unrecognized_df.to_csv("sconosciuti.csv", index=False)

    # Print counts
    for gender in genders_to_count:
        logging.info(f"{gender} count: {len(df[df['Genere'] == gender])}")

    logging.info(f"Unrecognized count: {len(unrecognized_df)}")
    return


if __name__ == "__main__":
    # Example usage
    process_genders(csv_file="test_data.csv", genders_to_count=["Male", "Female"])