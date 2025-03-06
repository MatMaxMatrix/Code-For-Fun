# Gender Separation Scripts

This directory contains various implementations of scripts that process CSV files to separate data based on gender. Each script uses a different approach and library to accomplish the same task.

## Test Data

The `test_data.csv` file contains sample data with various edge cases to test the scripts:
- Different capitalizations of "Male" and "Female"
- Leading and trailing spaces
- Empty gender values
- Non-binary gender identifiers
- Abbreviations (M, F)
- Gender terms in other languages
- Quoted values
- Duplicate entries

## Script Implementations

### 1. test1.py - CSV Module Approach

- Uses the standard Python `csv` module
- Processes data row by row
- Removes duplicates using set operations
- Has extensive error handling for different types of errors
- Outputs: `male.csv`, `female.csv`, `sconosciuti.csv`

Usage:
```
python test1.py
```

### 2. test2.py - Pandas Approach

- Uses `pandas` for data manipulation
- More concise code than the CSV module approach
- Takes gender categories as a parameter
- Outputs: `male.csv`, `female.csv`, `sconosciuti.csv`

Usage:
```
python test2.py
```

### 3. test2_modified.py - Improved Pandas Approach

- Uses `pandas` with duplicate removal
- Handles empty values and case sensitivity
- More robust error handling
- Outputs: `male_pandas.csv`, `female_pandas.csv`, `sconosciuti_pandas.csv`

Usage:
```
python test2_modified.py
```

### 4. test3.py - Dask Approach for Large Files

- Uses `dask` for handling large datasets
- Removes duplicates
- Designed for processing data that doesn't fit in memory
- Outputs: `male_dask.csv`, `female_dask.csv`, `unknown_dask.csv`

Usage:
```
python test3.py
```

### 5. test3_modified.py - Improved Dask Approach

- Uses `dask` with better naming conventions
- Preserves the original structure with minimal changes
- Has exception handling for error cases
- Outputs: `male.csv`, `female.csv`, `unknown.csv`

Usage:
```
python test3_modified.py
```

## Choosing the Right Approach

- For small files with standard processing: `test1.py` (CSV module)
- For medium-sized files with more concise code: `test2_modified.py` (Pandas)
- For very large files that don't fit in memory: `test3_modified.py` (Dask)

## Dependencies

- `csv` (standard library) - for test1.py
- `pandas` - for test2.py and test2_modified.py
- `dask` and `pyarrow` - for test3.py and test3_modified.py

Install dependencies:
```
pip install pandas dask pyarrow
``` 