import streamlit as st

st.title(" Simple Calculator")

# Input numbers
num1 = st.number_input("Enter first number")
num2 = st.number_input("Enter second number")

# Choose operation
operation = st.radio("Select operation", ["Add", "Subtract", "Multiply", "Divide"])

# Calculate
if st.button("Calculate"):
    if operation == "Add":
        result = num1 + num2
    elif operation == "Subtract":
        result = num1 - num2
    elif operation == "Multiply":
        result = num1 * num2
    elif operation == "Divide":
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Error: Division by zero"
    st.write("### Result:", result)

