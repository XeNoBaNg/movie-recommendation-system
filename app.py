import streamlit as st 
import bz2
import pickle
import pandas as pd
import requests
import gdown


movie_dict = pickle.load(open('movie_dict', 'rb'))
movies = pd.DataFrame(movie_dict)

with bz2.BZ2File("similarity.pbz2", "rb") as f:
    similarity = pickle.load(f)


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=bcaee6d4def9356901a88e2d6bd7b3e6&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/original/' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommends_movies = []
    movies_poster = []
    
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommends_movies.append(movies.iloc[i[0]].title)
        movies_poster.append(fetch_poster(movie_id))
    
    return recommends_movies, movies_poster

st.title("Movie Recommendation System")

selected_movie = st.selectbox(
    "Movie to Recommend",
    movies['title'].values,
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
        
                
