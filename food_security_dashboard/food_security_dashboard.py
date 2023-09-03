import streamlit as st
from food_security_dashboard.streamlitUtils import simple_line_chart, simple_area_chart

# Laden der Daten von der SQLite Datenbank
conn = st.experimental_connection("food_security_dashboard_db", type="sql")

world_bank_data = conn.query("select * from worldbank")
faostat_data = conn.query("select * from faostat")

st.title("Analyse Horn von Afrika")

with st.expander("Kurzbeschreibung"):
    st.markdown("Im Rahmen meiner Bewerbung auf das Young Fellow Progamm der DGAP ist folgende Auswertung von Daten zum Horn von Afrika (Kenia, Äthiopien, Somalia) entstanden.\n Die Daten für die Analyse kommen von der Weltbank und von der Food and Agriculture Organization der UN. Im Rahmen meiner Arbeit beschäftige ich mich mit vergleichbaren Daten. Die Wahl der Region ist unabhängig von meiner beruflichen Tätigkeit gefallen.")

tab1, tab2, tab3 = st.tabs(["Wirtschaftliche Entwicklung", "Ernährungsunsicherheit", "Rohdaten"])

with tab1:
    st.subheader("Kenia")

    col1, col2 = st.columns(2)

    with col1:
        simple_line_chart(
            title="Inflation in %",
            y_series=world_bank_data["KEN_Inflation"],
            x_series=world_bank_data["index"],
            ylim=(
                0,
                world_bank_data["KEN_Inflation"].max()
                + 0.3 * world_bank_data["KEN_Inflation"].max(),
            ),
        )

        simple_line_chart(
            title="Exporte und Importe in Mrd. USD",
            y_series=world_bank_data[["KEN_Exports", "KEN_Imports"]] / 1000000000,
            x_series=world_bank_data["index"],
            legend_enabled=True,
            legend_labels=["Exporte", "Importe"],
            ylim=0,
        )

    with col2:
        simple_line_chart(
            title="BIP in Mrd. USD (ppp in aktuellen USD)",
            y_series=world_bank_data["KEN_GDP_ppp"] / 1000000000,
            x_series=world_bank_data["index"],
        )

        simple_area_chart(
            "Verteilung Alter Bevölkerung",
            world_bank_data["index"],
            world_bank_data["KEN_bevoelkerung_0_14"],
            world_bank_data["KEN_bevoelkerung_14_65"],
            world_bank_data["KEN_bevoelkerung_65_plus"],
            labels=["0-13 Jahre", "14-64 Jahre", "65 + Jahre"],
        )

    st.divider()
    st.subheader("Somalia")

    col1, col2 = st.columns(2)

    with col1:
        simple_line_chart(
            title="Inflation in %",
            y_series=world_bank_data["SOM_Inflation"],
            x_series=world_bank_data["index"],
            ylim=(
                0,
                world_bank_data["KEN_Inflation"].max()
                + 0.3 * world_bank_data["KEN_Inflation"].max(),
            ),
        )

        simple_line_chart(
            title="Exporte und Importe in Mrd. USD",
            y_series=world_bank_data[["SOM_Exports", "SOM_Imports"]] / 1000000000,
            x_series=world_bank_data["index"],
            legend_enabled=True,
            legend_labels=["Exporte", "Importe"],
            ylim=0
            # ylim = (0, world_bank_data["KEN_Inflation"].max() + 0.3 * world_bank_data["KEN_Inflation"].max())
        )

    with col2:
        simple_line_chart(
            title="BIP in Mrd. USD (ppp in aktuellen USD)",
            y_series=world_bank_data["SOM_GDP_ppp"] / 1000000000,
            x_series=world_bank_data["index"],
        )

        simple_area_chart(
            "Verteilung Alter Bevölkerung",
            world_bank_data["index"],
            world_bank_data["SOM_bevoelkerung_0_14"],
            world_bank_data["SOM_bevoelkerung_14_65"],
            world_bank_data["SOM_bevoelkerung_65_plus"],
            labels=["0-13 Jahre", "14-64 Jahre", "65 + Jahre"],
        )

    st.markdown("\*Für Somalia liegen die Daten teilweise nur eingeschränkt vor.", unsafe_allow_html=True )

    st.divider()
    st.subheader("Äthiopien")

    col1, col2 = st.columns(2)

    with col1:
        simple_line_chart(
            title="Inflation in %",
            y_series=world_bank_data["ETH_Inflation"],
            x_series=world_bank_data["index"],
            ylim=(
                world_bank_data["ETH_Inflation"].min()
                - 0.3 * abs(world_bank_data["ETH_Inflation"].min()),
                world_bank_data["ETH_Inflation"].max()
                + 0.3 * world_bank_data["ETH_Inflation"].max(),
            ),
        )

        simple_line_chart(
            title="Exporte und Importe in Mrd. USD",
            y_series=world_bank_data[["ETH_Exports", "ETH_Imports"]] / 1000000000,
            x_series=world_bank_data["index"],
            legend_enabled=True,
            legend_labels=["Exporte", "Importe"],
            ylim=0,
        )

    with col2:
        simple_line_chart(
            title="BIP in Mrd. USD (ppp in aktuellen USD)",
            y_series=world_bank_data["ETH_GDP_ppp"] / 1000000000,
            x_series=world_bank_data["index"],
        )

        simple_area_chart(
            "Verteilung Alter Bevölkerung",
            world_bank_data["index"],
            world_bank_data["ETH_bevoelkerung_0_14"],
            world_bank_data["ETH_bevoelkerung_14_65"],
            world_bank_data["ETH_bevoelkerung_65_plus"],
            labels=["0-13 Jahre", "14-64 Jahre", "65 + Jahre"],
        )
    
    st.divider()
    st.caption("Quelle: Weltbank")


with tab2:
    st.subheader("Kenia")
    col1, col2 = st.columns(2)
    
    with col1: 
        simple_line_chart(
            title = "Anteil unterernährter Menschen in %",
            x_series=faostat_data["year"],
            y_series= faostat_data["Kenya_210041"]
        )
       

        simple_line_chart(
            title = "\nImportanteil Getreide am Konsum in %",
            x_series=faostat_data["year"],
            y_series= faostat_data["Kenya_Cereal_import_Abhängigkeit"]
        )

    with col2:
        # 
        simple_line_chart(
            title = "Anteil landw. Nutzfläche, das für Bewässerung ausgestattet ist in %",
            x_series=faostat_data["year"],
            y_series= faostat_data["Kenya_Anteil_Land_zur_Bewaesserung"]*100
        )

        simple_line_chart(
            title = "Durchschnittliche Energiedeckung in %",
            x_series=faostat_data["year"],
            y_series= faostat_data["Kenya_Durschnittliche_Energie_adequacy"]
        )
    
    st.divider()
    st.subheader("Somalia")

    col1, col2 = st.columns(2)
    
    with col1: 
        simple_line_chart(
            title = "Anteil unterernährter Menschen in %",
            x_series=faostat_data["year"],
            y_series= faostat_data["Somalia_210041"]
        )
       

        #simple_line_chart(
        #    title = "\nImportanteil Getreide am Konsum in %",
        #    x_series=faostat_data["year"],
        #    y_series= faostat_data["Somalia_Cereal_import_Abhängigkeit"]
        #)

        simple_line_chart(
            title = "Durchschnittliche Energiedeckung in %",
            x_series=faostat_data["year"],
            y_series= faostat_data["Somalia_Durschnittliche_Energie_adequacy"]
        )

    with col2:
        simple_line_chart(
            title = "Anteil landw. Nutzfläche, das für Bewässerung ausgestattet ist in %",
            x_series=faostat_data["year"],
            y_series= faostat_data["Somalia_Anteil_Land_zur_Bewaesserung"]*100
        )

    st.divider()
    st.subheader("Äthiopien")

    col1, col2 = st.columns(2)

    with col1: 
        simple_line_chart(
            title = "Anteil unterernährter Menschen in %",
            x_series=faostat_data["year"],
            y_series= faostat_data["Ethiopia_210041"]
        )
       

        simple_line_chart(
            title = "\nImportanteil Getreide am Konsum in %",
            x_series=faostat_data["year"],
            y_series= faostat_data["Ethiopia_Cereal_import_Abhängigkeit"]
        )

    with col2:
        simple_line_chart(
            title = "Anteil landw. Nutzfläche, das für Bewässerung ausgestattet ist in %",
            x_series=faostat_data["year"],
            y_series= faostat_data["Ethiopia_Anteil_Land_zur_Bewaesserung"]*100
        )

        #simple_line_chart(
        #    title = "Durchschnittliche Energiedeckung in %",
        #    x_series=faostat_data["year"],
        #    y_series= faostat_data["Ethiopia__Durschnittliche_Energie_adequacy"]
        #)
    
    st.divider()
    st.markdown("\*Für Somalia und Äthiopien liegen die Daten teilweise nur eingeschränkt vor.", unsafe_allow_html=True )
    st.caption("Quelle: UN Food and Agriculture Organization")

with tab3:
    st.title("Weltbank Daten")
    st.dataframe(world_bank_data)

    st.divider()

    st.title("FAO Daten")
    st.dataframe(faostat_data)
