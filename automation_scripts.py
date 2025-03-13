import os
import requests
import csv
import time
from bs4 import BeautifulSoup
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import random

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurations
URL = "https://example.com"
OUTPUT_CSV = "output/data.csv"
CHECK_INTERVAL = 60  # seconds
WATCH_DIRECTORY = "watch_folder"
EMAIL_ADDRESS = "youremail@example.com"
EMAIL_PASSWORD = "yourpassword"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587

# Function to scrape data from a website
def scrape_data(url):
    logger.info(f"Starting to scrape {url}")
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Failed to retrieve data: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    for item in soup.find_all('div', class_='item'):
        title = item.find('h2').text
        link = item.find('a')['href']
        data.append({'title': title, 'link': link})
    logger.info("Scraping completed")
    return data

# Function to save data to a CSV file
def save_to_csv(data, output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'link'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    logger.info(f"Data saved to {output_csv}")

# Class to handle file system events
class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        logger.info(f"New file created: {event.src_path}")
        time.sleep(5)  # Simulate processing delay
        self.send_email_notification(event.src_path)

    def send_email_notification(self, file_path):
        logger.info(f"Sending email notification for file: {file_path}")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f"New file created: {os.path.basename(file_path)}"
        
        body = f"A new file has been created: {file_path}"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info("Email notification sent")

# Main function
def main():
    logger.info("Automation script started")
    while True:
        try:
            data = scrape_data(URL)
            save_to_csv(data, OUTPUT_CSV)
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")

# File monitoring
def monitor_directory():
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIRECTORY, recursive=False)
    observer.start()
    logger.info(f"Monitoring directory: {WATCH_DIRECTORY}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    from threading import Thread
    scraper_thread = Thread(target=main)
    scraper_thread.start()
    monitor_directory()
    scraper_thread.join()