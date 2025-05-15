# NYC Taxi ETA Prediction

## Project Overview
This project aims to estimate the Expected Time of Arrival (ETA) for taxis in New York City. By leveraging weather data and taxi trip data sourced from the NYC Open Data platform, the project provides insights and predictions to improve transportation efficiency and user experience.

## Features
- **Data Processing**: Clean and preprocess raw taxi and weather data.
- **Machine Learning Models**: Train and evaluate models to predict taxi ETAs.
- **Deep Learning Models**: Explore advanced modeling techniques for better accuracy.
- **Visualization**: Analyze and visualize trip patterns and predictions.

## Project Structure
```
├── data/
│   ├── nyc_region_coordinates.csv
│   ├── nyc_tlc_yellow_taxi_data/
│   │   ├── yellow_tripdata_2009-01.parquet
│   │   └── ...
│   └── raw_data/
├── notebooks/
│   ├── data_processing.ipynb
│   ├── dl_modeling.ipynb
│   ├── downloader.ipynb
│   ├── ml_modeling.ipynb
│   └── starter.ipynb
├── public/
│   ├── data_dictionary_trip_records_fhv.pdf
│   ├── data_dictionary_trip_records_hvfhs.pdf
│   ├── nyc_multiple_rides_with_length.html
│   ├── personal_project_notes.docx
│   ├── shortest_path_finding.png
│   └── trip_record_user_guide.pdf
├── src/
│   └── uber_time_estimation/
├── pyproject.toml
├── README.md
└── uv.lock
```

## Getting Started

### Prerequisites
- Python 3.12 or higher
- Recommended: Virtual environment by `uv`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Ravikumarchavva/nyc-taxi-eta-expected-time-of-arrival.git
   cd nyc-taxi-eta-expected-time-of-arrival
   ```
2. Install dependencies:
   ```bash
   uv sync
   ```

### Data Setup
1. Download the NYC taxi and weather data from the NYC Open Data platform.
2. Place the data in the `data/` directory as per the structure above.

### Running the Project
- **Data Processing**: Run the `data_processing.ipynb` notebook to clean and preprocess the data.
- **Model Training**: Use `ml_modeling.ipynb` or `dl_modeling.ipynb` to train and evaluate models.
- **Visualization**: Explore trip patterns using the `starter.ipynb` notebook.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## Suggestions for Improvement
1. **Documentation**: Add detailed docstrings and comments in the codebase.
2. **Testing**: Implement unit tests for critical functions and models.
3. **Automation**: Create scripts for data downloading and preprocessing to streamline the workflow.
4. **Deployment**: Package the project for deployment as a web service or API.
5. **Visualization**: Enhance visualizations with interactive dashboards (e.g., using Plotly or Dash).

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- NYC Open Data platform for providing the taxi and weather datasets.
- Open-source contributors and libraries used in this project.