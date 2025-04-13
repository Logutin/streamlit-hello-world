# app.py
import streamlit as st
import pandas as pd
import io

# Import the function from your utils file
from utils import extract_last_table_as_df

# --- Initialize Session State ---
# Use session state to store persistent info across reruns
if 'uploaded_file_bytes' not in st.session_state:
    st.session_state.uploaded_file_bytes = None
    st.session_state.uploaded_file_name = None
    st.session_state.dataframe_result = None # Store the result of the LAST processing
    st.session_state.processing_attempted = False # Track if Process button was clicked

# --- Main App Logic ---
st.title("DOCX Table Extractor with Process Button")

# --- File Uploader ---
uploaded_file = st.file_uploader(
    "1. Choose a DOCX file",
    type=["docx"],
    key="file_uploader" # Added a key for potential future state management needs
)

# --- Store/Update Uploaded File Details ---
# This block runs whenever the file uploader widget has a file object
if uploaded_file is not None:
    # Check if this is a different file than the one stored (optional but good practice)
    # For simplicity, we'll just update if the uploader has a file.
    new_file_bytes = uploaded_file.getvalue()
    new_file_name = uploaded_file.name

    # If the uploaded file is different from what's stored, update state
    # and reset previous processing results.
    if new_file_bytes != st.session_state.get('uploaded_file_bytes'):
        st.session_state.uploaded_file_bytes = new_file_bytes
        st.session_state.uploaded_file_name = new_file_name
        st.session_state.dataframe_result = None # Clear old results
        st.session_state.processing_attempted = False # Reset processing flag
        st.info(f"File '{new_file_name}' loaded. Ready to process.")
        # We don't process here, just load and wait for the button

# --- Processing Controls and Button (Only if a file is loaded in state) ---
if st.session_state.uploaded_file_bytes is not None:

    st.write("---")
    st.markdown(f"**File ready:** `{st.session_state.uploaded_file_name}`")

    # --- Configuration Options ---
    use_header_checkbox = st.checkbox(
        "2. Use first row as header",
        value=True, # Default to checked each time UI is drawn before processing
        key='header_checkbox'
    )
    st.write("---") # Separator

    # --- Process Button ---
    if st.button("3. Process File!"):
        st.session_state.processing_attempted = True # Mark that we tried processing
        with st.spinner("Processing table..."): # Show a spinner during processing
            df_result = extract_last_table_as_df(
                st.session_state.uploaded_file_bytes,
                use_first_row_as_header=use_header_checkbox # Use current checkbox value
            )
        st.session_state.dataframe_result = df_result # Store result (DataFrame or None)
        # No rerun needed here, the display section below will update naturally

    # --- Display Area (Only show results *after* processing attempt) ---
    if st.session_state.processing_attempted:
        st.write("---")
        st.write("### Processing Result:")
        result_df = st.session_state.dataframe_result

        if result_df is not None:
            if not result_df.empty:
                st.dataframe(result_df)
            else:
                st.warning("Processing successful, but the extracted table is empty.")
        else:
            # This means extract_last_table_as_df returned None (error or no table)
            st.error("Could not extract a valid table. Check if the document contains tables.")

else:
    # Initial state before any upload
    st.info("👆 Upload a DOCX file to begin.")