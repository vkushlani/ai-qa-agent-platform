import streamlit as st


st.title("AI Testing Agent")
#st.write("Welcome to your AI-powered testing assistant.")


# question = st.text_input(
#    "Enter your testing question:"
# )

# if question:
#     st.write("You asked:")
#     st.write(question)

uploaded_file = st.file_uploader(
    "Upload your release notes", 
     type=["txt"]
)

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    st.subheader("Uploaded Content")
    st.write(content)