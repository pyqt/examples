import sqlite3
connection = sqlite3.connect("projects.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE projects
    (url TEXT, descr TEXT, income INTEGER)
""")
cursor.execute("""INSERT INTO projects VALUES 
    ('giraffes.io', 'Uber, but with giraffes', 1900),
    ('dronesweaters.com', 'Clothes for cold drones', 3000),
    ('hummingpro.io', 'Online humming courses', 120000)
""")
connection.commit()