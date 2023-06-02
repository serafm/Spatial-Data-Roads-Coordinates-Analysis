# Road Network Analysis

This project focuses on analyzing a road network using data from a CSV file. It provides functions to read the road data, calculate the minimum bounding rectangle (MBR) for each road, and perform various analyses on the road network.

## Installation

To use this project, you need to have Python 3 installed. You can download Python from the official website: [python.org/downloads](https://www.python.org/downloads/)

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/Spatial-Data-Road-Network-Analysis.git
```

## Usage

1. Place your road data CSV file in the `data` directory. Make sure the CSV file has the correct format with road coordinates.
2. Modify the `read_roads_csv()` function in `main.py` to handle your specific CSV file structure if needed.
3. Run the `main.py` file:


The script will read the road data from the CSV file, calculate the MBR for each road, and perform various analyses on the road network.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please create a pull request. You can also open an issue to report bugs or discuss new features.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use and modify the code as per the license terms.

## Acknowledgements

The road data used in this project is sourced from the [TIGER/Line Shapefiles](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html) provided by the U.S. Census Bureau.
