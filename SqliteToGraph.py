import os
import sqlite3
import networkx as nx
import unittest

class SQLToGraphConverter:
    def __init__(self, db_path):
        """
        Initializes an SQLToGraphConverter object.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.db_path = db_path

    def extract_schema(self):
        """
        Extracts the schema information from the SQLite database.

        Returns:
            dict: A dictionary containing schema information for each table in the database.
                  The keys are table names, and the values are dictionaries with "columns" and "foreign_keys" keys.
        """
        schema_info = {}
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                cursor.execute(f"PRAGMA foreign_key_list({table_name})")
                foreign_keys = cursor.fetchall()
                schema_info[table_name] = {"columns": columns, "foreign_keys": foreign_keys}
        return schema_info

    def construct_graph(self, schema_info):
        """
        Constructs a directed graph from the schema information.

        Args:
            schema_info (dict): A dictionary containing schema information for each table in the database.

        Returns:
            networkx.DiGraph: A directed graph representing the relationships between tables and their columns.
        """
        G = nx.DiGraph()
        for table, details in schema_info.items():
            G.add_node(table, columns=details["columns"])
            for fk in details["foreign_keys"]:
                G.add_edge(table, fk[2], from_column=fk[3], to_column=fk[4])
        return G

    def find_paths(self, graph, fk1, fk2):
        """
        Finds paths in the graph where the start node has foreign key property `fk1`
        and the end node has foreign key property `fk2`.

        Args:
            graph (networkx.DiGraph): The directed graph representing the database schema.
            fk1 (str): The name of the first foreign key property.
            fk2 (str): The name of the second foreign key property.

        Returns:
            list: A list of paths (lists of table names) that connect nodes with the specified foreign key properties.
        """
        undirected_graph = nx.Graph(graph)  # Creating an undirected version of the graph
        paths = []
        for node in undirected_graph.nodes:
            if any(edge[2].get('from_column') == fk1 for edge in graph.out_edges(node, data=True)):
                for target in undirected_graph.nodes:
                    if any(edge[2].get('from_column') == fk2 for edge in graph.out_edges(target, data=True)):
                        for path in nx.all_simple_paths(undirected_graph, node, target):
                            paths.append(path)
        return paths
    

