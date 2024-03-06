import streamlit as st
import pickle
import pandas as pd
import requests
import os

from dotenv import load_dotenv
load_dotenv()


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, os.getenv('api')))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster


movies_list = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox('Please select a movie of your choice', movies['title'].values)
if st.button('Recommend'):
   recommendations, posters = recommend(selected_movie_name)
   
   col1, col2, col3, col4, col5 = st.columns(5)
   horizontal_headers = []
   horizontal_images = []
   for i in range(5):
       horizontal_headers.append(recommendations[i])
       horizontal_images.append(posters[i])
   with col1:
           st.header(horizontal_headers[0])
           st.image(horizontal_images[0])
   with col2:
           st.header(horizontal_headers[1])
           st.image(horizontal_images[1])
   with col3:
           st.header(horizontal_headers[2])
           st.image(horizontal_images[2])
   with col4:
           st.header(horizontal_headers[3])
           st.image(horizontal_images[3])
   with col5:
           st.header(horizontal_headers[4])
           st.image(horizontal_images[4])