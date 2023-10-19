import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress Matplotlib warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

# Set full-screen mode at the beginning
st.set_page_config(layout="wide")

# Custom CSS for styling (you can customize this further)
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #75B6C4 0%, #002F63 100%);
            color: white;
        }
        .stSelectbox, .stTextInput {
            background-color: #001F4D;
            color: white;
        }
        .stButton {
            background-color: #F39A1F;
            color: white;
            font-weight: bold;
        }
        .stDataFrame, .stTable {
            font-size: 18px;
            color: black;
        }
        .st-checkbox label, .st-radio label {
            font-size: 18px;
            color: white;
        }
        .st-number-input input, .st-text-area textarea {
            font-size: 18px;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit App Title
st.title("CSV File Data Analysis")

# Upload a CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Function to load and preprocess data using st.cache
@st.cache
def load_data(file):
    if file is not None:
        data = pd.read_csv(file)
        return data

if uploaded_file is not None:
    data = load_data(uploaded_file)

    # Display the DataFrame
    st.write("Data Preview:")
    st.write(data)

    # Basic Data Statistics
    st.subheader("Basic Data Statistics:")
    st.dataframe(data.describe(), height=300)

    # Data Visualization
    st.subheader("Data Visualization:")

    # Show Correlation Heatmap
    if st.checkbox("Show Correlation Heatmap"):
        st.write("Correlation Heatmap:")
        corr_matrix = data.corr()
        st.dataframe(corr_matrix, height=300)

        # Calculate figure size proportionally
        fig_width, fig_height = 1,2
        heatmap_fig = plt.figure(figsize=(fig_width, fig_height))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f", square=True, annot_kws={"size": 5})
        st.pyplot(heatmap_fig)

    # Univariate and Bivariate Analysis
    analysis_col1, analysis_col2 = st.columns(2)

    with analysis_col1:
        st.subheader("Univariate Analysis:")
        univariate_column = st.selectbox("Select a column for univariate analysis", data.columns)

        if univariate_column:
            st.subheader(f"Univariate Analysis of {univariate_column}")
            plot_type = st.selectbox("Select a plot type", ["Histogram", "Pie Chart"])

            st.write(f"{plot_type} of {univariate_column}")
            fig_width, fig_height = 8, 6
            univariate_fig = plt.figure(figsize=(fig_width, fig_height))

            if plot_type == "Histogram":
                sns.histplot(data[univariate_column], kde=True, color='#F39A1F')
            elif plot_type == "Pie Chart":
                counts = data[univariate_column].value_counts()
                plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set3"))
            st.pyplot(univariate_fig)

    with analysis_col2:
        st.subheader("Bivariate Analysis:")
        x_variable = st.selectbox("Select the X-axis variable for bivariate analysis", data.columns)
        y_variable = st.selectbox("Select the Y-axis variable for bivariate analysis", data.columns)
        plot_type = st.selectbox("Select a plot type for bivariate analysis", ["Scatter Plot", "Line Plot", "Bar Plot"])

        if x_variable and y_variable:
            st.write(f"{plot_type} of {x_variable} vs {y_variable}")
            fig_width, fig_height = 8, 6
            bivariate_fig = plt.figure(figsize=(fig_width, fig_height))

            if plot_type == "Scatter Plot":
                sns.scatterplot(data=data, x=x_variable, y=y_variable, color='#F39A1F')
            elif plot_type == "Line Plot":
                sns.lineplot(data=data, x=x_variable, y=y_variable, color='#F39A1F')
            elif plot_type == "Bar Plot":
                sns.barplot(data=data, x=x_variable, y=y_variable, color='#F39A1F')

            st.pyplot(bivariate_fig)
