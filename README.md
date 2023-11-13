## Overview
SqliteToGraph is a Python utility for converting Sqlite database schemas into graphs. This tool allows for the extraction of schema information from a Sqlite database, constructs a graph representation of the schema, and finds paths between tables based on foreign key relationships.

## Features
- **Schema Extraction**: Retrieves schema details from a Sqlite database, including tables, columns, and foreign keys.
- **Graph Construction**: Builds a directed graph where nodes are database tables and edges denote foreign key relationships.
- **Path Finding**: Identifies all possible paths between two tables in the database schema based on specified foreign key properties.

## Installation
Clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/BlaiseLabs/SqliteToGraph.git
cd SqliteToGraph
pip install -r requirements.txt
```

## Usage
Use the `SqlToGraphConverter` class in `SqliteToGraph.py` for operations. Here's a basic usage example:
```python
from SqliteToGraph import SqlToGraphConverter

# Initialize the converter with your Sqlite database path
converter = SqlToGraphConverter("./sample_database.db")

# Extract schema information
schema_info = converter.extract_schema()

# Construct a graph from the schema
graph = converter.construct_graph(schema_info)

# Find paths between tables based on foreign keys
paths = converter.find_paths(graph, "product_id", "user_id")
```

## Running Tests
To run the tests, use the following command:

```python
python -m unittest tests.py
```
