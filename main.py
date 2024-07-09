import streamlit as st
import matplotlib.pyplot as plt
from fftvibdata import VibrationDataProcessor
import numpy as np

# Streamlit app
st.title('Vibration Data Analysis')

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded file
    data = np.genfromtxt(uploaded_file, delimiter=',', skip_header=1)
    time = data[:, 0]
    vibration = data[:, 1]

    # User inputs for cutoff frequencies
    high_pass_cutoff = st.number_input('Enter the high-pass filter cutoff frequency (Hz)', min_value=0, value=1)
    low_pass_cutoff = st.number_input('Enter the low-pass filter cutoff frequency (Hz)', min_value=0, value=10000)

    if st.button('Process Data'):
        # Initialize the VibrationDataProcessor class
        processor = VibrationDataProcessor(time, vibration)
        
        # Process the data with the provided cutoff frequencies
        results = processor.process_data(high_pass_cutoff, low_pass_cutoff)

        # create 2 columns 
        col1,col2 = st.columns(2)
        with col1:
            # Time domain plots
            st.subheader('Time Domain Data')
            
            fig, ax = plt.subplots()
            ax.plot(results['time'], results['vibration'], label='Raw Data', color='blue')
            ax.plot(results['time'], results['filtered_vibration'], label='Filtered Data', color='red')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Vibration')
            ax.legend()
            st.pyplot(fig)

        with col2:
            # Frequency domain plots
            st.subheader('Frequency Domain Data')
            
            fig, ax = plt.subplots()
            ax.plot(results['raw_frequencies'], results['raw_magnitude'], label='Raw Data', color='blue')
            ax.plot(results['filtered_frequencies'], results['filtered_magnitude'], label='Filtered Data', color='red')
            ax.set_xlabel('Frequency (Hz)')
            ax.set_ylabel('Magnitude')
            ax.legend()
            st.pyplot(fig)
