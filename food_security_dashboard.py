import streamlit as st
from streamlitUtils import simple_line_chart

conn = st.experimental_connection('food_security_dashboard_db', type='sql')

world_bank_data = conn.query("select * from worldbank")
faostat_data = conn.query("select * from faostat")

tab1, tab2 = st.tabs(["Wirtschaftliche Entwicklung", "Ernährungsunsicherheit"])

with tab1: 

    col1, col2 = st.columns(2)

    with col1: 
        simple_line_chart(
            "Inflation Kenia",
            data =  world_bank_data,
            y_series_name="KEN_Inflation",
            x_series_name="index"
            )
       # st.markdown("Inflation Kenia", )
       # st.line_chart(data = world_bank_data["KEN_Inflation"])
    
    with col2:
        simple_line_chart("BIP in Mrd. USD (ppp in aktuellen USD) Kenia", world_bank_data["KEN_GDP_ppp"]/1000000000) 

with tab2: 

    st.header("Ernährungsunsicherheit")

    st.dataframe(world_bank_data)
    st.dataframe(faostat_data)