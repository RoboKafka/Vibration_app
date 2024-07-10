# Streamlit application for visulizing Vibration data 

## Install the required dependancies
```bash
pip install streamlit
pip install numpy
pip install scipy
pip install matplotlib
pip install plotly
```
## Data format
The program is designed to only take in csv file with the following format. The first row of the file will be considered a header. 

```Python
# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded file
    data = np.genfromtxt(uploaded_file, delimiter=',', skip_header=1)
    time = data[:, 0]
    vibration = data[:, 1]
```
## Example
Use the csv file provided in the data folder as an example. 
![Streamlit Interface](images/streamlit_interface.png)
![Streamlit Dashboard](images/streamlit_dashboard.png)


