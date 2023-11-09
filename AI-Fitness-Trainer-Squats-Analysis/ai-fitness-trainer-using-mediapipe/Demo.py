import streamlit as st


st.title('AI PATO Trainer: Analisis de sentadilla')


recorded_file = 'output_sample.mp4'
sample_vid = st.empty()
sample_vid.video(recorded_file)
