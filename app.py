import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openai
import os

# Set up OpenAI API Key (Replace with your own if needed)
os.environ["OPENAI_API_KEY"] = "your-free-api-key"
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("📊 Excel Data Visualization & AI Insights")

# Upload file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("## Preview of Data")
    st.write(df.head())
    
    # Select column for visualization
    column = st.selectbox("Select a column to visualize", df.columns)
    
    # Basic visualizations
    st.write("## Data Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df[column], kde=True, ax=ax)
    st.pyplot(fig)
    
    # Scatter Plot
    if len(df.columns) > 1:
        st.write("## Scatter Plot")
        x_col = st.selectbox("Select X-axis", df.columns, index=0)
        y_col = st.selectbox("Select Y-axis", df.columns, index=1)
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
        st.pyplot(fig)
    
    # AI-Powered Data Insights
    if st.button("Get AI Insights"):
        prompt = f"Provide key insights about the following dataset:\n{df.describe().to_string()}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a data analyst."},
                      {"role": "user", "content": prompt}]
        )
        st.write("### AI Insights:")
        st.write(response["choices"][0]["message"]["content"])
