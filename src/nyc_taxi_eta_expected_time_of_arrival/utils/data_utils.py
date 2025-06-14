import polars as pl


class Preprocess:
    @staticmethod
    def calculate_memory_usage(data: pl.DataFrame):
        return data.estimated_size("mb")

    @staticmethod
    def reduce_memory_usage(data: pl.DataFrame, print_info=True):
        """
        Reduce memory usage of a Polars DataFrame by casting columns to smaller data types.
        """
        if print_info:
            print(
                f"Memory usage before: {Preprocess.calculate_memory_usage(data):.2f} MB"
            )
        for column in data.columns:
            if data[column].dtype == pl.Int64:
                data = data.with_columns(data[column].cast(pl.Int32))
            elif data[column].dtype == pl.Float64:
                data = data.with_columns(data[column].cast(pl.Float32))
        if print_info:
            print(
                f"Memory usage after: {Preprocess.calculate_memory_usage(data):.2f} MB"
            )
        return data
