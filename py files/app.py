import streamlit as st
from predict_salary import show_predict_page
from explore_data import show_explore_data_page


def run_app():
    """This function runs the app"""
    page = st.sidebar.selectbox("Predict or Explore", options=["Predict", "Explore"], index=1)

    if page == "Predict":
        show_predict_page()
    else: 
        show_explore_data_page()


if __name__ == '__main__':
    run_app()