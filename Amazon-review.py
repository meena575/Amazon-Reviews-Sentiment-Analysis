import streamlit as st
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

# Define the scope for Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Function to get Google Sheets service
@st.cache_resource
def get_google_sheet_service():
    flow = InstalledAppFlow.from_client_secrets_file("key.json", SCOPES)
    cred = flow.run_local_server(port=0)
    return build("sheets", "v4", credentials=cred).spreadsheets().values()

# Function to fetch data from Google Sheets
def get_sheet_data(service, spreadsheet_id, range_name, retries=3):
    for attempt in range(retries):
        try:
            result = service.get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            return result.get('values', [])
        except socket.gaierror as e:
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                st.error(f"Network error: {e}")
                return []

# Function to perform sentiment analysis on reviews
def perform_sentiment_analysis(df):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    for review in df["Reviews"]:
        sentiment_score = analyzer.polarity_scores(review)['compound']
        if sentiment_score > 0.5:
            sentiments.append("Positive😃")
        elif sentiment_score < -0.5:
            sentiments.append("Negative😠")
        else:
            sentiments.append("Neutral😐")
    df['Sentiments'] = sentiments
    return df

# Function to update Google Sheets with the new data
def update_google_sheet(service, spreadsheet_id, data):
    body = {"values": data}
    service.update(
        spreadsheetId=spreadsheet_id,
        range="A:E",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

# Streamlit app
def main():
    st.title("Amazon Review Sentiment Analysis")  # Title of the app

    # Display an image
    image = "https://www.revuze.it/blog/wp-content/uploads/sites/2/2020/03/Amazon-Review-Analysis.png"
    st.markdown(
        f'<div style="text-align:center;">'
        f'<img src="{image}" style="width:500px">'
        '</div>',
        unsafe_allow_html=True
    )

    # Custom CSS for button and text input
    st.markdown(
    """
    <style>
    .stButton button {
        background-color: #00CCCC;
        color: black;
    }
    .stTextInput input {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    
    # Input fields for Google Sheets ID and range
    spreadsheet_id = st.text_input("Enter Google Sheets ID", "1629g6F4qSzTs2-MLm9TjbbKPnclK58BGw-hC-ybhJhs")
    range_name = st.text_input("Enter Range Name", "A:D")

    if st.button("Analyze Sentiments"):
        st.write("Fetching data from Google Sheets...")

        # Fetch data from Google Sheets
        service = get_google_sheet_service()
        data = get_sheet_data(service, spreadsheet_id, range_name)

        if not data:
            st.write("No data found.")
            return

        # Convert data to DataFrame and perform sentiment analysis
        df = pd.DataFrame(data[1:], columns=data[0])
        df = perform_sentiment_analysis(df)
        updated_data = [df.columns.tolist()] + df.values.tolist()

        # Update Google Sheets with the new data
        update_google_sheet(service, spreadsheet_id, updated_data)
        st.write("Updated DataFrame:")

        # Function to apply background color based on sentiment values
        def apply_sentiment_color(val):
            if val == 'Positive😃':
                return 'background-color: yellow; color: black'
            elif val == 'Negative😠':
                return 'background-color: red; color: white'
            else:
                return 'background-color: white; color: black'

        # Apply styling to DataFrame
        styled_df = df.style.applymap(apply_sentiment_color, subset=['Sentiments'])

        # Apply header styling
        header_style = {
            'selector': 'th',
            'props': [('background-color', 'blue'), ('color', 'white')]
        }

        # Display styled DataFrame
        st.write(styled_df.set_table_styles([header_style]), unsafe_allow_html=True)

        # Display sentiment analysis results
        st.title("Sentiment Analysis Results:")

        # Create a bar chart for sentiment counts
        sentiment_counts = df['Sentiments'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        col1, col2 = st.columns(2)
        with col1:
            bar_chart = alt.Chart(sentiment_counts).mark_bar().encode(
                x='Sentiment',
                y='Count',
                color='Sentiment'
            ).properties(
                width=300,
                height=300,
                title="Sentiment Count Bar Chart"
            )
            st.altair_chart(bar_chart)

        with col2:
            st.subheader("Pie Chart")
            counts = df['Sentiments'].value_counts()
            fig_pie = px.pie(values=counts, names=counts.index)
            fig_pie.update_layout(
                width=300,
                height=300
            )
            st.plotly_chart(fig_pie)

        # Display a word cloud of the reviews
        st.subheader("Word Cloud of Reviews:")
        text = " ".join(review for review in df['Reviews'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

if __name__ == "__main__":
    main()
