import sqlite3 

conn = sqlite3.connect("Text.db")
c = conn.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS text(
		data text NOT NULL
		)""")

data = """ 
"""

# c.execute("INSERT INTO text values(:data)", {"data":data})



# data = c.execute("select * from text").fetchall()
# see = data[1][0]



conn.commit()
conn.close()	