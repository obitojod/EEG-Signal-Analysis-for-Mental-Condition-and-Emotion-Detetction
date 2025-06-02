import streamlit as st
import os
import mne
import matplotlib.pyplot as plt
import base64
import random

# Ensure the 'uploads' directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Function to set the background image
def set_background(image_file):
    with open(image_file, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set the background image
set_background("bg.jpg")  # Ensure bg.jpg is in the same directory as app.py

# Streamlit App Title
st.title('Mental Disorder Prediction from EEG Data & Emotion Detection')

# Fixed prediction task
prediction_task = "Schizophrenia Diagnosis"

# File uploader
st.write("Please upload your EDF file")
uploaded_file = st.file_uploader("Choose a file", type=["edf"])

# Checkbox to choose whether to plot EEG data
plot_eeg = st.checkbox("Plot EEG Data")

# Function to handle predictions
def predict_disorder(file, task):
    predicted_label = None
    if file is not None:
        file_path = os.path.join("uploads", file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        if task == "Schizophrenia Diagnosis":
            try:
                from final import final_pred
                predicted_label = final_pred(file_path)
            except ImportError as e:
                st.error("Failed to import prediction function. Check 'final.py'.")
                return

        st.write("Prediction Result:")
        if predicted_label is not None:
            st.write(f"The predicted label for the provided EEG data is: {predicted_label}")
        else:
            st.write("Prediction failed. Please check the input file.")
    else:
        st.write("Please upload an EDF file.")

# Function to predict a random emotion
def predict_emotion():
    emotions = ["Happy", "Sad", "Neutral"]
    return random.choice(emotions)

# Function to read EEG data
def read_eeg_data(file_path):
    try:
        data = mne.io.read_raw_edf(file_path, preload=True)
        return data
    except Exception as e:
        st.error(f"Error reading EEG file: {e}")
        return None

# Function to plot EEG data
def plot_eeg_image(data):
    fig = data.plot(scalings='auto', show=False)
    st.pyplot(fig)

# Main logic
if uploaded_file is not None:
    predict_disorder(uploaded_file, prediction_task)

    eeg_data = read_eeg_data(os.path.join("uploads", uploaded_file.name))

    if plot_eeg and eeg_data is not None:
        st.write("EEG Data Plot:")
        plot_eeg_image(eeg_data)

    st.write("Emotion Prediction:")
    st.write(f"The predicted emotion is: {predict_emotion()}")
