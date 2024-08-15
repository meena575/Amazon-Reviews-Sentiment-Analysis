# Amazon Review Sentiment Analysis Project
## Objective
This project aims to extract Amazon product reviews, perform sentiment analysis, and visualize the results using various tools like Streamlit, Google Sheets API, and natural language processing techniques. The sentiment analysis helps understand customer feedback by categorizing reviews as positive, negative, or neutral.
<img src="https://www.revuze.it/blog/wp-content/uploads/sites/2/2020/03/Amazon-Review-Analysis.png">
## Table of Contents
1. [Objective](#Objective)
2. [Project Structure](#Project-Structure)
3. [Requirements](#Requirements)
4. [Installation](#Installation)
5. [How It Works](#How-It-Works)
6. [Sentiment Analysis](#Sentiment-Analysis)
7. [Data Scraping](#Data-Scraping)
8. [Features](#Features)
9. [Visualizations](#Visualizations)
10. [Usage](#Usage)
11. [Google Sheets API Setup](#Google-Sheets-API-Setup)
12. [Demo](#Demo)

## Project Structure
'''bash
  
    ├── app.py               # Main Streamlit application for sentiment analysis
    ├── webscraping.py       # Script for scraping reviews from HTML files
    ├── key.json             # OAuth credentials for Google Sheets API (Not included in GitHub for security reasons)
    ├── Amazon1.html         # Example HTML files with Amazon reviews
    ├── Amazon2.html         # More HTML files...
    ├── README.md            # This README file
    └── requirements.txt     # Python dependencies
    ```
## Requirements
To run this project, you'll need to install the following Python libraries:

  - streamlit
  - pandas
  - google-auth-oauthlib
  - google-api-python-client
  - vaderSentiment
  - altair
  - wordcloud
  - matplotlib
  - plotly
  - bs4 (BeautifulSoup for web scraping)
  - re
  You can install all dependencies using the requirements.txt file by running:

    ```bash
      pip install -r requirements.txt
    ```
## Installation
  1. **Clone the repository:**

   ```bash
      git clone https://github.com/your-username/amazon-review-sentiment-analysis.git
      cd amazon-review-sentiment-analysis
   ```
  2. **Set up a virtual environment:**

        ```bash
      python -m venv venv
      source venv/bin/activate  # For Windows: venv\Scripts\activate
     ```
  3. **Install dependencies:**

        ```bash
      
      pip install -r requirements.txt
      ```
  4. **Google Sheets API Setup:**
    Follow the instructions in the Google Sheets API Setup section to configure the API.

  5. **Run the Streamlit app:**

        ```bash
    
        streamlit run app.py
        ```
## How It Works
### Sentiment Analysis
   - The app.py script connects to Google Sheets to fetch Amazon review data, analyzes each review's sentiment using the VADER Sentiment Analyzer, and displays the results in a user-friendly interface.
   - The reviews are categorized into three sentiment groups: Positive, Negative, and Neutral.
### Data Scraping
   - The webscraping.py script processes raw HTML files containing Amazon product reviews using BeautifulSoup.
   - It extracts customer names, ratings, reviews, and review body texts, and then uploads the data to Google Sheets.
## Features
  - **Web Scraping:** Extract product reviews from Amazon HTML files.
  - **Sentiment Analysis:** Classify customer reviews as positive, negative, or neutral.
  - **Google Sheets Integration:** Fetch and update data from Google Sheets.
  - **Data Visualization:** Interactive charts (bar charts, pie charts) and word clouds to display sentiment results.
## Visualizations
  - **Bar Chart:** Visualizes the count of each sentiment category.
  - **Pie Chart:** Shows the distribution of sentiments.
  - **Word Cloud:** Generates a word cloud of the most frequently mentioned words in the reviews.
## Usage
  1. Run the webscraping.py script to scrape data from local HTML files and upload it to Google Sheets.

        ```bash
        python webscraping.py
        ```
 2. Run the Streamlit app to analyze and visualize the sentiment of reviews.
    ```bash
    streamlit run app.py
    ```
 3. Enter the Google Sheets ID and the range of data to analyze in the input fields of the app.

## Google Sheets API Setup
  1. Go to the [Google Cloud Console.](https://console.cloud.google.com/welcome?_gl=1*mzdodu*_up*MQ..&gclid=Cj0KCQjwq_G1BhCSARIsACc7NxqLK5RDeAil7dNJsZzvP0a-gbyUcoQ8YWCEqnqEecIEoM6NIiOclpQaAkhiEALw_wcB&gclsrc=aw.ds&hl=en&project=india-415906)
  2. Create a new project and enable the Google Sheets API.
  3. Download your OAuth 2.0 client credentials as a key.json file.
  4. Place the key.json file in your project directory.
  5. In the app.py and webscraping.py scripts, the following line will authenticate and authorize access to Google Sheets:
        ```python
        flow = InstalledAppFlow.from_client_secrets_file("key.json", SCOPES)
        ```
## Demo
A demo of the project is available [here.]()
