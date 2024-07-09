import streamlit as st
import plotly.graph_objs as go
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

        # Time domain plot
        st.subheader('Time Domain Data')
        fig_time = go.Figure()
        fig_time.add_trace(go.Scatter(x=results['time'], y=results['vibration'], mode='lines', name='Raw Data', line=dict(color='blue')))
        fig_time.add_trace(go.Scatter(x=results['time'], y=results['filtered_vibration'], mode='lines', name='Filtered Data', line=dict(color='red')))
        fig_time.update_layout(title='Time Domain Data', xaxis_title='Time (s)', yaxis_title='Vibration')
        st.plotly_chart(fig_time)

        # Frequency domain plot
        st.subheader('Frequency Domain Data')
        fig_freq = go.Figure()
        fig_freq.add_trace(go.Scatter(x=results['raw_frequencies'], y=results['raw_magnitude'], mode='lines', name='Raw Data', line=dict(color='blue')))
        fig_freq.add_trace(go.Scatter(x=results['filtered_frequencies'], y=results['filtered_magnitude'], mode='lines', name='Filtered Data', line=dict(color='red')))
        fig_freq.update_layout(title='Frequency Domain Data', xaxis_title='Frequency (Hz)', yaxis_title='Magnitude')
        st.plotly_chart(fig_freq)
