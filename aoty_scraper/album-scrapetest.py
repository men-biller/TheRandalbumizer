from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
import random
import re

# Set up Selenium WebDriver options
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())

# Open CSV file to store album data
with open("album_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Album Name", "Artist", "Year of Release", "Genre"])

    # Loop through pages 
    for page_num in range(7, 9):
        driver = webdriver.Chrome(service=service, options=options)
        page_url = f"https://www.albumoftheyear.org/ratings/user-highest-rated/all/r-and-b/{page_num}/"
        driver.get(page_url)
        print(f"Saving HTML for page {page_num}: {page_url}")
        
        time.sleep(random.uniform(5, 10))  # Wait to avoid CAPTCHA detection
        
        # Save page source to file
        filename = f"albums{page_num}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        driver.quit()

# Process the saved HTML files
for page_num in range(7, 9):
    filename = f"albums{page_num}.txt"
    with open(filename, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    # Extract album links from saved page
    albums = soup.find_all("a", itemprop="url")
    
    for album in albums:
        album_url = "https://www.albumoftheyear.org" + album.get("href")
        
        # Open album page and extract details
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(album_url)
        print(f"Scraping album page: {album_url}")
        
        time.sleep(random.uniform(1, 5))  # Delay for CAPTCHA avoidance
        
        album_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Album Name
        album_title = album_soup.select_one("h1.albumTitle span[itemprop='name']")
        album_title = album_title.text.strip() if album_title else "Unknown Album"

        # Artist Name
        artist_name = album_soup.select_one("span[itemprop='name'] a")
        artist_name = artist_name.text.strip() if artist_name else "Unknown Artist"

        # Year of Release
        detail_div = album_soup.select_one("div.detailRow")
        if detail_div:
            full_text = detail_div.get_text(separator=" ", strip=True)
            match = re.search(r"\b\d{4}\b", full_text)  # Extract just the year
            album_year = match.group(0) if match else "Unknown Year"
        else:
            album_year = "Unknown Year"

        # Genre(s)
        genre_tags = album_soup.select("div.detailRow a[itemprop='genre']")
        album_genre = ", ".join(tag.get_text(strip=True) for tag in genre_tags) if genre_tags else "Unknown Genre"


        # Write data to CSV
        with open("album_data.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([album_title, artist_name, album_year, album_genre])
            print(f"Scraped: {album_title} by {artist_name} | Year: {album_year}")
        
        driver.quit()
