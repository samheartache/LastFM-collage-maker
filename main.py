import base64
import os
import time
from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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
        
        chrome_options.page_load_strategy = 'eager'

        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('--disable-features=NetworkService')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')

        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def authorize(self):
        self.driver.set_page_load_timeout(5)
        
        try:
            self.driver.get('https://www.last.fm/')
        except:
            print("Page load timeout reached, continuing anyway...")
        
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'site-auth-control')))
            login_button.click()
        except Exception as e:
            print(f"Error clicking login button: {e}")
            login_button = self.driver.execute_script(
                "return document.querySelector('.site-auth-control');")
            if login_button:
                login_button.click()
        
        try:
            login_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username_or_email"]')))
            
            self.driver.execute_script("""
                document.querySelector('input[name="username_or_email"]').value = arguments[0];
                document.querySelector('input[name="password"]').value = arguments[1];
                document.querySelector('button[name="submit"]').click();
            """, self.username, self.password)
        except Exception as e:
            print(f"Error during authorization: {e}")
            login_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="username_or_email"]')
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[name="submit"]')
            
            login_input.send_keys(self.username)
            password_input.send_keys(self.password)
            submit_button.click()
        
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'header-avatar')))
        except:
            print("Warning: Avatar not found, but continuing anyway...")
        
        self.get_albums()
    
    def get_albums(self):
        self.driver.set_page_load_timeout(300)
        self.driver.implicitly_wait(0)
        
        main_link = f'https://www.last.fm/user/{self.username}/library'
        main_link += '/tracks?date_preset=LAST_7_DAYS&page=' if self.week else '?page='

        for page in range(1, self.num_pages + 1):
            print(f"Handling page {page}")
            
            while True:
                try:
                    self.driver.get(f'{main_link}{page}')
                    
                    start_time = time.time()
                    while True:
                        try:
                            tracks = self.driver.find_elements(By.CSS_SELECTOR, 'td.chartlist-name > a')
                            if tracks:
                                track_links = {a.get_attribute('href') for a in tracks}
                                break
                        except:
                            pass
                        
                        if time.time() - start_time > 60:
                            raise Exception("Слишком долгая загрузка элементов")
                        
                        time.sleep(1)
                    
                    for track_link in track_links:
                        self._process_track_guaranteed(track_link, page)
                    
                    break

                except Exception as e:
                    print(f"Erroron page {page}: {str(e)}")
                    print("Retrying...")
                    time.sleep(2)
                    continue
    
    def _process_track_guaranteed(self, track_link, page):
        try:
            self.driver.get(track_link)
            
            if self._is_album_unavailable():
                self._add_to_not_found(track_link)
                return
            
            artist, album = self._get_album_info()
            
            if artist and album:
                album_info = f'{artist} - {album}'
                self.albums.add(album_info)
                print(f'Handled: {album_info} | Page: {page}')
            else:
                self._add_to_not_found(track_link)
                
        except Exception as e:
            print(f"Error handling {track_link}: {e}")
            self._add_to_not_found(track_link)

    def _is_album_unavailable(self):
        try:
            missing_phrases = [
                "У нас пока нет альбомов для этой композиции",
                "We don't have any albums for this track yet",
                "Показать все альбомы этого исполнителя"
            ]
            
            page_text = self.driver.page_source
            if any(phrase in page_text for phrase in missing_phrases):
                return True
                
            no_album_section = self.driver.find_elements(By.CSS_SELECTOR, '.resource-list--release-list.empty')
            if no_album_section:
                return True
                
            return False
            
        except:
            return False

    def _get_album_info(self):
        try:
            artist = self.driver.find_element(By.CSS_SELECTOR, '.source-album-artist a').text
            album = self.driver.find_element(By.CSS_SELECTOR, '.source-album-name a').text
            return (artist, album)
        except:
            return (None, None)

    def _add_to_not_found(self, track_link):
        try:
            decoded_url = unquote(track_link)
            parts = decoded_url.split('/')
            artist = ' '.join(parts[4].split('+'))
            track_name = ' '.join(parts[-1].split('+'))
            self.not_found_tracks.add(f'{artist} - {track_name}')
            print(f'Track with unknown album: {artist} - {track_name}')
        except:
            print(f'Failed to recognize URL: {track_link}')
            self.not_found_tracks.add(f'Unknown - {track_link}')
    
    def save_results(self):
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
    username = input("Enter Last.fm username: ")
    password = input("Enter Last.fm password: ")
    parser = LastFM(username, password, 5, is_headless=False)
    parser.authorize()
    parser.save_results()
    ALBUMS = [album for album in open('albums.txt', encoding='utf-8')]
    covers_dir = input('Enter directory name where album covers will be saved: ')
    parser.search_images(queries=ALBUMS, covers_dir=covers_dir, delay=2)
    collage_path = input('Enter file name for collage: ')
    make_collage(collage_path=collage_path, images_path=covers_dir)