import unittest
import sqlite3
import os
from SqliteToGraph import SQLToGraphConverter
import matplotlib.pyplot as plt
import networkx as nx

class TestSQLToGraphConverter(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
      cls.db_path = './test.db'  # Set your database path here
      cls.converter = SQLToGraphConverter(cls.db_path)
      cls.create_sample_database()

  @classmethod
  def tearDownClass(cls):
      # Clean up the database file after tests
      os.remove(cls.db_path)

  @staticmethod
  def create_sample_database():
      with sqlite3.connect(TestSQLToGraphConverter.db_path) as conn:
          # Create the connection to the database
          conn = sqlite3.connect('test.db')

          # Create the 'users' table
          conn.execute('''
              CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE
              )
          ''')

          # Create the 'addresses' table
          conn.execute('''
              CREATE TABLE IF NOT EXISTS addresses (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  street_address TEXT NOT NULL,
                  city TEXT NOT NULL,
                  state TEXT NOT NULL,
                  zip_code TEXT NOT NULL,
                  user_id INTEGER NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users(id)
              )
          ''')

          # Create the 'orders' table
          conn.execute('''
              CREATE TABLE IF NOT EXISTS orders (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  order_date DATETIME NOT NULL,
                  user_id INTEGER NOT NULL,
                  shipping_address_id INTEGER NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users(id),
                  FOREIGN KEY (shipping_address_id) REFERENCES addresses(id)
              )
          ''')

          # Create the 'order_items' table
          conn.execute('''
              CREATE TABLE IF NOT EXISTS order_items (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  order_id INTEGER NOT NULL,
                  product_id INTEGER NOT NULL,
                  quantity INTEGER NOT NULL,
                  FOREIGN KEY (order_id) REFERENCES orders(id),
                  FOREIGN KEY (product_id) REFERENCES products(id)
              )
          ''')

          # Create the 'products' table
          conn.execute('''
              CREATE TABLE IF NOT EXISTS products (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  price DECIMAL(10,2) NOT NULL,
                  category_id INTEGER NOT NULL,
                  FOREIGN KEY (category_id) REFERENCES categories(id)
              )
          ''')

          # Create the 'categories' table
          conn.execute('''
              CREATE TABLE IF NOT EXISTS categories (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL
              )
          ''')

          # Commit the changes to the database
          conn.commit()

  def test_extract_schema(self):
      """
      Test the extract_schema method of SQLToGraphConverter.
      """
      schema_info = self.converter.extract_schema()
      self.assertIn("products", schema_info)
      self.assertIn("orders", schema_info)

  def test_construct_graph(self):
      """
      Test the construct_graph method of SQLToGraphConverter.
      """
      schema_info = self.converter.extract_schema()
      graph = self.converter.construct_graph(schema_info)
      self.assertIn("products", graph.nodes)
      self.assertIn("order_items", graph.nodes)
      self.assertTrue(graph.has_edge("order_items", "products"))

  def test_find_paths(self):
      """
      Test the find_paths method of SQLToGraphConverter.
      """
      schema_info = self.converter.extract_schema()
      graph = self.converter.construct_graph(schema_info)
      paths = self.converter.find_paths(graph, "category_id", "user_id")
      self.assertTrue(any(path for path in paths if "products" in path and "orders" in path))
      nx.draw(graph, with_labels=True)
      plt.savefig("test_graph.png")

if __name__ == "__main__":
  unittest.main(argv=['first-arg-is-ignored'], exit=False)
