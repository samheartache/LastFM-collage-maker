from pprint import pprint
import time
import base64
import math
import os

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image

from test_data import albums
from utils import remove_similar_strings


class LastFM:

    def __init__(self, username, password, quantity):
        self.username = username
        self.password = password
        self.quantity = quantity
        self.saved_images = [os.path.join('covers', filename) for filename in os.listdir('covers')]

        self.driver = self.initialize_driver()

    def initialize_driver(self, is_headless=False):
        chrome_options = Options()
        if is_headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
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
        
        login_button = driver.find_element(By.CLASS_NAME, 'site-auth-control')
        login_button.click()

        time.sleep(5)

        login_input = driver.find_element(By.CSS_SELECTOR, 'input[name="username_or_email"]')
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[name="submit"]')

        login_input.send_keys(self.username)
        password_input.send_keys(self.password)
        submit_button.click()
        time.sleep(5)
        self.get_albums()
    
    def get_albums(self):
        driver = self.driver

        albums = set()
        not_found_tracks = set()

        driver.get(f'https://www.last.fm/user/{self.username}/library/tracks?date_preset=LAST_7_DAYS&page=1')
        time.sleep(20)

        pages = self.get_pagination_links(driver=driver)

        for page in range(len(pages) + 1):
            if page != 0:
                driver.get(pages[page - 1])
                time.sleep(10)
            
            track_links = [a.get_attribute('href') for a in driver.find_elements(By.XPATH, '//td[@class="chartlist-name"]/a')]

            for track_link in track_links:
                driver.get(track_link)

                try:
                    artist = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'source-album-artist'))
                    ).text

                    album_name = driver.find_element(By.CLASS_NAME, 'source-album-name').text
                    albums.add(f'{artist} - {album_name}')
                
                except Exception as e:
                    track_artist = ' '.join(track_link.split('/')[4].split('+'))
                    track_name = ' '.join(track_link.split('/')[-1].split('+'))
                    not_found_tracks.add(f'{track_artist} - {track_name}')
        
        pprint(albums)
        pprint(not_found_tracks)
    
    def get_pagination_links(self, driver):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pagination-list'))
        )

        a_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination-list a')

        links = [a.get_attribute('href') for a in a_elements]

        return links
    
    def get_album_covers(self, albums):
        driver = self.driver
        covers_dir = 'covers'
        os.makedirs(covers_dir, exist_ok=True)
        
        for album in albums:

            driver.get('https://images.google.com/')
            search_input = driver.find_element(By.NAME, 'q')
            search_input.send_keys(album)
            search_input.send_keys(Keys.RETURN)
            time.sleep(5)

            div_s = driver.find_element(By.ID, 'search')
            img = div_s.find_element(By.TAG_NAME, 'img')
            image_url = img.get_attribute('src')

            try:
                header, encoded = image_url.split(',', 1)
                image_data = base64.b64decode(encoded)

                safe_album_name = album.replace('/', '_').replace('\\', '_')
                image_path = os.path.join(covers_dir, f'{safe_album_name}.jpg')
                
                with open(image_path, 'wb') as f:
                    f.write(image_data)

                self.saved_images.append(image_path)
            
            except Exception as e:
                print(f'Error during processing {album}: {e}')
        
        self.make_collage()
    
    def make_collage(self, collage_path='collage.jpg', collage_size=1200, margin=0):
        if not self.saved_images:
            print('No images to make collage of')
            return
        
        print(len(self.saved_images))
        self.saved_images = remove_similar_strings(self.saved_images, 0.7)
        print(len(self.saved_images))

        images = [Image.open(path) for path in self.saved_images]

        num_images = len(images)
        cols = int(math.sqrt(num_images))
        rows = math.ceil(num_images / cols)

        thumb_size = collage_size // max(cols, rows)

        collage_image = Image.new('RGB', (thumb_size * cols, thumb_size * rows), color='white')

        def crop_center(img):
            width, height = img.size
            new_side = min(width, height)
            left = (width - new_side) // 2
            top = (height - new_side) // 2
            right = (width + new_side) // 2
            bottom = (height + new_side) // 2
            return img.crop((left, top, right, bottom))

        x = margin
        y = margin

        for idx, img in enumerate(images):
            img = crop_center(img)
            img = img.resize((thumb_size, thumb_size), Image.LANCZOS)
            collage_image.paste(img, (x * thumb_size, y * thumb_size))

            x += 1
            if x >= cols:
                x = 0
                y += 1

        collage_image.save(collage_path)


if __name__ == '__main__':
    username = 'test'
    password = 'test'
    parser = LastFM(username, password, 3)
    parser.make_collage()

