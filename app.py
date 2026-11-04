import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Page configuration
st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 Book Recommendation System")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Home", "Recommend Books"])


# HOME PAGE
if page == "Home":

    st.header("🔥 Popular Books")

    col1, col2, col3, col4, col5 = st.columns(5)

    for i in range(min(20, len(popular_df))):

        with [col1, col2, col3, col4, col5][i % 5]:

            st.image(popular_df.iloc[i]['Image-URL-M'])

            st.subheader(popular_df.iloc[i]['Book-Title'])

            st.write("Author:", popular_df.iloc[i]['Book-Author'])

            st.write("Votes:", popular_df.iloc[i]['num_ratings'])

            st.write("Rating:", round(popular_df.iloc[i]['avg_rating'], 2))


# RECOMMENDATION PAGE
elif page == "Recommend Books":

    st.header("🔍 Find Similar Books")

    user_input = st.text_input("Enter a Book Name")

    if st.button("Recommend"):

        if user_input in pt.index:

            index = np.where(pt.index == user_input)[0][0]

            similar_items = sorted(
                list(enumerate(similarity_scores[index])),
                key=lambda x: x[1],
                reverse=True
            )[1:5]

            st.subheader("✨ Recommended Books")

            cols = st.columns(4)

            for i, item in enumerate(similar_items):

                with cols[i]:

                    temp_df = books[
                        books['Book-Title'] == pt.index[item[0]]
                    ].drop_duplicates('Book-Title')

                    if not temp_df.empty:

                        st.image(temp_df.iloc[0]['Image-URL-M'])

                        st.write("**" + temp_df.iloc[0]['Book-Title'] + "**")

                        st.write("Author:", temp_df.iloc[0]['Book-Author'])

        else:

            st.error("Book not found! Please enter a valid book name.")
