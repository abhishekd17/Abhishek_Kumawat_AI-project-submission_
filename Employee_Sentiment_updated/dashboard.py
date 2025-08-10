import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
try:
    df = pd.read_excel('outputs/comprehensive_sentiment_analysis_report.xlsx', sheet_name='Analyzed_Data')
except FileNotFoundError:
    st.error("Excel file not found. Please ensure 'outputs/comprehensive_sentiment_analysis_report.xlsx' exists.")
    st.stop()

# Check and compute 'score' if missing
if 'score' not in df.columns:
    sentiment_scores = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
    if 'sentiment' in df.columns:
        df['score'] = df['sentiment'].map(sentiment_scores)
        st.info("'score' column was missing—computed it from 'sentiment'.")
    else:
        st.error("'sentiment' column is missing from the data. Cannot compute scores.")
        st.stop()

# Convert 'month' to string for filtering if needed
df['month'] = df['month'].astype(str)

st.title('Employee Sentiment Dashboard')
st.sidebar.header('Filters')
selected_month = st.sidebar.selectbox('Select Month', sorted(df['month'].unique()))

# Filter data
filtered_df = df[df['month'] == selected_month]

# Sentiment Distribution
st.subheader('Sentiment Distribution')
fig, ax = plt.subplots()
sns.countplot(x='sentiment', data=filtered_df, ax=ax)
st.pyplot(fig)

# Top Employees
st.subheader('Top Positive/Negative Employees')
employee_scores = filtered_df.groupby('from')['score'].sum().sort_values(ascending=False)
st.write("**Top Positive:**")
st.dataframe(employee_scores.head(3).reset_index())
st.write("**Top Negative:**")
st.dataframe(employee_scores.tail(3).reset_index())

# Flight Risk (Placeholder—replace with your actual list or computation)
st.subheader('Flight Risk Employees')
flight_risks = ['emp1', 'emp2']  # Replace with actual list from your analysis
st.write(flight_risks)
