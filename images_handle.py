import difflib
import os
import math
import base64
import time

import requests
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pystyle import *

from utils import initialize_driver, remove_similar_strings


def make_collage(collage_path='collage.jpg', collage_size=1200, margin=0, images_path='covers', similar_value=False):
        if (not collage_path.endswith('.jpg')) and (not collage_path.endswith('.png')):
            collage_path += '.jpg'

        images = [os.path.join(images_path, filename) for filename in os.listdir(images_path)]
        if not images:
            print(Colorate.Horizontal(Colors.red_to_white, 'No images to make collage of'))
            return
        
        if similar_value:
            images = remove_similar_strings(images, similar_value)

        images = [Image.open(path) for path in images]

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

        for img in images:
            img = crop_center(img)
            img = img.resize((thumb_size, thumb_size), Image.LANCZOS)
            collage_image.paste(img, (x * thumb_size, y * thumb_size))

            x += 1
            if x >= cols:
                x = 0
                y += 1

        collage_image.save(collage_path)


def search_image(query, covers_dir, delay=3):
        driver = initialize_driver()
        os.makedirs(covers_dir, exist_ok=True)

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
                
                print(Colorate.Horizontal(Colors.green_to_white, f'Downloaded cover for: {query}'))

                if delay:
                    print(f'Pausing for {delay} seconds to avoid bot detection...')
                    time.sleep(delay)

            else:
                print(Colorate.Horizontal(Colors.red_to_white, f'Skipping non-base64 or empty image for {query}'))

        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_white, f'Error processing {query}: {e}'))


def fast_search_images(queries, covers_dir, delay):
    os.makedirs(covers_dir, exist_ok=True)
    for album in queries:
        album_arr = album.split(',')
        title = album_arr[0].strip()

        if len(album_arr) > 1:
            if len(album_arr[1]) > 4:
                image = album_arr[1].strip()
                save_image_path = os.path.join(covers_dir, f'{title}.jpg')

                try:
                    response = requests.get(url=image, stream=True)

                    with open(save_image_path, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    
                    print(Colorate.Horizontal(Colors.green_to_white, f'Downloaded cover for: {title}'))
                except Exception as e:
                    print(Colorate.Horizontal(Colors.red_to_white, f'Error processing {title}: {e}'))
            else:
                search_image(query=title, covers_dir=covers_dir, delay=delay)
        else:
            search_image(query=title, covers_dir=covers_dir, delay=delay)