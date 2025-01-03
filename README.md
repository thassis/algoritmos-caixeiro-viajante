# tsp-reader-app/tsp-reader-app/README.md

# TSP Reader Application

This project is a Python application designed to read and process TSP (Traveling Salesman Problem) files, specifically focusing on instances with EUC 2D and TSP format. It constructs a graph representation of the data using Networkx or iGraph.

## Project Structure

```
tsp-reader-app
├── src
│   ├── main.py        # Entry point of the application
│   ├── graph.py       # Contains the Graph class for managing graph structure
│   └── utils.py       # Utility functions for parsing and validating TSP files
├── tsp_examples
│   └── a280.tsp       # Example TSP file to be read by the application
├── requirements.txt    # Lists the dependencies required for the project
└── README.md           # Documentation for the project
```

## Requirements

To run this application, you need to install the required dependencies. You can do this by running:

```
pip install -r requirements.txt
```

## Usage

To execute the application, run the following command:

```
python src/main.py tsp_examples/a280.tsp
```

This command will read the specified TSP file, validate its format, and construct a graph representation of the data.

## TSP File Format

The TSP files used in this project should adhere to the following specifications:

- **Type**: TSP
- **Metric**: EUC 2D
- The file should contain a list of nodes with their coordinates.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.