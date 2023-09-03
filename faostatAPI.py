import faostat
import pandas as pd

class faostatAPI(object):
    """
    Implementierung eines objektorientierten Programms zur Extraktion der UN "Food and
    Agriculture Organization".
    """

    def __init__(self, **kwargs) -> None:
        self.countries = kwargs.get("COUNTRIES")
        self.series = kwargs.get("SERIES")
        self.implemented_faostat_databases = ["FS"]

    def _check_if_database_implemented(self):
        # Check, ob alle abzufragenden Datenbanken bereits implementiert wurden
        # TODO: Was passiert, wenn einzelne implementiert sind (bsp: ["HI", "FS"]). Dann
        # TODO: sollte FS schon abgezogen werden, HI aber nicht.
        series_to_be_queried = [key for key in self.series.keys()]

        truth_series = [True if x in self.implemented_faostat_databases else False for x in series_to_be_queried]

        return all(truth_series)

    def extract_faostat_api_data(self) -> None:
        
        for key in self.series.keys():

            # FAOSTAT hat unterschiedliche Datumsformate für ihre unterschiedlichen
            # Datenbanken/Indikatoren, daher müssen wir prüfen, auf welche
            # Datenbank zugegriffen wird. 
            if key == "FS":
                
                # Jede Datenbank kann andere Area Codes haben. Daher muss hier nochmal
                # geprüft werden, ob die codes vorhanden sind und welche es für die 
                # jeweilige Datenbank sind. 
                country_codes_faostat = [faostat.get_areas(key)[i] for i in self.countries]

                self.faostatData = faostat.get_data_df(
                    key, 

                    # Aus der API Dokumentation: 
                    # "pars key can be one or more of the following 
                    # string: 'areas', 'years', 'elements', 'items'"

                    pars = {
                        "areas": country_codes_faostat,
                        "items": [key for key in self.series[key].keys()]

                    }
                )

            else:

                self.faostatData = None

    def transform_faostat_data(self):
        if self.faostatData is None:
            raise Exception("Es wurden keine Daten gefunden")
        
        self.faostatData = self.faostatData.replace({"Item Code":self.series["FS"]})
        self.faostatData["element_renamed"] = self.faostatData["Area"] + "_" + self.faostatData["Item Code"]
        self.faostatData["element_renamed"] = self.faostatData["element_renamed"].str.replace(" ", "_")

        self.faostatData["Value"] = self.faostatData["Value"].astype(float)

        self.faostatData["year"] = self.faostatData["Year"].str[:4].astype(int) + 1

        self.faostatData = self.faostatData.pivot(index = "year", columns = "element_renamed", values = "Value")

        self.faostatData.columns = [column.replace(r'[^a-zA-Z0-9]', '_') for column in self.faostatData.columns]


        
    def main(self):
        if not self._check_if_database_implemented():
            raise Exception("Keine der gewählten FAO Datenbanken ist implementiert. Suchen Sie sich eine aus folgender Liste aus: {}".format(self.implemented_faostat_databases))

        self.extract_faostat_api_data()
        self.transform_faostat_data()

        return self.faostatData

if __name__ == "__main__":
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

    faostat_data = faostatAPI(**config["FAO"]).main()
