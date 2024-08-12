import pandas as pd
from bs4 import BeautifulSoup as bs
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Function to extract data from a single HTML file
def extract_data_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = bs(content, 'html.parser')
    
    # Extract data
    cust_name = []
    ratings = []
    reviews = []
    review_body = []
    
    # Find customer names
    for span in soup.find_all('span', class_='a-profile-name'):
        try:
            cust_name.append(span.get_text())
        except:
            cust_name.append("")
    
    # Find ratings and extract numeric part
    for span in soup.find_all('span', class_='a-icon-alt'):
        try:
            rating_text = span.get_text()
            rating = re.search(r'(\d+\.\d+)', rating_text).group(1)
            ratings.append(rating)
        except:
            ratings.append("")
    
    # Find review titles
    for a in soup.find_all('a', class_='review-title-content'):
        try:
            span = a.find('span', class_='a-letter-space')
            if span:
                reviews.append(span.find_next_sibling('span').get_text())
            else:
                reviews.append("")
        except:
            reviews.append("")
    
    # Find review bodies
    for span in soup.find_all('span', {"data-hook": "review-body"}):
        try:
            review_body.append(span.get_text().strip())
        except:
            review_body.append("")
    
    # Ensure all lists have the same length
    min_length = min(len(cust_name), len(ratings), len(reviews), len(review_body))
    cust_name = cust_name[:min_length]
    ratings = ratings[:min_length]
    reviews = reviews[:min_length]
    review_body = review_body[:min_length]
    
    # Create DataFrame
    df = pd.DataFrame({
        'Customer Name': cust_name,
        'Ratings': ratings,
        'Reviews': reviews,
        'Review Body': review_body
    })
    
    # Drop duplicate customer names
    df.drop_duplicates(subset=['Customer Name'], inplace=True)
    
    return df

# List of HTML file paths
html_files = [ 'Amazon1.html','Amazon2.html','Amazon3.html','Amazon4.html','Amazon5.html','Amazon6.html','Amazon7.html','Amazon8.html','Amazon9.html','Amazon10.html']  # Add more file paths as needed

# Initialize an empty list to hold all dataframes
data_frames = []

# Process each HTML file and append the data to the list
for file_path in html_files:
    df = extract_data_from_html(file_path)
    data_frames.append(df)

# Concatenate all dataframes
all_data = pd.concat(data_frames, ignore_index=True)

# Convert DataFrame to a list of lists
data = all_data.values.tolist()

# Add column headers to data
#headers = ["Customer Name", "Ratings", "Reviews", "Review Body"]
#data.insert(0, headers)

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

flow = InstalledAppFlow.from_client_secrets_file("key1.json", SCOPES)
cred = flow.run_local_server(port=0)
service = build('sheets', 'v4', credentials=cred)

# Update the spreadsheet with the data
spreadsheet_id = "1629g6F4qSzTs2-MLm9TjbbKPnclK58BGw-hC-ybhJhs"
range_name = 'Sheet1'  # Specify the sheet name

body = {
    "values": data
}

response = service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range=range_name,
    valueInputOption="USER_ENTERED",
    insertDataOption="INSERT_ROWS",
    body=body
).execute()

print(response)
