import requests
from bs4 import BeautifulSoup
import pandas as pd

def merge_and_save_data():
    # Scrape data from all sources
    racing_post_data = scrape_racing_post()
    at_the_races_data = scrape_at_the_races()
    sporting_life_data = scrape_sporting_life()

    # Debug: Print the column names
    print("Racing Post Data Columns:", racing_post_data.columns)
    print("At The Races Data Columns:", at_the_races_data.columns)
    print("Sporting Life Data Columns:", sporting_life_data.columns)

    # Rename columns to ensure consistency
    racing_post_data.rename(columns={"name": "Horse Name"}, inplace=True)
    at_the_races_data.rename(columns={"horse_name": "Horse Name"}, inplace=True)
    sporting_life_data.rename(columns={"name": "Horse Name"}, inplace=True)

    # Check for empty DataFrames
    if racing_post_data.empty:
        print("Racing Post data is empty.")
    if at_the_races_data.empty:
        print("At The Races data is empty.")
    if sporting_life_data.empty:
        print("Sporting Life data is empty.")

    # Merge only non-empty DataFrames
    dataframes = [racing_post_data, at_the_races_data, sporting_life_data]
    valid_dataframes = [df for df in dataframes if not df.empty]

    if len(valid_dataframes) > 1:
        merged_data = pd.concat(valid_dataframes, join="outer", ignore_index=True)
        merged_data.to_csv("UK_Horses_Data.csv", index=False)
        print("Data saved to UK_Horses_Data.csv")
    else:
        print("Not enough data to create a meaningful dataset.")


# Function to scrape Racing Post
def scrape_racing_post():
    url = "https://www.racingpost.com/racecards"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())  # View the HTML structure of the page


    horses = []
    for card in soup.find_all('div', class_='rc-card__horse-name'):
        horse_name = card.text.strip()
        trainer = card.find_next_sibling('div', class_='rc-card__trainer-name').text.strip()
        odds = card.find_next('span', class_='rc-card__odds').text.strip()
        horses.append({"Horse Name": horse_name, "Trainer": trainer, "Odds": odds})
    return pd.DataFrame(horses)

# Function to scrape At The Races
def scrape_at_the_races():
    url = "https://www.attheraces.com/racecards"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())  # View the HTML structure of the page


    horses = []
    for card in soup.find_all('div', class_='atr-horse-name'):
        horse_name = card.text.strip()
        jockey = card.find_next_sibling('div', class_='atr-jockey-name').text.strip()
        track_condition = card.find_next('span', class_='atr-track-condition').text.strip()
        horses.append({"Horse Name": horse_name, "Jockey": jockey, "Track Condition": track_condition})
    return pd.DataFrame(horses)

# Function to scrape Sporting Life
def scrape_sporting_life():
    url = "https://www.sportinglife.com/racing/racecards"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())  # View the HTML structure of the page


    horses = []
    for card in soup.find_all('div', class_='sl-horse-name'):
        horse_name = card.text.strip()
        recent_finish = card.find_next_sibling('div', class_='sl-recent-form').text.strip()
        horses.append({"Horse Name": horse_name, "Recent Finish": recent_finish})
    return pd.DataFrame(horses)

# Function to merge and save data
def merge_and_save_data():
    racing_post_data = scrape_racing_post()
    at_the_races_data = scrape_at_the_races()
    sporting_life_data = scrape_sporting_life()

    merged_data = pd.merge(racing_post_data, at_the_races_data, on="Horse Name", how="outer")
    merged_data = pd.merge(merged_data, sporting_life_data, on="Horse Name", how="outer")

    merged_data.to_csv("UK_Horses_Data.csv", index=False)
    print("Data saved to UK_Horses_Data.csv")

# Run the scraper
merge_and_save_data()
