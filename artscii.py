from pathlib import Path
import cv2
import requests
import numpy as np
import json

default_palette = """
                {
                "darkmode": false,
                "range_to": 255,
                "palette": [
                    {"letter": "@", "under_val": 15},
                    {"letter": "#", "under_val": 30},
                    {"letter": "8", "under_val": 45},
                    {"letter": "&", "under_val": 60},
                    {"letter": "o", "under_val": 75},
                    {"letter": ":", "under_val": 90},
                    {"letter": "*", "under_val": 105},
                    {"letter": "+", "under_val": 120},
                    {"letter": "=", "under_val": 135},
                    {"letter": "-", "under_val": 150},
                    {"letter": "~", "under_val": 165},
                    {"letter": ".", "under_val": 180},
                    {"letter": "`", "under_val": 210},
                    {"letter": " ", "under_val": 255}
                ]
                }
                """

def convert(image, palette: dict = json.loads(default_palette), scale: float = 0.1, font_ratio: float = 0.45, res_path: str = False, darkmode: bool = False):

    palette_dict = {}
    last_val = 0
    for i in palette["palette"]:
        letter = i["letter"]
        for val in range(last_val, i["under_val"]):
            palette_dict[val] = letter
        last_val = i["under_val"]


    original_size = image.shape[:2]

    hor_block_size = int(1/scale)
    ver_block_size = int(hor_block_size*(1/font_ratio))

    hsv_img = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    result = []

    for l in range(original_size[0]-ver_block_size+1)[::ver_block_size]:

        res_line = []
        
        for p in range(original_size[1]-hor_block_size+1)[::hor_block_size]:
            
            region = hsv_img[l:l+ver_block_size, p:p+hor_block_size]

            val = []
            for line in region:
                for pxl in line:
                    val.append(pxl[2])

            brightness = sum(val)/len(val)

            if (not palette["darkmode"] and darkmode) or (palette["darkmode"] and not darkmode):
                brightness = 255 - brightness

            res_line.append(palette_dict[int(brightness)])

        result.append("".join(res_line))

    if res_path:
        with open(res_path, "w") as f:
            for line in result:
                f.write(line + "\n")

    return result
    


def image_from_path(img_path: str):
                    
    p = Path(__file__).parent / img_path
    image = cv2.imread(img_path)
    
    if image is None:
        raise FileNotFoundError(f"Could not read image at {p}")
    
    return image

def image_from_url(url: str):
    
    response = requests.get(url)
    response.raise_for_status()

    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)

    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Could not decode image from URL")
    
    return image

def print_to_console(result):
    for i in result:
        print(i)

def load_palette(path: str):
    
    p = Path(__file__).parent / path
    
    with open(p, 'r') as f:
        data = json.load(f)

    if data is None:
        raise ImportError(f"Something went wrong importing the palette from {p}")
    
    return data
