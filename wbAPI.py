import wbgapi as wb
import pandas as pd


class wbAPI(object):
    """
    Implementierung eines objektorientierten Programms zur Extraktion von
    Weltbankdaten. Die Zeitreihen werden für die angegebenen Länder und den
    Datumsbereich abgerufen. Anschließend werden sie von einem "long-format"
    in ein "wide-format" umgewandelt.

    Die Methode main() orchestriert alle Methoden innerhalb der Klasse.
    """

    def __init__(self, **kwargs) -> None:
        """
        Parameters:
            countries (list): Liste der ISO3-Codes von Ländern, für die Zeitreihen heruntergeladen werden sollten.
            series (dict): Dictionary von Weltbank Zeitreihen IDs als  keys und den sprechenden Namen als value.
            dateRange (range): Range für die die Daten heruntergelanden werden sollen in Jahren.
        """

        self.countries = kwargs.get("COUNTRIES")
        self.series = kwargs.get("SERIES")
        self.dateRange = kwargs.get("DATERANGE")

    def extract_wb_api_data(self) -> None:
        """
        Funktion, die Daten der Weltbank extrahiert,
        indem sie sich mit der offiziellen und öffentlichen Weltbank-API verbindet.
        * Dokumentation:
            https://blogs.worldbank.org/opendata/introducing-wbgapi-
            new-python-package-accessing-world-bank-data
        """

        # Für eine sinnvolle benamung werden die Zeitreihen IDs in einem
        # dictionary gepflegt. Die Keys sind der sprechende Name, die
        # values die von der WB verwendete ID
        series = [key for key in self.series.keys()]

        data = wb.data.DataFrame(
            series,
            self.countries,
            self.dateRange,
            # Wichtig, damit Graphen später einfacher korrekt dargestellt werden können
            numericTimeKeys=True,
        )

        self.wbData = data

    def transform_wb_data(self):
        """
        Funktion um die Weltbank Daten in ein Datenformat zu bringen,
        welches gut in SQLite abgespeichert werden kann und die
        Abfrage von Daten im Frontend erleichtert.
        """

        self.wbData = self.wbData.reset_index()
        # Umbenennung der Spalte series in etwas sprechendes
        self.wbData["series"] = self.wbData["series"].replace(self.series)
        self.wbData.index = self.wbData["economy"] + "_" + self.wbData["series"]
        self.wbData = self.wbData.drop(["economy", "series"], axis=1)

        self.wbData = self.wbData.transpose()

    def main(self) -> pd.DataFrame:
        """
        Funktion, die die Orchestrierung der anderen Methoden des
        Programms steuert.
        """

        self.extract_wb_api_data()
        self.transform_wb_data()

        return self.wbData


if __name__ == "__main__":
    config = {
        "WB": {
            "COUNTRIES": ["KEN", "SOM"],
            "SERIES": {"NY.GDP.MKTP.PP.CD": "GDP_ppp", "FP.CPI.TOTL.ZG": "Inflation"},
            "DATERANGE": range(2000, 2024),
        },
        "FAO": {
            "COUNTRIES": ["Ethiopia", "Kenya", "Somalia"],
            "FAOSTAT_SERIES": {"FS": {"21001": "Number of people undernourished mil"}},
        },
    }

    wb_data = wbAPI(**config["WB"]).main()
