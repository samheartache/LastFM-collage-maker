from PIL import Image

import difflib
import os
import math

def remove_similar_strings(strings, threshold=0.85):
    result = []
    for s in strings:
        if not any(difflib.SequenceMatcher(None, s, r).ratio() > threshold for r in result):
            result.append(s)
    return result

def make_collage(collage_path='collage.jpg', collage_size=1200, margin=0, images_path='covers', similar_value=None):
        images = [os.path.join(images_path, filename) for filename in os.listdir(images_path)]
        if not images:
            print('No images to make collage of')
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

        for idx, img in enumerate(images):
            img = crop_center(img)
            img = img.resize((thumb_size, thumb_size), Image.LANCZOS)
            collage_image.paste(img, (x * thumb_size, y * thumb_size))

            x += 1
            if x >= cols:
                x = 0
                y += 1

        collage_image.save(collage_path)