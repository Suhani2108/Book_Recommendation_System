import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

# Get current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Load Pickle Files
@st.cache_resource
def load_data():

    popular_df = pickle.load(
        open(os.path.join(BASE_DIR, 'popular.pkl'), 'rb')
    )

    pt = pickle.load(
        open(os.path.join(BASE_DIR, 'pt.pkl'), 'rb')
    )

    books = pickle.load(
        open(os.path.join(BASE_DIR, 'books.pkl'), 'rb')
    )

    similarity_scores = pickle.load(
        open(os.path.join(BASE_DIR, 'similarity_scores.pkl'), 'rb')
    )

    return popular_df, pt, books, similarity_scores


try:
    popular_df, pt, books, similarity_scores = load_data()

except Exception as e:
    st.error("Unable to load book data files.")
    st.exception(e)
    st.stop()


# Sidebar Navigation
st.sidebar.title("📚 Book Recommendation")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Recommend Books"]
)


# HOME PAGE
if page == "Home":

    st.title("📚 Book Recommendation System")

    st.header("🔥 Popular Books")

    cols = st.columns(5)

    for i in range(min(20, len(popular_df))):

        with cols[i % 5]:

            st.image(popular_df.iloc[i]['Image-URL-M'])

            st.subheader(popular_df.iloc[i]['Book-Title'])

            st.write(
                "Author:",
                popular_df.iloc[i]['Book-Author']
            )

            st.write(
                "Votes:",
                popular_df.iloc[i]['num_ratings']
            )

            st.write(
                "Rating:",
                round(popular_df.iloc[i]['avg_rating'], 2)
            )


# RECOMMENDATION PAGE
elif page == "Recommend Books":

    st.title("🔍 Recommend Books")

    user_input = st.text_input(
        "Enter your favourite book name:"
    )

    if st.button("Recommend Books"):

        if user_input in pt.index:

            index = np.where(pt.index == user_input)[0][0]

            similar_items = sorted(
                list(enumerate(similarity_scores[index])),
                key=lambda x: x[1],
                reverse=True
            )[1:5]

            st.header("✨ Recommended Books")

            cols = st.columns(4)

            for i, item in enumerate(similar_items):

                with cols[i]:

                    temp_df = books[
                        books['Book-Title'] == pt.index[item[0]]
                    ].drop_duplicates('Book-Title')

                    if not temp_df.empty:

                        st.image(
                            temp_df.iloc[0]['Image-URL-M']
                        )

                        st.subheader(
                            temp_df.iloc[0]['Book-Title']
                        )

                        st.write(
                            "Author:",
                            temp_df.iloc[0]['Book-Author']
                        )

        else:

            st.error(
                "Book not found! Please enter the correct book name."
            )
