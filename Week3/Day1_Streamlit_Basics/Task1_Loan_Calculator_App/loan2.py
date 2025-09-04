import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Loan Calculator", layout="wide")
st.title("💰Loan Calculator")

# USER INPUTS
with st.sidebar:
    st.header("👤 User Details")
    name = st.text_input("Enter your name:")
    age = st.number_input("Age:", min_value=18, max_value=100, value=25)
    
    st.header("💵 Loan Details")
    principal = st.number_input("Loan Amount (₹):", min_value=1000, value=50000, step=1000)
    annual_rate = st.slider("Annual Interest Rate (%):", min_value=1.0, max_value=20.0, value=5.0, step=0.1)
    duration_years = st.number_input("Loan Duration (years):", min_value=1, max_value=30, value=5)
    
    st.header("⚡ Additional Options")
    monthly_contribution = st.checkbox("Include extra monthly payment")
    extra_payment = st.number_input("Extra monthly payment (₹):", min_value=0, value=0) if monthly_contribution else 0

# CALCULATIONS
months = duration_years * 12
monthly_rate = annual_rate / 100 / 12
monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)
monthly_payment += extra_payment

# Generate amortization schedule
schedule = []
balance = principal
for month in range(1, months+1):
    interest = balance * monthly_rate
    principal_paid = monthly_payment - interest
    balance -= principal_paid
    balance = max(balance, 0)
    schedule.append([month, monthly_payment, principal_paid, interest, balance])

df_schedule = pd.DataFrame(schedule, columns=["Month", "Payment", "Principal Paid", "Interest Paid", "Balance"])

# DISPLAY RESULTS
st.subheader(f"Hello {name}, here are your loan details:")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Payment", f"₹{monthly_payment:,.2f}")
col2.metric("Total Payment", f"₹{df_schedule['Payment'].sum():,.2f}")
col3.metric("Total Interest Paid", f"₹{df_schedule['Interest Paid'].sum():,.2f}")

# GRAPHS 
st.subheader("📊 Loan Payment Graphs")

# Remaining balance line chart
fig_balance = px.line(df_schedule, x="Month", y="Balance", 
                      title="Remaining Loan Balance Over Time",
                      line_shape='spline', color_discrete_sequence=['#FF5733'])
st.plotly_chart(fig_balance, use_container_width=True)

# Principal vs Interest stacked area chart
fig_stack = px.area(df_schedule, x="Month", y=["Principal Paid", "Interest Paid"],
                    title="Principal vs Interest Paid Over Time",
                    color_discrete_sequence=['#33FF57','#3357FF'])
st.plotly_chart(fig_stack, use_container_width=True)

# Pie chart for total principal vs interest
fig_pie = px.pie(names=["Principal","Interest"], values=[principal, df_schedule['Interest Paid'].sum()],
                 title="Total Payment Breakdown", color_discrete_sequence=['#FF5733','#3357FF'])
st.plotly_chart(fig_pie, use_container_width=True)

# AMORTIZATION SCHEDULE
st.subheader("📄 Amortization Schedule")
st.dataframe(df_schedule.style.format({"Payment":"₹{:,.2f}", 
                                      "Principal Paid":"₹{:,.2f}", 
                                      "Interest Paid":"₹{:,.2f}", 
                                      "Balance":"₹{:,.2f}"}))

# DOWNLOAD CSV
csv_data = df_schedule.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Schedule CSV",
    data=csv_data,
    file_name="amortization_schedule.csv",
    mime="text/csv"
)

