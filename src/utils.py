# Import necessary libraries
import os       # For operating system interactions (e.g., file/directory handling)
import sys      # For system-specific parameters and functions (used in error handling)
import dill     # For serializing (saving) Python objects (like pickle but more powerful)
import numpy as np  # For numerical operations (not directly used here but often needed in ML workflows)
import pandas as pd # For data manipulation (not directly used here but common in ML projects)

# Import a custom exception class for better error handling
from src.exception import CustomException

def save_object(file_path: str, obj: object) -> None:
    """
    Saves a Python object to a specified file path using dill serialization.
    Creates directories if they don't exist.

    Args:
        file_path (str): Path where the object will be saved (e.g., "artifacts/model.pkl").
        obj (object): Python object to be saved (e.g., a trained ML model).

    Raises:
        CustomException: If an error occurs during saving.
    """
    try:
        # Step 1: Extract the directory path from the full file path
        # Example: If file_path is "artifacts/model.pkl", dir_path becomes "artifacts"
        dir_path = os.path.dirname(file_path)

        # Step 2: Create the directory (and parent directories) if they don't exist
        # exist_ok=True prevents errors if the directory already exists
        os.makedirs(dir_path, exist_ok=True)

        # Step 3: Save the object to the file using dill
        # "wb" mode = write in binary (required for serialization)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)  # Serialize and save the object

    except Exception as e:
        # Step 4: If any error occurs, raise a custom exception with the error details
        raise CustomException(e, sys)