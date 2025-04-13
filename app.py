import streamlit as st

# Set a title for the app
st.title("Hello World from Codespaces! version 2")

# Write some text
st.write("This Streamlit app is running inside GitHub Codespaces.")
st.write("It's pretty cool!")

# Add a little fun element
if st.button("Click me for balloons!"):
    st.balloons()