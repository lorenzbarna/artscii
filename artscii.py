from pathlib import Path
import cv2
import requests
import numpy as np

default_scale = 0.1
default_console_print = True
default_res_path = False

def convert(image, scale, console_print, res_path):
    
    #image = image[0:10,0:10]


    original_size = image.shape[:2]
    block_size = int(1/scale)
    hsv_img = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    print("org size", original_size)

    result = []

    for h in range(original_size[0]-block_size+1)[::block_size]:

        res_line = []
        
        for l in range(original_size[1]-block_size+1)[::block_size]:
            
            region = image[h:h+block_size, l:l+block_size]

            val = []
            for line in region:
                for pxl in line:
                    val.append(pxl[2])

            brightness = sum(val)/len(val)

            if brightness <= 50:
                res_line.append(".")
            elif brightness <= 100:
                res_line.append("-")
            elif brightness <= 150:
                res_line.append("*")
            elif brightness <= 200:
                res_line.append("O")
            else:
                res_line.append("W")

        result.append("".join(res_line))
        if console_print:
            print("".join(res_line))

    if res_path:
        with open(res_path, "w") as f:
            for line in result:
                f.write(line + "\n")

    


def convert_from_path(img_path: str, scale: float = default_scale, console_print: bool = default_console_print, res_path: str = default_res_path):
    
    p = Path(__file__).parent / img_path
    image = cv2.imread(img_path)
    
    if image is None:
        raise FileNotFoundError(f"Could not read image at {p}")
    
    return convert(image, scale, console_print, res_path)

def convert_from_web(url: str, scale: float = default_scale, console_print: bool = default_console_print, res_path: str = default_res_path):
    
    response = requests.get(url)
    response.raise_for_status()

    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)

    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Could not decode image from URL")
    
    return convert(image, scale, console_print, res_path)




convert_from_path("test1.png", res_path="test.txt") #  scale=0.5)
