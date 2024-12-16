import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=041da4c77e2037969fdb5270eddddc1b&language=en-US'.format(movie_id)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for movie ID {movie_id}")
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

def recommend(movie):
    index_of_the_movie = movies_data[movies_data['title'] == movie].index[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)[1:6]
    recommended_movies = []
    recommended_posters = []

    for i in sorted_similar_movies:
        movie_id = movies_data.iloc[i[0]].id
        title_from_index = movies_data[movies_data.index == i[0]]['title'].values[0]
        recommended_movies.append(title_from_index)  # Correct indentation
        recommended_posters.append(fetch_poster(movie_id))  # Correct indentation

    return recommended_movies, recommended_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies_data = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('KH Movies Recommendation System')
selected_movie_name = st.selectbox('Let us know your favourite movie !',(movies_data['title'].values))

if st.button('Movies Suggested For You : Click here to view them'):
    names, posters = recommend(selected_movie_name)
    row1_cols = st.columns(5)
    for i, col in enumerate(row1_cols):
        with col:
            st.text(names[i])
            st.image(posters[i], width=150)

