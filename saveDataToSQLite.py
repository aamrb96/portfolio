import sqlite3
from wbAPI import wbAPI
from faostatAPI import faostatAPI


class saveDataToSQLite(object):
    def __init__(
        self, wb_api_instance: wbAPI, faostat_api_instance: faostatAPI
    ) -> None:
        self.wb_api = wb_api_instance
        self.faostat_api = faostat_api_instance

        self.wb_data = self.wb_api.main()
        self.faostat_data = self.faostat_api.main()

    def saveToSqlLite(self, path: str):
        conn = sqlite3.connect(path)

        self.wb_data.to_sql("worldbank", conn, index=True, if_exists="replace")
        self.faostat_data.to_sql("faostat", conn, index=True, if_exists="replace")

        conn.close()


if __name__ == "__main__":
    # Connect to SQLite database
    SQLITEPATH = "food_security_dashboard.db"

    # Definition config Dictionary mit **kwargs
    config = {
        "WB": {
            "COUNTRIES": ["KEN", "SOM", "ETH"],
            "SERIES": {
                "NY.GDP.MKTP.PP.CD": "GDP_ppp",
                "FP.CPI.TOTL.ZG": "Inflation",
                "NE.EXP.GNFS.CD": "Exports",
                "NE.IMP.GNFS.CD": "Imports",
                "SP.POP.0014.TO.ZS": "bevoelkerung_0_14",
                "SP.POP.1564.TO.ZS": "bevoelkerung_14_65",
                "SP.POP.65UP.TO.ZS": "bevoelkerung_65_plus"
            },
            "DATERANGE": range(2000, 2024),
        },
        "FAO": {
            "COUNTRIES": ["Ethiopia", "Kenya", "Somalia"],
            "SERIES": {"FS": {
                "21001": "Anzahl Unterernährter Menschen",
                "21004":"Anteil Unternährter Menschen",
                "21010":"Durschnittliche Energie adequacy",
                "21035":"Cereal import Abhängigkeit",
                "21034":"Anteil Land zur Bewaesserung"
                }
            },
        },
    }

    wb_api = wbAPI(**config["WB"])
    faostat_api = faostatAPI(**config["FAO"])

    dataObjects = saveDataToSQLite(wb_api, faostat_api)

    dataObjects.saveToSqlLite(path=SQLITEPATH)
