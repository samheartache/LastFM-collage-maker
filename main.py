import base64
import os
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from images_handle import make_collage


class LastFM:

    def __init__(self, username, password, num_pages, week=False, is_headless=True):
        self.username = username
        self.password = password
        self.num_pages = num_pages
        self.week = week

        self.albums = set()
        self.not_found_tracks = set()
        self.saved_images = []

        self.is_headless = is_headless

        self.driver = self.initialize_driver()

    def initialize_driver(self):
        chrome_options = Options()

        if self.is_headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def authorize(self):
        driver = self.driver
        driver.get('https://www.last.fm/')
        
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'site-auth-control')))
        login_button.click()

        login_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username_or_email"]')))
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[name="submit"]')

        login_input.send_keys(self.username)
        password_input.send_keys(self.password)
        submit_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'header-avatar')))
        
        self.get_albums()
    
    def get_albums(self):
        driver = self.driver
        main_link = f'https://www.last.fm/user/{self.username}/library'

        if self.week:
            main_link += '/tracks?date_preset=LAST_7_DAYS&page='
        else:
            main_link += '?page='

        for page in range(1, self.num_pages + 1):
            driver.get(f'{main_link}{page}')
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//td[@class="chartlist-name"]/a')))
        
            track_links = set([a.get_attribute('href') for a in driver.find_elements(By.XPATH, '//td[@class="chartlist-name"]/a')])

            for track_link in track_links:
                driver.get(track_link)

                artist_elements = driver.find_elements(By.CLASS_NAME, 'source-album-artist')
                album_elements = driver.find_elements(By.CLASS_NAME, 'source-album-name')

                if artist_elements and album_elements:
                    self.albums.add(f'{artist_elements[0].text} - {album_elements[0].text}')
                else:
                    track_artist = ' '.join(track_link.split('/')[4].split('+'))
                    track_name = ' '.join(track_link.split('/')[-1].split('+'))
                    self.not_found_tracks.add(f'{track_artist} - {track_name}')
        
        with open('albums.txt', 'w', encoding='utf-8') as file:
            for al in self.albums:
                file.write(al + '\n')
        
        with open('songs.txt', 'w', encoding='utf-8') as file:
            for s in self.not_found_tracks:
                file.write(s + '\n')

    
    def search_images(self, queries, covers_dir, delay=3):
        driver = self.driver
        os.makedirs(covers_dir, exist_ok=True)

        for query in queries:
            query = query.strip()
            
            try:
                driver.get('https://images.google.com/')
                
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, 'q')))
                search_input.send_keys(query)
                search_input.send_keys(Keys.RETURN)

                img = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#rcnt img')))
                
                image_url = img.get_attribute('src') or img.get_attribute('data-src')

                if image_url and image_url.startswith('data:image'):
                    header, encoded = image_url.split(',', 1)
                    image_data = base64.b64decode(encoded)

                    safe_image_name = query.replace('/', '_').replace('\\', '_')
                    image_path = os.path.join(covers_dir, f'{safe_image_name}.jpg')

                    with open(image_path, 'wb') as f:
                        f.write(image_data)

                    self.saved_images.append(image_path)
                    print(f'Downloaded cover for: {query}')

                    if delay:
                        print(f"Pausing for {delay} seconds to avoid bot detection...")
                        time.sleep(delay)

                else:
                    print(f'Skipping non-base64 or empty image for {query}')

            except Exception as e:
                print(f'Error processing {query}: {e}')


if __name__ == '__main__':
    username = input()
    password = input()
    parser = LastFM(username, password, 28, is_headless=False)
    parser.authorize()
    ALBUMS = [album for album in open('albums.txt', encoding='utf-8')]
    parser.search_images(queries=ALBUMS, covers_dir='test_images', delay=0)

