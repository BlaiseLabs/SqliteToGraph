import sqlite3
import matplotlib.pyplot as plt
import networkx as nx
from SqliteToGraph import SQLToGraphConverter


if __name__ == '__main__':
  # has the same schema as the db used for tests 
  db_path = "./sample_database.db"
  converter = SQLToGraphConverter(db_path)
  schema_info = converter.extract_schema()
  graph = converter.construct_graph(schema_info)
  paths = converter.find_paths(graph, "category_id", "user_id")
  for path in paths:
      print(path)