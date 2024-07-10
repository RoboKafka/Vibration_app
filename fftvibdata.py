import numpy as np
from scipy.signal import butter, filtfilt

class VibrationDataProcessor:
    def __init__(self, time, vibration):
        self.time = time
        self.vibration = vibration
        self.sampling_frequency = self.calculate_sampling_frequency()
        self.filtered_vibration = None

    def calculate_sampling_frequency(self):
        time_intervals = np.diff(self.time)
        average_time_interval = np.mean(time_intervals)
        sampling_frequency = 1 / average_time_interval
        return sampling_frequency

    def high_pass_filter(self, data, cutoff_freq):
        nyquist = 0.5 * self.sampling_frequency
        normal_cutoff = cutoff_freq / nyquist
        b, a = butter(4, normal_cutoff, btype='high', analog=False)
        filtered_data = filtfilt(b, a, data)
        return filtered_data

    def low_pass_filter(self, data, cutoff_freq):
        nyquist = 0.5 * self.sampling_frequency
        normal_cutoff = cutoff_freq / nyquist
        b, a = butter(4, normal_cutoff, btype='low', analog=False)
        filtered_data = filtfilt(b, a, data)
        return filtered_data

    def apply_filters(self, high_pass_cutoff, low_pass_cutoff):
        high_passed_vibration = self.high_pass_filter(self.vibration, high_pass_cutoff)
        self.filtered_vibration = self.low_pass_filter(high_passed_vibration, low_pass_cutoff)

    def compute_fft(self, data):
        fft_data = np.fft.fft(data)
        frequencies = np.fft.fftfreq(len(data), d=1/self.sampling_frequency)
        magnitude = np.abs(fft_data) / len(data)  # Normalizing the magnitude
        return frequencies, magnitude

    def process_data(self, high_pass_cutoff, low_pass_cutoff):
        self.apply_filters(high_pass_cutoff, low_pass_cutoff)
        raw_frequencies, raw_magnitude = self.compute_fft(self.vibration)
        filtered_frequencies, filtered_magnitude = self.compute_fft(self.filtered_vibration)
        
        # Prepare mirrored frequencies and magnitudes
        N = len(raw_frequencies)
        half_len = N // 2
        mirrored_frequencies = np.concatenate([raw_frequencies[:half_len], raw_frequencies[1:half_len][::-1]])
        mirrored_filtered_frequencies = np.concatenate([filtered_frequencies[:half_len], filtered_frequencies[1:half_len][::-1]])
        
        mirrored_magnitude = np.concatenate([raw_magnitude[:half_len], raw_magnitude[1:half_len][::-1]])
        mirrored_filtered_magnitude = np.concatenate([filtered_magnitude[:half_len], filtered_magnitude[1:half_len][::-1]])
        
        return {
            'time': self.time,
            'vibration': self.vibration,
            'filtered_vibration': self.filtered_vibration,
            'raw_frequencies': mirrored_frequencies,
            'raw_magnitude': mirrored_magnitude,
            'filtered_frequencies': mirrored_filtered_frequencies,
            'filtered_magnitude': mirrored_filtered_magnitude
        }

    def peak_to_peak_acceleration_per_frequency(self, magnitude):
        return 2 * magnitude  # Since peak-to-peak value in the frequency domain is twice the magnitude
