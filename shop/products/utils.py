import os
import secrets
from PIL import Image
from flask import current_app

def add_pictures(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img', picture_name)

    # Open the image
    img = Image.open(picture).convert("RGBA")
    
    # Create a transparent background
    background = Image.new('RGBA', (600, 600), (255, 255, 255, 0))
    
    # Resize the image to fit within 600x600 while maintaining aspect ratio
    img.thumbnail((600, 600), Image.LANCZOS)
    
    # Get the size of the resized image
    img_w, img_h = img.size
    
    # Calculate position to paste the resized image onto the background
    pos_x = (600 - img_w) // 2
    pos_y = (600 - img_h) // 2
    
    # Paste the resized image onto the background
    background.paste(img, (pos_x, pos_y), img)
    
    # Convert to RGB if saving as JPEG
    if f_ext.lower() in ['.jpg', '.jpeg']:
        background = background.convert("RGB")
    
    # Save the final image
    background.save(picture_path)

    return picture_name



def ratings(reviews):
    total=0
    for review in reviews:
        total+=review.rating
    return round(total/reviews.count(), 2) if reviews.count() else 0
