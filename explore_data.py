import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
plt.style.use("seaborn")
import seaborn as sns

# Helper Functions
def clean_devtype(descrptn: str) -> str:
    role = descrptn.split(";")[0]    # select the 1st split
    return role

def assign_devtype(devtype: str) -> str:
    """This function tidies up the job titles."""
    if devtype == 'Developer back-end':
        return 'Backend Developer'
    elif devtype == 'Developer full-stack':
        return 'Fullstack Developer'
    elif devtype == 'Database administrator':
        return 'Database Administrator'
    elif devtype == 'Data or business analyst':
        return 'Data/Business Analyst'
    elif devtype == 'Developer front-end':
        return 'Frontend Developer'
    elif (devtype == 'Academic researcher') or (devtype =='Scientist') or (devtype =='Educator'): 
        return 'Academic Researcher/Scientist'
    elif devtype == 'Designer':
        return 'Designer'
    elif devtype == 'Developer desktop or enterprise applications':
        return 'Desktop/Enterprise Applications Developer'
    elif devtype == 'Data scientist or machine learning specialist':
        return 'Data scientist/Machine Learning Specialist'
    elif devtype == 'Developer mobile':
        return 'Mobile Developer'
    elif devtype == 'Developer embedded applications or devices':
        return 'Embedded applications/devices Developer'
    elif devtype == 'DevOps specialist':
        return 'DevOps'
    elif devtype == 'Developer QA or test':
        return 'QA/Test Developer'
    
    elif devtype == 'Engineer data':
        return 'Data Engineer'
    elif devtype == 'Developer game or graphics':
        return 'Game/Graphics Developer'
    elif (devtype == 'Engineering manager') or (devtype =='Product manager'):
        return 'Engineering/Product Manager'
    else:
        return 'Others'

def edu_level(col: str) -> str:
    if col == "Bachelor’s degree (B.A., B.S., B.Eng., etc.)":
        return "Bachelor’s degree"
    elif col == "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)":
        return "Master’s degree"
    elif col == "Other doctoral degree (Ph.D., Ed.D., etc.)":
        return "Doctoral degree"
    elif col == "Some college/university study without earning a degree":
        return "College/University dropout"
    elif col == "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)":
        return "Secondary/High school"
    elif (col == "Associate degree (A.A., A.S., etc.)") or (col == "Professional degree (JD, MD, etc.)"):
        return "Associate/Professional degree"
    else:   # "Primary/elementary school", "I never completed any formal education"
        return "Less than Secondary/High school"

def clean_country(col: str) -> str:
    top_countries = ['United States','Others','India','United Kingdom','Germany','Canada','Brazil','France','Spain',
    'Australia','Netherlands','Poland','Italy','Russian Federation','Sweden','Turkey','Israel','Switzerland','Pakistan']

    if col in top_countries:
        return col
    else:
        return "Others"

def clean_years_code_pro(num: float) -> float:
    if num == "Less than 1 year":
        return 0.5
    elif num == "More than 50 years":
        return 50
    else: 
        return float(num)


@st.cache   # prevents the dataframe from reloading every time
def load_dataframe() -> pd.DataFrame:
    """Clean and load the data."""

    # load the data
    raw_data = pd.read_csv("data/survey_results_public.csv")
    # select the columns to use
    cols = "Country EdLevel DevType Employment WorkWeekHrs YearsCodePro ConvertedComp".split(" ")
    df = raw_data.copy()
    df = df[cols]
    # filter out all the columns without "ConvertedComp"
    df1 = df[df['ConvertedComp'].notna()]
    # remove the missing values in 'DevType'
    df1 = df1.dropna(subset=['DevType'])
    df2 = df1.copy()
    # clean the 'DevType'
    df2['DevType'] = df2['DevType'].str.replace(',', ' ')
    df2['DevType'] = df2['DevType'].apply(clean_devtype)
    # remove the excessive whitespaces
    df2['DevType'] = df2['DevType'].str.replace("  ", " ")
    # clean the DevType
    df2['DevType'] = df2['DevType'].apply(assign_devtype)
    # clean the EdLevel
    df2['EdLevel'] = df2['EdLevel'].apply(edu_level)
    df3 = df2.copy()
    # Exclude respondent that are not "Employed full-time"
    df3 = df3.loc[(df3["Employment"] == "Employed full-time")]
    # top 19 countries by frequency
    top_countries = [*df3["Country"].value_counts().index[:19]]
    # clean "Country"
    df3['Country'] = df3['Country'].apply(clean_country)
    # clean "YearsCodePro"
    df3['YearsCodePro'] = df3['YearsCodePro'].apply(clean_years_code_pro)
    # drop 'WorkWeekHrs' and 'Employment'
    df3 = df3.drop(columns=['WorkWeekHrs', 'Employment'])
    # replace the missing values in "YearsCodePro" with the median
    df3['YearsCodePro'] = df3['YearsCodePro'].fillna(value=df3['YearsCodePro'].median())
    df4 = df3.copy()
    # cut off i.e 10th percentile
    min_cut_off = np.percentile(df4['ConvertedComp'], 10)
    # cut off i.e 96th percentile
    max_cut_off = np.percentile(df4['ConvertedComp'], 96)
    df4 = df4.loc[(df4['ConvertedComp'] >= min_cut_off) & (df4['ConvertedComp'] <= max_cut_off)]
    # rename column
    df4.rename(columns={'ConvertedComp': 'Salary(USD)'}, inplace=True)

    return df4

my_df = load_dataframe() 

def show_explore_data_page():
    st.title("""
            Explore the Salaries of Developers
            ### Stack Overflow Developer Survey 2020
    """)
    nrows, ncols = 1, 1
    fig1, ax = plt.subplots(nrows, ncols, figsize=(14, 5))

    sns.countplot(data=my_df, x='Country', ax=ax, palette='Paired')
    ax.tick_params(axis='x', labelrotation=90, labelsize=12)
    
    for bar in ax.patches:
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        ax.annotate(text=y,                         # text pos
                xy=(x, y),                          # (x, y)
                xytext=(0, 6),                      # text position
                ha='center',                        # horizontal alignment
                va='center',                        # vertical alignment
                size=9,                             # text size
                textcoords='offset points')         # text coordinates???
        
    # fig1.tight_layout()
    # plt.show()
    st.write("""### Number of Countries""")
    st.pyplot(fig1)


    # a = my_df.groupby(['Country'])['Salary(USD)'].mean()  

    data = pd.crosstab(index=my_df['Country'], columns='Salary(USD)', aggfunc=np.mean, values=my_df['Salary(USD)'])
    data.columns = ['Salary(USD)']
    data['Salary(USD)'] = data['Salary(USD)'].apply(lambda x: round(x, 2))
    st.write("""### Mean Salary of The Countries""")
    st.bar_chart(data, width=400, height=400)
