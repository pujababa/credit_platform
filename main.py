import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Credit Platform", layout="centered")
st.title("Credit Platform")
st.write("Predict credit eligibility using ML model")

# User inputs
age = st.number_input("Age", 18, 100, 30)
income = st.number_input("Income", 1000, 1000000, 50000)
credit_history = st.selectbox("Credit History", ["Good", "Average", "Poor"])
loan_amount = st.number_input("Loan Amount", 1000, 1000000, 200000)

if st.button("Predict"):
    # Prediction logic
    if income > 30000 and credit_history == "Good":
        st.success("Credit Eligibility: Eligible")
    else:
        st.success("Credit Eligibility: Not Eligible")

    st.write("### Income vs Loan Amount")
    # Bar chart
    fig, ax = plt.subplots()
    ax.bar(["Income", "Loan Amount"], [income, loan_amount], color=['green','red'])
    ax.set_ylabel("Amount")
    st.pyplot(fig)

    st.write("### Age vs Income Scatter Plot")
    # Scatter plot using Plotly for interactivity
    df = pd.DataFrame({
        "Age": [age],
        "Income": [income]
    })
    scatter_fig = px.scatter(df, x="Age", y="Income", size=[income/1000], color=[income], labels={"Age":"Age", "Income":"Income"}, title="Age vs Income")
    st.plotly_chart(scatter_fig)
