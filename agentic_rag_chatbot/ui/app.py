import streamlit as st

st.write("✅ App has started!")

try:
    import fitz  # PyMuPDF
    st.write("✅ fitz (PyMuPDF) imported successfully!")
except Exception as e:
    st.exception(e)

try:
    # Your other imports (langchain, faiss, etc.)
    st.write("✅ Other imports starting...")
except Exception as e:
    st.exception(e)
