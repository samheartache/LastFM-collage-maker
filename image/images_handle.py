import os
import math
import base64
import time

import requests
from PIL import Image, ImageChops, ImageDraw, ImageFont
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pystyle import *

from utils.selenium import initialize_driver
from utils.files import make_path_valid
from utils.utils import remove_similar_strings

from settings.settings_data import BASE_SETTINGS

LASTFM_UNKNOWN_PATH = 'image\lastfm_unknown.jpg'


def compare_images(img1_path, img2_path):
    img1 = Image.open(img1_path).convert('L')
    img2 = Image.open(img2_path).convert('L')

    if img1.size > img2.size:
        img1 = img1.resize(size=img2.size)
    elif img1.size < img2.size:
        img2 = img2.resize(size=img1.size)
    
    diff = ImageChops.difference(image1=img1, image2=img2)

    similar_pixels = np.count_nonzero(np.array(diff)==0)
    total_pixels = img1.size[0] * img1.size[1]
    similarity_percent = float((similar_pixels / total_pixels) * 100)

    return similarity_percent


def remove_similar(images_path: str, similarity_percent: int) -> None:
    images = os.listdir(images_path)
    to_remove = []

    for ind, origin_image in enumerate(images):
        origin_image_path = os.path.join(images_path, origin_image)
        for compare_image in images[ind:]:
            compare_image_path = os.path.join(images_path, compare_image)
            if compare_images(img1_path=origin_image_path, img2_path=compare_image_path) > similarity_percent:
                to_remove.append(origin_image_path)
    
    for image_path in to_remove:
        os.remove(path=image_path)


def make_collage(collage_path='collage.jpg', collage_size=1200, margin=0, images_path='covers', similar_value=False, scale=True, numerate=False):
        if (not collage_path.endswith('.jpg')) and (not collage_path.endswith('.png')):
            collage_path += '.jpg'
        default_collage_dir = BASE_SETTINGS['default collage directory']

        if default_collage_dir:
            os.makedirs(default_collage_dir, exist_ok=True)
            collage_path = os.path.join(BASE_SETTINGS['default collage directory'], collage_path)

        images = [os.path.join(images_path, filename) for filename in os.listdir(images_path)]
        
        if not images:
            print(Colorate.Horizontal(Colors.red_to_white, 'No images to make collage of'))
            return
        
        if similar_value:
            images = remove_similar_strings(images, similar_value)

        images = [Image.open(path) for path in images]

        num_images = len(images)
        cols = int(num_images ** 0.5)
        rows = math.ceil(num_images / cols)

        thumb_size = collage_size // max(cols, rows)

        collage_image = Image.new('RGB', (thumb_size * cols + (margin * (cols + 1)), thumb_size * rows + (margin * (rows + 1))), color='white')

        x = margin
        y = margin

        for idx, img in enumerate(images, start=1):
            if scale:
                img = scale_center(img)

            img = img.resize((thumb_size, thumb_size), Image.LANCZOS)


            if numerate:
                font = ImageFont.load_default(size=(thumb_size // 8))
                draw = ImageDraw.Draw(img)
                num_text = str(idx)

                text_box = draw.textbbox((0, 0), num_text, font=font)
                text_box_w = text_box[2] - text_box[0] + 10
                text_box_h = text_box[3] - text_box[1] + 10

                pos = (thumb_size - text_box_w, thumb_size - text_box_h)
                pos_text = (thumb_size - text_box_w + (int(text_box_w * 0.1)), thumb_size - text_box_h - (int(text_box_h * 0.1)))

                draw.rectangle([pos, (pos[0] + text_box_w, pos[1] + text_box_h)], fill=(0, 0, 0))
                draw.text(pos_text, num_text, font=font, fill=(255, 255, 255))
            
            collage_image.paste(img, (x, y))
            x += thumb_size + margin
            if idx % cols == 0:
                x = margin
                y += thumb_size + margin 

        collage_image.save(collage_path)


def scale_center(img):
    width, height = img.size
    new_side = min(width, height)
    left = (width - new_side) // 2
    top = (height - new_side) // 2
    right = (width + new_side) // 2
    bottom = (height + new_side) // 2
    return img.crop((left, top, right, bottom))


def search_image(queries, covers_dir, delay=3):
        driver = initialize_driver()
        os.makedirs(covers_dir, exist_ok=True)

        for query in queries:
            query = query.strip(', \n')
            
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
                    safe_image_name = make_path_valid(safe_image_name)
                    image_path = os.path.join(covers_dir, f'{safe_image_name}.jpg')

                    with open(image_path, 'wb') as f:
                        f.write(image_data)
                    
                    print(Colorate.Horizontal(Colors.green_to_white, f'Downloaded cover for: {query} (selenium)'))

                    if delay:
                        print(f'Pausing for {delay} seconds to avoid bot detection...')
                        time.sleep(delay)

                else:
                    print(Colorate.Horizontal(Colors.red_to_white, f'Skipping non-base64 or empty image for {query}'))

            except Exception as e:
                print(Colorate.Horizontal(Colors.red_to_white, f'Error processing {query}: {e}'))


def fast_search_images(queries, covers_dir, delay, timeout):
    os.makedirs(covers_dir, exist_ok=True)

    queries = sorted(queries, key=lambda x: len(x.split(',')[-1]), reverse=1)
    noimages = []

    for ind, album in enumerate(queries):
        album_arr = album.split(',')
        title = album_arr[0].strip()
        title = make_path_valid(title)

        if len(album_arr) > 1:
            if len(album_arr[-1]) > 4:
                image = album_arr[-1].strip()
                save_image_path = os.path.join(covers_dir, f'{title}.jpg')

                try:
                    response = requests.get(url=image, stream=True, timeout=timeout)

                    with open(save_image_path, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    
                    if compare_images(img1_path=save_image_path, img2_path=LASTFM_UNKNOWN_PATH) > 80:
                        noimages.append(title)
                    
                    print(Colorate.Horizontal(Colors.green_to_white, f'Downloaded cover for: {title} (url)'))
                except Exception as e:
                    print(Colorate.Horizontal(Colors.red_to_white, f'Error processing {title} (url): {e}'))
            else:
                queries += noimages
                search_image(queries=queries[ind:], covers_dir=covers_dir, delay=delay)
                return
        else:
            queries += noimages
            search_image(queries=queries[ind:], covers_dir=covers_dir, delay=delay)
            return