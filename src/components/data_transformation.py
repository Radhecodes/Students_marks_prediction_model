# --------- Standard Library Imports ----------
import sys                             # For accessing system-specific parameters and functions
from dataclasses import dataclass       # To create simple configuration classes

# --------- Third-Party Libraries ----------
import numpy as np                     # For numerical operations (e.g., arrays)
import pandas as pd                    # For data manipulation and loading CSVs

# --------- Scikit-learn Tools for Data Preprocessing ----------
from sklearn.compose import ColumnTransformer         # To apply different preprocessing on different columns
from sklearn.impute import SimpleImputer              # To handle missing values
from sklearn.pipeline import Pipeline                 # To build a sequence of preprocessing steps
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # To encode categorical data and scale numerical data

# --------- Custom Modules ----------
from src.exception import CustomException             # Custom exception class for cleaner error handling
from src.logger import logging                        # Custom logger to track execution flow
# --------- Miscellaneous ----------
import os                             # To work with file paths
from src.utils import save_object
# -----------------------------------------------------------------------------------------
# Configuration class to store the path where the preprocessor object will be saved
# -----------------------------------------------------------------------------------------
@dataclass
class DataTransformationConfig:
    # Creates a default file path for saving the serialized preprocessor object
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")

# -----------------------------------------------------------------------------------------
# Main class responsible for handling data preprocessing logic
# -----------------------------------------------------------------------------------------
class DataTransformation:

    def __init__(self):
        # Initialize the config which includes the path for saving the preprocessor
        self.data_transformation_config = DataTransformationConfig()
    # -------------------------------------------------------------------------
    # Method to build and return a preprocessing pipeline object
    # -------------------------------------------------------------------------
    def get_data_transformer_object(self):
        '''
        This function builds and returns a ColumnTransformer which applies:
        - Median imputation + Standard Scaling to numerical features
        - Most frequent imputation + One-Hot Encoding + Scaling to categorical features
        '''

        try:
            # List of numerical and categorical columns in the dataset
            numerical_columns = ["writing score", "reading score"]
            categorical_columns = [
                "gender",
                "race/ethnicity",
                "parental level of education",
                "lunch",
                "test preparation course",
            ]

            # Preprocessing pipeline for numerical data
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),     # Replace missing with median
                    ("scaler", StandardScaler())                      # Normalize the features
                ]
            )

            # Preprocessing pipeline for categorical data
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),  # Replace missing with most frequent value
                    ("one_hot_encoder", OneHotEncoder()),                 # Convert categorical to numeric
                    ("scaler", StandardScaler(with_mean=False))           # Scale the encoded values
                ]
            )

            # Logging the columns being processed
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Apply numerical and categorical pipelines to the respective columns
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            # Wrap and raise any exception with context
            raise CustomException(e, sys)

    # -------------------------------------------------------------------------
    # Method to initiate the data transformation process
    # -------------------------------------------------------------------------
    def initiate_data_transformation(self, train_path, test_path):
        '''
        This function:
        - Reads the train/test data from CSV
        - Separates features and target column
        - Applies preprocessing
        - Saves the preprocessing object
        - Returns processed arrays and the path to the saved preprocessor
        '''

        try:
            # Load the datasets
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")

            # Get the preprocessor pipeline (defined above)
            preprocessing_obj = self.get_data_transformer_object()

            # Define the name of the target column
            target_column_name = "math score"
            numerical_columns = ["writing score", "reading score"]

            # Separate input features and target for both train and test
            input_feature_train_df = train_df.drop(columns=[target_column_name])
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing data")

            # Fit the preprocessor on training data and transform
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)

            # Use the already-fitted preprocessor to transform test data
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine the transformed features with the target column
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object.")

            # Save the preprocessor object to disk using custom utility function
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            # Return the processed train/test arrays and the path to the saved object
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            # If any exception occurs, raise it with more context using CustomException
            raise CustomException(e, sys)
