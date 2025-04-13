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
    st.session_state.dataframe = None
    st.session_state.header_option_used = True # Store the option used to GENERATE the current df

# --- Helper Function for Resetting State ---
def reset_state():
    # Clear file-specific data
    st.session_state.uploaded_file_bytes = None
    st.session_state.uploaded_file_name = None
    st.session_state.dataframe = None
    st.session_state.header_option_used = True
    # Optionally reset the file uploader itself by changing its key if needed,
    # but often clearing the data state is sufficient.
    # If you added a key like 'file_uploader_key', increment it here:
    # if 'file_uploader_key' in st.session_state:
    #    st.session_state.file_uploader_key += 1

# --- Main App Logic ---
st.title("Advanced DOCX Table Extractor 2")

uploaded_file = st.file_uploader(
    "Choose a DOCX file",
    type=["docx"],
    # Removed on_change callback
    # key="file_uploader_key" # Optional: Add key if explicit widget reset is needed
)

# --- Process the file upload IN THE SAME RUN if a file is present ---
if uploaded_file is not None:
    # Check if this is genuinely a NEW file compared to what's in state
    # (This helps prevent reprocessing if the script reruns for other reasons)
    # A simple check is if the current session state has no bytes yet.
    is_new_upload = st.session_state.uploaded_file_bytes is None

    # If it's a new upload, process and store it
    if is_new_upload:
        st.session_state.uploaded_file_bytes = uploaded_file.getvalue()
        st.session_state.uploaded_file_name = uploaded_file.name
        # Always process a new file using the default header setting first
        st.session_state.header_option_used = True
        st.session_state.dataframe = extract_last_table_as_df(
            st.session_state.uploaded_file_bytes,
            use_first_row_as_header=True # Use default setting
        )
        # No st.rerun() here - let the script continue to the display section

# --- Display Area (runs if file bytes exist in session state) ---
if st.session_state.uploaded_file_bytes is not None:
    st.success(f"Working with: {st.session_state.uploaded_file_name}")
    st.write("---")

    # --- UI Controls ---
    # Get the current value of the checkbox from the UI in this run
    use_header_checkbox_current_value = st.checkbox(
        "Use first row as header",
        value=st.session_state.header_option_used, # Set initial value based on last processing run
        key='header_checkbox'
    )

    # Determine if the checkbox setting differs from the setting used for the currently stored dataframe
    show_refresh_button = (use_header_checkbox_current_value != st.session_state.header_option_used)

    if show_refresh_button:
        st.warning("Header option changed. Click Refresh to update the table view.")
        if st.button("Refresh Table View"):
            # Process again using the CURRENT checkbox setting
            new_df = extract_last_table_as_df(
                st.session_state.uploaded_file_bytes,
                use_first_row_as_header=use_header_checkbox_current_value # Use value from checkbox
            )
            # Update session state: store the new dataframe and the option we just used
            st.session_state.dataframe = new_df
            st.session_state.header_option_used = use_header_checkbox_current_value
            # Rerun needed AFTER processing to update the display and hide the refresh button
            st.rerun()

    # --- Display Table ---
    st.write("### Last Table Extracted:")
    if st.session_state.dataframe is not None:
        if not st.session_state.dataframe.empty:
            st.dataframe(st.session_state.dataframe)
        else:
            st.warning("The extracted table appears to be empty.")
    else:
        # This means extraction failed or no table was found
        st.error("Could not extract a valid table from the document.")

    st.write("---")
    # Button to clear everything and upload a new file
    if st.button("Upload New File"):
        reset_state()
        st.rerun() # Rerun to reflect the cleared state

else:
    st.info("👆 Upload a DOCX file to begin.")