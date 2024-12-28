import polars as pl
import pandas as pd

class FeatureEngineering:
    @staticmethod
    def prepare_features_and_labels(data: pl.DataFrame, label_column: str):
        """
        Prepares features (X) and labels (y) from a Polars DataFrame.
        """
        if label_column not in data.columns:
            raise ValueError(f"Label column '{label_column}' not found in the DataFrame.")
        
        # Separate features and labels
        X = data.drop(label_column).to_pandas()
        y = data[[label_column]].to_pandas()
        
        return X, y
