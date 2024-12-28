import polars as pl

class DataPreprocessing:
    @staticmethod
    def preprocess(data: pl.DataFrame):
        """
        Apply necessary preprocessing steps: removing unwanted columns, transforming, etc.
        """
        # Example: Add 'dropoff_year' from 'dropoff_datetime'
        data = data.with_columns(pl.Series(name='dropoff_date', values=data['dropoff_datetime'].dt.date()))
        data = data.with_columns(pl.Series(name='dropoff_month', values=data['dropoff_datetime'].dt.month()))
        
        # Remove unwanted columns
        data = data.drop(['pickup_datetime', 'dropoff_datetime', 'request_datetime', 
                          'on_scene_datetime', 'hvfhs_license_num', 'airport_fee', 
                          'dispatching_base_num', 'shared_request_flag', 'originating_base_num',
                          'shared_match_flag', 'access_a_ride_flag', 'wav_request_flag', 
                          'wav_match_flag'])
        
        return data
