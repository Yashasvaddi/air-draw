import streamlit as st
from subprocess import call
from PIL import Image

# Custom CSS for background color and button hover effect
background_color = """
    <style>
    body {
        background-color: #f0f0f0;  /* Change to your desired color */
    }
    .stButton button {
        display: block;
        margin: 0 auto;
        background-color: #4CAF50;  /* Button background color */
        color: white;  /* Initial text color */
        border-radius: 8px;
        border: 2px solid #FFFFFF; /* Initial border color */
        padding: 20px 40px;  /* Adjust padding for better button size */
        font-size: 36px;  /* Adjusted for better readability */
        transition: color 0.3s ease, border-color 0.3s ease; /* Smooth transition for text and border color */
    }
    .stButton button:hover {
        color: #00FFFF; /* Cyan text color on hover */
        border-color: #00FFFF; /* Cyan outline on hover */
    }
    </style>
"""

# Apply the custom CSS
st.markdown(background_color, unsafe_allow_html=True)

# Title of the app with cyan outline
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; font-size: 150px;
    text-shadow: -2px -2px 0 #FFFFFF, 2px -2px 0 #00FFFF, -2px 2px 0 #00FFFF, 2px 2px 0 #00FFFF;'>
    AIR DRAW</h1>
    """, unsafe_allow_html=True)

# Load and display the logo
try:
    image = Image.open("C:\\Users\\YASHAS\\Pictures\\[removal.ai]_798fcf3a-6273-4e9e-8729-aec432569a21-dark-blue-modern-professional-technology-company-logo-2 (1) (1).png")
    st.image(image, use_column_width=True)
except FileNotFoundError:
    st.error("Image not found. Please check the file path.")

# App description
st.markdown("<h3 style='text-align: center;'>Draw in the air using your hands and see your artwork on screen!</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>This app uses computer vision to track your hand movements and allows you to draw on a virtual canvas.</p>", unsafe_allow_html=True)

# Create two columns for buttons
col1, col2 = st.columns(2)

# Button to launch AirDraw
with col1:
    if st.button("Open AirDraw"):
        try:
            st.write("Launching AirDraw... ")
            call(["python", "air-draw/cv.py"])
        except Exception as e:
            st.error(f"An error occurred while launching AirDraw: {e}")

# Additional button to process the image
with col2:
    if st.button("Process the Image"):
        try:
            st.write("Processing the image... ")
            call(["python", "C:\\codes\\college stuff\\ss.py"])
        except Exception as e:
            st.error(f"An error occurred while processing the image: {e}")

# Footer
st.markdown("<p style='text-align: center; color: grey;'>Project by Yashas Vaddi</p>", unsafe_allow_html=True)
