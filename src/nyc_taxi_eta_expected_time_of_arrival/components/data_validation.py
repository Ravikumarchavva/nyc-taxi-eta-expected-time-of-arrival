import polars as pl
from configs.data_configs import PROCESSED_FILE_LIST  # Added import
import os
from tqdm.auto import tqdm


class DataValidation:
    """
    A class to validate data and prepare features and labels.
    """

    def __init__(self, PREPROCESSED_DATA_DIR):
        self.PREPROCESSED_DATA_DIR = PREPROCESSED_DATA_DIR

    @staticmethod
    def prepare_features_and_labels(data: pl.DataFrame, label_column: str):
        """
        Prepares features (X) and labels (y) from a Polars DataFrame.
        """
        if label_column not in data.columns:
            raise ValueError(
                f"Label column '{label_column}' not found in the DataFrame."
            )

        # Separate features and labels
        X = data.drop(label_column).to_pandas()
        y = data[[label_column]].to_pandas()

        return X, y

    @staticmethod
    def validate_missing_values(data: pl.DataFrame):
        """
        Validate if there are any missing values in the dataset.
        """
        missing = data.null_count()
        if missing.any():
            print(
                f"Warning: Missing values detected in columns: {missing[missing > 0]}"
            )

    @staticmethod
    def validate_data_types(data: pl.DataFrame):
        """
        Validate the data types of the columns.
        """
        expected_types = {
            "pickup_datetime": pl.Datetime,
            "dropoff_datetime": pl.Datetime,
            "tip_amount": pl.Float64,
            # Add other columns with expected types here
        }

        for column, expected_type in expected_types.items():
            if column in data.columns:
                actual_type = data[column].dtype
                if actual_type != expected_type:
                    print(
                        f"Warning: Column '{column}' is expected to be of type {expected_type}, but found {actual_type}."
                    )

    def validate_data(self):
        """
        Validate the data and prepare features and labels.
        """
        features_dir = os.path.join(self.PREPROCESSED_DATA_DIR, "features")
        labels_dir = os.path.join(self.PREPROCESSED_DATA_DIR, "labels")
        os.makedirs(features_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)

        for file_path in tqdm(PROCESSED_FILE_LIST, desc="Validating data files"):
            data = pl.read_parquet(file_path)

            # Perform validation checks
            self.validate_missing_values(data)
            self.validate_data_types(data)

            # Prepare features and labels
            X, y = self.prepare_features_and_labels(data, label_column="tip_amount")

            # Save features and labels to separate directories
            features_file_path = os.path.join(
                features_dir, f"features_{os.path.basename(file_path)}"
            )
            labels_file_path = os.path.join(
                labels_dir, f"labels_{os.path.basename(file_path)}"
            )

            # Convert pandas DataFrame back to Parquet for features and labels
            X.to_parquet(features_file_path, index=False)
            y.to_parquet(labels_file_path, index=False)

            print(
                f"Validated and saved features and labels for {os.path.basename(file_path)}."
            )
