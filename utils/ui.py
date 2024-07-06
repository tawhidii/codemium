import os
import streamlit as st
from decouple import config
from langchain_community.vectorstores.faiss import FAISS
from core import data_ingestion, setup_vector_store, get_embedding, load_llm, get_response
from streamlit_cognito_auth import CognitoAuthenticator
from helpers import CodebaseToText

pool_id = config("POOL_ID")
app_client_id = config("APP_CLIENT_ID")
app_client_secret = config("APP_CLIENT_SECRET")

authenticator = CognitoAuthenticator(
    pool_id=pool_id,
    app_client_id=app_client_id,
    app_client_secret=app_client_secret,
    use_cookies=False
)


def logout():
    print("Logout in example")
    authenticator.logout()


def codemium_ui():
    st.set_page_config("CodeMium")

    is_logged_in = authenticator.login()

    if not is_logged_in:
        st.stop()

    logo_url = "https://i.imghippo.com/files/1J67j1720265311.png"
    st.markdown(
        f"""
            <div style="display: flex; justify-content: center;">
                <img src="{logo_url}" alt="Logo" style="width: 150px;">
            </div>
            """,
        unsafe_allow_html=True
    )

    user_question = st.text_area("Ask me about your project")

    with st.sidebar:
        st.text(f"Welcome,\n{authenticator.get_email()}")
        st.button("Logout", "logout_btn", on_click=logout)

        st.title("Create Vector Embeddings")
        if st.button("Update Vector DB"):
            with st.spinner("Running ...."):
                docs = data_ingestion()
                setup_vector_store(docs)
                st.success("Vector Embeddings Successful ")

        st.title("Process code to text")
        process_data_input = st.text_input("Enter github url or project folder path:")
        if st.button("Process Data"):
            with st.spinner("Running ...."):
                code_to_text = CodebaseToText(input_path=process_data_input,
                                              exclude_hidden=True,
                                              output_type="txt",
                                              output_path="/Users/hasnat/Desktop/codemium/data/data.txt")
                code_to_text.get_file()
                st.success("Success !")

    if st.button("Generate Response !") or user_question:
        # first check if the vector store exists
        if not os.path.exists("faiss_index"):
            st.error("Please create the vector store first from the sidebar.")
            return
        if not user_question:
            st.error("Please enter a question.")
            return
        with st.spinner("Running ...."):
            faiss_index = FAISS.load_local("faiss_index", embeddings=get_embedding(),
                                           allow_dangerous_deserialization=True)
            llm = load_llm()
            st.write(get_response(llm, faiss_index, user_question))
            st.success("Done")
