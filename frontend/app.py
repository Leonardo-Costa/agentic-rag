import streamlit as st
import requests

# Backend API URL (use service-name for Docker Compose networking)
API_URL = "http://api:8001"

st.title("Agentic RAG Frontend")

st.header("Upload Documents")
uploaded_file = st.file_uploader("Choose a file to upload", type=None)
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    with st.spinner("Uploading..."):
        try:
            response = requests.post(f"{API_URL}/documents", files=files)
            if response.status_code == 200:
                st.success("File uploaded successfully!")
            else:
                st.error(f"Upload failed: [{response.status_code}] {response.text}")
        except Exception as e:
            st.error(f"Error uploading document: {e}")

st.header("Ask a Question")
question = st.text_input("Enter your question:")
if st.button("Query") and question:
    with st.spinner("Querying..."):
        try:
            response = requests.post(f"{API_URL}/query", json={"question": question})
            if response.status_code == 200:
                st.write(response.json())
            else:
                st.error(f"Query failed: [{response.status_code}] {response.text}")
        except Exception as e:
            st.error(f"Error querying: {e}")