import dask.dataframe as dd
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def process_large_csv(input_file, gender_column="Genere"):
    try:
        # Read the CSV file and remove duplicates
        df = dd.read_csv(input_file).drop_duplicates()
        
        known_genders = ["Male", "Female"]
        
        # Filter by gender
        df_male = df[df[gender_column].str.strip().str.capitalize() == "Male"]
        df_female = df[df[gender_column].str.strip().str.capitalize() == "Female"]
        df_unknown = df[~df[gender_column].str.strip().str.capitalize().isin(known_genders) | df[gender_column].isna()]

        # Save to CSV files with distinct names
        df_male.to_csv("male.csv", single_file=True, index=False)
        df_female.to_csv("female.csv", single_file=True, index=False)
        df_unknown.to_csv("unknown.csv", single_file=True, index=False)

        # Compute and log counts
        male_count = len(df_male.compute())
        female_count = len(df_female.compute())
        unknown_count = len(df_unknown.compute())
        
        logging.info(f"Male count: {male_count}")
        logging.info(f"Female count: {female_count}")
        logging.info(f"Unknown count: {unknown_count}")
        logging.info("Files successfully saved.")

    except Exception as e:
        logging.error(f"Error: {e}")

# Use our test data
if __name__ == "__main__":
    process_large_csv("test_data.csv") 