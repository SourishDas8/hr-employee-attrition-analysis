import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set page config
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

# Title & Description
st.title("HR Analytics & Employee Attrition Analysis")
st.markdown("""
Analyze HR data to understand factors influencing employee attrition.
Explore distributions, correlations, and interactive visualizations.
""")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("hr_analytics_dataset.csv")
    # Convert Attrition to numeric for plotting purposes (optional)
    df['Attrition'] = df['Attrition'].astype(int)
    return df

df = load_data()

# Show raw data toggle
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Sidebar filters
st.sidebar.header("Filters")
department_filter = st.sidebar.multiselect(
    "Select Department(s):", options=df['Department'].unique(), default=df['Department'].unique()
)
salary_filter = st.sidebar.multiselect(
    "Select Salary Level(s):", options=df['SalaryLevel'].unique(), default=df['SalaryLevel'].unique()
)

filtered_df = df[(df['Department'].isin(department_filter)) & (df['SalaryLevel'].isin(salary_filter))]

# Attrition distribution
st.subheader("Attrition Distribution")
fig1, ax1 = plt.subplots()
sns.countplot(data=filtered_df, x='Attrition', ax=ax1)
ax1.set_xticklabels(['Stayed', 'Left'])
st.pyplot(fig1)

# Department-wise Attrition Rate
st.subheader("Department-wise Attrition Rate")
dept_attr = filtered_df.groupby('Department')['Attrition'].mean().sort_values(ascending=False)
fig2, ax2 = plt.subplots()
dept_attr.plot(kind='bar', color='coral', ax=ax2)
ax2.set_ylabel('Attrition Rate')
st.pyplot(fig2)

# Correlation Heatmap
st.subheader("Correlation Heatmap")
numeric_df = filtered_df.select_dtypes(include=['number'])
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax3)
st.pyplot(fig3)

# Interactive Satisfaction vs Evaluation Plot
st.subheader("Satisfaction vs Evaluation (Colored by Attrition)")
fig4 = px.scatter(filtered_df, x='SatisfactionLevel', y='LastEvaluation',
                  color=filtered_df['Attrition'].astype(str),
                  labels={'color': 'Attrition'},
                  title='Satisfaction vs Last Evaluation')
st.plotly_chart(fig4, use_container_width=True)

# Key Insights
st.subheader("Key Insights")
st.markdown("""
- Sales and Support departments have higher attrition rates.
- Employees with low satisfaction and high evaluation scores tend to leave more.
- Lower salary levels correlate with higher attrition.
- Longer tenure sometimes increases attrition risk.
""")
