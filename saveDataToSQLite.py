import sqlite3
from wbAPI import wbAPI

# Connect to SQLite database
SQLITEPATH = 'my_database.db'

conn = sqlite3.connect(SQLITEPATH)

COUNTRIES = ["KEN", "SOM"]
WB_SERIES = {"NY.GDP.MKTP.PP.CD": "GDP_ppp", "FP.CPI.TOTL.ZG": "Inflation"}
DATERANGE = range(2000, 2024)
wb_data = wbAPI(countries=COUNTRIES, series=WB_SERIES, dateRange=DATERANGE).main()

# Save DataFrame to SQLite
wb_data.to_sql('other_table', conn, index=False, if_exists='replace')

# Close the connection
conn.close()