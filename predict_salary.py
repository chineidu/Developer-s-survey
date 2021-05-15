import numpy as np
import pandas as pd
import streamlit as st
import pickle

def load_model() -> "pickle_object":
    """
    This function returns a pickle object containing a Random Forest trained regressor, a Label Encoders for 
    Country, DevType and Education level.
    """
    
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    return model

model = load_model()

regressor = model['regressor']
le_country = model['le_country']
le_devtype = model['le_devtype']
le_education = model['le_education']




def show_predict_page():
    """
    This function displays the predict page.
    """
    st.title(""" 
                     Salary Predictor
            ### Made by ['Neidu](https://github.com/chineidu)
                    """)

    st.info("Please enter some information to be used to predict the salary")

    country = ['Australia', 'Brazil', 'Canada', 'France', 'Germany', 'India','Israel','Italy', 'Netherlands', 'Pakistan', 'Poland',
        'Russian Federation', 'South Africa', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'United Kingdom', 'United States']

      
    education = [ 'Less than Secondary/High school', 'Secondary/High school', 'College/University dropout', 'Associate/Professional degree',   
     'Bachelor’s degree', 'Master’s degree', 'Doctoral degree', ]
    
    devtype = ['Backend Developer', 'Fullstack Developer', 'Database Administrator', 'Frontend Developer', 
    'Data/Business Analyst', 'Academic Researcher/Scientist', 'Desktop/Enterprise Applications Developer', 
    'Designer', 'Data scientist/Machine Learning Specialist', 'Mobile Developer', 'Embedded applications/devices Developer', 
    'DevOps', 'QA/Test Developer', 'Engineering/Product Manager', 'Data Engineer', 'Game/Graphics Developer']
    
    country = st.selectbox("Countries", country, index=0)
    education = st.selectbox("Education Level", education, index=0)
    devtype = st.selectbox("DevType", devtype, index=3)
    years_experience = st.number_input("Years of Coding", min_value=1, max_value=50, help="Please select the number of years you have coded")

    predict_buttion = st.button("Calculate Salary", help="Click this buttopn to calculate salary")
    if predict_buttion:
        # make predictions for new data
        #              Country,   Edlevel,  DevType,  YearsCodePro
        X = np.array([[country, education, devtype, years_experience]]) 

        # encode Country
        X[:, 0] = le_country.transform(X[:, 0])

        # encode EdLevel
        X[:, 1] = le_education.transform(X[:, 1])

        # encode DevType
        X[:, 2] = le_devtype.transform(X[:, 2])    

        # Apply log transformation to YearsCodePro
        X[:, 3] = np.log(int(X[:, 3]) + 1) 

        pred = regressor.predict(X)
        salary = np.exp(pred)
        salary = round(salary[0], 2)
        # display prediction
        st.success(f"Your estimated salary is: ${salary:,}")
        