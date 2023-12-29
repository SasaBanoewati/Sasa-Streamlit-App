import streamlit as st

st.set_page_config(layout="wide")
st.title("Ms. Power BI Unifi Dashboard")

# Display additional content or title
#st.markdown("# Power BI 1 Dashboard")
#st.markdown("")

power_bi_link = "https://app.powerbi.com/view?r=eyJrIjoiNmI5M2YxM2QtYTE5NS00MWMwLWE0MjgtMjZkNmNkZDhmZjcwIiwidCI6ImE2MGEzZWRmLTgzOTktNGQ5ZS1hMGEwLWQ3NGRjOTg1NDI2NCIsImMiOjEwfQ%3D%3D"

# Use st.components.iframe to embed the Power BI link
st.components.v1.iframe(power_bi_link, width=1500, height=600)


