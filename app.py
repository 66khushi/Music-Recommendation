import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Load the similarity matrix and Data dataframe
similarity = pickle.load(open('similarity.pkl', 'rb'))
Data = pickle.load(open('Data.pkl', 'rb'))

# Function to get song recommendations
def recommendation(song_name):
    try:
        idx = Data[Data['song'] == song_name].index[0]
        distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
        songs = [Data.iloc[m_id[0]].song for m_id in distances[1:21]]
        return songs
    except IndexError:
        return ["Song not found in dataset"]

# Function to plot recommendations
def plot_recommendations(song_name):
    try:
        idx = Data[Data['song'] == song_name].index[0]
        distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])[1:11]

        recommended_songs = [Data.iloc[m_id[0]].song for m_id in distances]
        similarity_scores = [m_id[1] for m_id in distances]

        plt.figure(figsize=(12, 6))
        plt.barh(recommended_songs, similarity_scores, color='purple')
        plt.xlabel('Similarity Score')
        plt.ylabel('Recommended Songs')
        plt.title(f'Top 10 Recommended Songs for "{song_name}"')
        plt.gca().invert_yaxis()
        plt.show()
    except IndexError:
        st.write("Song not found in dataset")
        return

# Streamlit UI
st.title('Song Recommendation System')

song_list = Data['song'].unique()
selected_song = st.selectbox('Select a song to get recommendations', song_list)

if st.button('Show Recommendations'):
    recommended_songs = recommendation(selected_song)
    st.write('Recommended Songs:')
    for song in recommended_songs:
        st.write(song)

    st.write("Recommendation Plot:")
    plot_recommendations(selected_song)
    st.pyplot(plt)