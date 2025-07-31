import streamlit as st
from processing import process_file
from api import post_to_api

st.title("Tabbycat Data Importer")

uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    institutions_df, judges_df, teams_df = process_file(uploaded_file)

    st.subheader("Institutions")
    st.dataframe(institutions_df)
    st.download_button("Download Institutions", institutions_df.to_csv(index=False), "institutions.csv")

    st.subheader("Judges")
    st.dataframe(judges_df)
    st.download_button("Download Judges", judges_df.to_csv(index=False), "judges.csv")

    st.subheader("Teams")
    st.dataframe(teams_df)
    st.download_button("Download Teams", teams_df.to_csv(index=False), "teams.csv")

    st.divider()
    st.subheader("Post to Tabbycat")

    token = st.text_input("API Token", type="password")
    site = st.text_input("Base Site URL", placeholder="https://tabbycat.example.com/")
    slug = st.text_input("Tournament Slug")

    if st.button("🚀 Submit to API"):
        if not token or not site or not slug:
            st.error("All fields are required.")
        else:
            post_to_api(institutions_df, judges_df, teams_df, token, site, slug)
