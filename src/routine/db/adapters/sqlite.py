# TODO

import sqlite3

connection = sqlite3.connect("test.db")
print(connection.total_changes)