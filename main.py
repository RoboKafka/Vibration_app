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

        # Compute peak-to-peak acceleration for each frequency component
        p2p_acceleration = processor.peak_to_peak_acceleration_per_frequency(results['raw_magnitude'])

        # Create three columns for side-by-side plots
        col1, col2, col3 = st.columns(3)

        with col1:
            # Time domain plot
            st.subheader('Time Domain Data')
            fig_time, ax_time = plt.subplots()
            ax_time.plot(results['time'], results['vibration'], label='Raw Data', color='blue')
            ax_time.plot(results['time'], results['filtered_vibration'], label='Filtered Data', color='red')
            ax_time.set_xlabel('Time (s)')
            ax_time.set_ylabel('Vibration')
            ax_time.legend()
            st.pyplot(fig_time)

        with col2:
            # Frequency domain plot
            st.subheader('Frequency Domain Data')
            fig_freq, ax_freq = plt.subplots()
            ax_freq.plot(results['raw_frequencies'], results['raw_magnitude'], label='Raw Data', color='blue')
            ax_freq.plot(results['filtered_frequencies'], results['filtered_magnitude'], label='Filtered Data', color='red')
            ax_freq.set_xlabel('Frequency (Hz)')
            ax_freq.set_ylabel('Magnitude')
            ax_freq.legend()
            st.pyplot(fig_freq)
        
        with col3:
            # Peak-to-peak acceleration vs frequency plot
            st.subheader('Peak-to-Peak Acceleration vs Frequency')
            fig_p2p, ax_p2p = plt.subplots()
            ax_p2p.plot(results['raw_frequencies'], p2p_acceleration, label='P2P Acceleration', color='green')
            ax_p2p.set_xlabel('Frequency (Hz)')
            ax_p2p.set_ylabel('Peak-to-Peak Acceleration')
            ax_p2p.legend()
            st.pyplot(fig_p2p)
