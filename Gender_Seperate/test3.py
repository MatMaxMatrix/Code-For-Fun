import dask.dataframe as dd
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def process_large_csv(input_file, gender_column="Genere"):
    try:
        df = dd.read_csv(input_file).drop_duplicates()
        known_genders = ["Male", "Female"]
        
        df_male = df[df[gender_column] == "Male"]
        df_female = df[df[gender_column] == "Female"]
        df_unknown = df[~df[gender_column].isin(known_genders) | df[gender_column].isna()]

        df_male.to_csv("male.csv", single_file=True, index=False)
        df_female.to_csv("female.csv", single_file=True, index=False)
        df_unknown.to_csv("sconosciuti.csv", single_file=True, index=False)

        logging.info("Files successfully saved.")

    except Exception as e:
        logging.error(f"Error: {e}")

# Use our test data
process_large_csv("test_data.csv")