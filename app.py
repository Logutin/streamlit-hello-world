import streamlit as st
import docx # Import the library
# Ensure python-docx is installed: pip install python-docx

# Set a title for the app
st.title("Hello World, and simple upload...")

# Write some text
st.write("This Streamlit app is running inside GitHub Codespaces.")

# Add a little fun element
if st.button("Click me for balloons!"):
    st.balloons()

st.write("Upload a .docx file below:")

# Add the file uploader widget
# - label: The text displayed above the uploader
# - type: A list of allowed file extensions
uploaded_file = st.file_uploader("Choose a DOCX file", type=["docx"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # File is uploaded, display information about it
    st.success(f"Successfully uploaded: {uploaded_file.name}") # Use st.success for positive feedback

    st.write("---") # Add a separator line
    st.write("File Details:")
    st.write(f"Name: {uploaded_file.name}")
    st.write(f"Type: {uploaded_file.type}") # The MIME type (e.g., 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    st.write(f"Size: {uploaded_file.size} bytes")

    # Try reading the content of the uploaded docx file
    try:
        # The UploadedFile object returned by st.file_uploader acts like a file!
        # python-docx can read directly from this file-like object.
        document = docx.Document(uploaded_file)

        # Extract some basic information
        num_paragraphs = len(document.paragraphs)
        num_tables = len(document.tables)
        # You could extract more: word count (approx), sections, etc.

        st.write(f"**Number of paragraphs:** {num_paragraphs}")
        st.write(f"**Number of tables:** {num_tables}")

        # Optional: Display the first few paragraphs (be careful with large files)
        # st.write("---")
        # st.write("#### First 3 Paragraphs:")
        # for i, p in enumerate(document.paragraphs[:3]):
        #     if p.text.strip(): # Only show non-empty paragraphs
        #         st.write(f"P{i+1}: {p.text[:200]}...") # Show preview

    except Exception as e:
        st.error(f"Error reading or processing the DOCX file: {e}")
        st.warning("The file might be corrupted or not a valid DOCX format.")

    st.write("---------------------")

    st.info("Note: This file is processed in memory and is not saved permanently.")

else:
    st.info("Please upload a file.")
