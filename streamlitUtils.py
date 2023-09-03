import pandas as pd
import streamlit as st


def simple_line_chart(
    title: str, data: pd.DataFrame, y_series_name: str, x_series_name: str
):
    st.markdown(title)
    st.line_chart(data=data, y=y_series_name, x=x_series_name)
