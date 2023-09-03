import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def simple_line_chart(title: str, x_series: pd.Series, y_series: pd.Series, y_label: str = "", x_label:str = "", ylim = None, legend_enabled: bool = False, legend_labels: list = None):
    
    st.markdown(title)
    fig, ax = plt.subplots()
    ax.plot(x_series, y_series)

    ax.set_ylabel(x_label)
    ax.set_xticks(range(x_series.min(), x_series.max(), 5))

    ax.set_ylabel(y_label)
    ax.yaxis.set_tick_params(length = 0)
    ax.yaxis.grid(True, color = "#c7cbd1")
    ax.spines[["right", "top", "left", "bottom"]].set_visible(False)

    if ylim is not None: 
        ax.set_ylim(ylim
        )

    if legend_enabled == True:
        ax.legend(legend_labels, fancybox=True, shadow=True, bbox_to_anchor = (0.5, -0.1), ncol = len(legend_labels), loc = "upper center")

    st.pyplot(fig)

def simple_area_chart(title: str, x_series: pd.Series, *args, labels: list):

    st.markdown(title)
    fig, ax = plt.subplots()

    ax.spines[["right", "top", "left", "bottom"]].set_visible(False)

    ax.stackplot(
        x_series, 
        *args,
        labels = labels,
        alpha = 0.7
    )

    ax.legend(labels, fancybox=True, shadow=True, bbox_to_anchor = (0.5, -0.1), ncol = len(labels), loc = "upper center")
    
    st.pyplot(fig)