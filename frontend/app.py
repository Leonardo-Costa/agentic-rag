import streamlit as st
import requests

# Backend API URL (use host.docker.internal for Docker networking)
API_URL = "http://host.docker.internal:8001"

st.title("Agentic RAG Frontend")

st.header("Upload Documents")
uploaded_file = st.file_uploader("Choose a file to upload", type=None)
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    with st.spinner("Uploading..."):
        try:
            response = requests.post(f"{API_URL}/documents", files=files)
            if response.status_code == 200:
                data = response.json()
                st.success("File uploaded successfully!")
                st.subheader("Upload Response")
                st.json(data)
            else:
                st.error(f"Upload failed: [{response.status_code}] {response.text}")
        except Exception as e:
            st.error(f"Error uploading document: {e}")

st.header("Ask a Question")
question = st.text_input("Enter your question:")
if st.button("Query") and question:
    with st.spinner("Querying..."):
        try:
            response = requests.post(f"{API_URL}/question", json={"question": question})
            if response.status_code == 200:
                data = response.json()
                st.subheader("Query Response")
                st.json(data)
                st.subheader("Answer")
                st.markdown(f"> {data.get('answer', '')}")
                st.subheader("Source Chunks")
                for chunk in data.get("chunks", []):
                    title = f"{chunk.get('file_name', '')} - Page {chunk.get('page_number', '')}"
                    with st.expander(title):
                        st.write(chunk.get("content", ""))
            else:
                st.error(f"Query failed: [{response.status_code}] {response.text}")
        except Exception as e:
            st.error(f"Error querying: {e}")