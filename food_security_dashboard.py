import streamlit as st
from streamlitUtils import simple_line_chart, simple_area_chart

conn = st.experimental_connection("food_security_dashboard_db", type="sql")

world_bank_data = conn.query("select * from worldbank")
faostat_data = conn.query("select * from faostat")

tab1, tab2 = st.tabs(["Wirtschaftliche Entwicklung", "Ernährungsunsicherheit"])

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

with tab2:
    st.header("Ernährungsunsicherheit")

    st.dataframe(world_bank_data)
    st.dataframe(faostat_data)
