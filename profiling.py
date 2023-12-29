import pandas as pd
from pandas_profiling import ProfileReport
import streamlit as st
from streamlit_pandas_profiling import st_profile_report

csv_file_path = 'technical/data/food/wfp_food_prices_idn.csv'
data = pd.read_csv(csv_file_path, low_memory=False)

profile = ProfileReport(data, minimal=True,
                        title="Profiling Report: Food Price",
                        dataset= {
                        "description":    "This profiling report was generated for Albar's Medium",
                        "url (dataset)": "https://data.humdata.org/dataset/wfp-food-prices-for-indonesia",
                        },
                        )
profile.to_file("your_report.html")

st.title("Profiling Report: Food Price")
st_profile_report(profile)
