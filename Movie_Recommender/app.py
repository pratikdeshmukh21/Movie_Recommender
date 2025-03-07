import pickle
import streamlit as st
import requests
from PIL import Image


# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=9baab5cb452eb97da3d511fd2bed1d0e&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""


# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Load movie data and similarity matrix
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.markdown("""
    <style>
        .big-font { font-size:30px !important; text-align: center; font-weight: bold; color: #FF4B4B; }
        .sub-text { font-size:18px; text-align: center; color: #4B6CC1; }
    </style>
""", unsafe_allow_html=True)

movies = pickle.load(open('../MOVIE-RECOMMANDATION/modal/movie_list.pkl', 'rb'))
similarity = pickle.load(open('../MOVIE-RECOMMANDATION/modal/similarity.pkl', 'rb'))

st.markdown('<p class="big-font">🎬 Movie Recommender System 🍿</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Find movies similar to your favorites!</p>', unsafe_allow_html=True)

# Movie selection
dropdown_col, _ = st.columns([3, 1])
with dropdown_col:
    selected_movie = st.selectbox("🎥 Select a movie from the dropdown", movies['title'].values)

# Show recommendations
if st.button('🔍 Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="big-font">Recommended Movies 🎬</p>', unsafe_allow_html=True)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.write(f"**{recommended_movie_names[i]}**")  # Fixing the movie name display
            st.image(recommended_movie_posters[i], width=200)

