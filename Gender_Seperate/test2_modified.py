import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def process_genders(csv_file: str, genders_to_count: list[str]) -> None:
    # Load the CSV file
    try:
        df = pd.read_csv(csv_file)
        
        # Handle NaN values in the Genere column
        df['Genere'] = df['Genere'].fillna('')
        
        # Clean and capitalize gender values
        df['Genere'] = df['Genere'].astype(str).str.strip().str.capitalize()
        
        # Save recognized genders to separate CSV files
        for gender in genders_to_count:
            gender_df = df[df['Genere'] == gender]
            # Remove duplicates based on all columns
            gender_df = gender_df.drop_duplicates()
            output_file = f"{gender.lower()}_pandas.csv"
            gender_df.to_csv(output_file, index=False)
            logging.info(f"Written {len(gender_df)} rows for {gender} to {output_file}")
        
        # Save unrecognized genders
        unrecognized_df = df[~df['Genere'].isin(genders_to_count)]
        # Remove duplicates from unrecognized data
        unrecognized_df = unrecognized_df.drop_duplicates()
        output_file = "sconosciuti_pandas.csv"
        unrecognized_df.to_csv(output_file, index=False)
        logging.info(f"Written {len(unrecognized_df)} rows to {output_file}")
        
        # Print counts (after duplicate removal)
        for gender in genders_to_count:
            gender_count = len(df[df['Genere'] == gender].drop_duplicates())
            logging.info(f"{gender} count (after duplicate removal): {gender_count}")
        
        logging.info(f"Unrecognized count (after duplicate removal): {len(unrecognized_df)}")
    
    except Exception as e:
        logging.error(f"Error processing file: {e}")
    
    return


if __name__ == "__main__":
    # Use our test data
    process_genders(csv_file="employees.csv", genders_to_count=["Male", "Female"]) 