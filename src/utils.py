# Import necessary libraries
import os       # For operating system interactions (e.g., file/directory handling)
import sys      # For system-specific parameters and functions (used in error handling)
import dill     # For serializing (saving) Python objects (like pickle but more powerful)
import numpy as np  # For numerical operations (not directly used here but often needed in ML workflows)
import pandas as pd # For data manipulation (not directly used here but common in ML projects)
from sklearn.metrics import r2_score
# Import a custom exception class for better error handling
from src.exception import CustomException

def save_object(file_path: str, obj: object) -> None:         #the function does not return anything
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
    
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            #para=param[list(models.keys())[i]]

           # gs = GridSearchCV(model,para,cv=3)
            #gs.fit(X_train,y_train)

            #model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)#learns patterns from data and develop a function best suited for ytrain

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)#y_train_pred!=y_train, the difference quantify the model's training error
 
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score#models.keys() return a view object which cannot be indexed, in order to support direct indexing we type cast it to lists

        return report

    except Exception as e:
        raise CustomException(e, sys)