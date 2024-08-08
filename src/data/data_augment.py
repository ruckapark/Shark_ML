import numpy as np
import pandas as pd
from pathlib import Path
import cv2

class ImageAugmentor:
    def __init__(self, image_path):
        #check if this works with Paht object or only with string
        #self.image = Image.open(image_path)
        self.image = cv2.imread(image_path)
    
    def cv_zoom(self, factor: float) -> np.array:
        height,width,depth = self.image.shape
        new_height,new_width = int(height/factor),int(width/factor)
        dy,dx = height - new_height, width - new_width
        crop = self.image[int(dy/2):-int(dy/2), int(dx/2):-int(dx/2),:]
        if height != new_height:
            self.image = cv2.resize(crop, (width,height))
    
    def cv_change_brightness(self, b_value: float) -> Image:

        """Function could also work to shift hue or saturation"""

        #cap brightness change
        value = min(b_value,50)
        value = max(b_value,-50)

        #convert rgb to hue, sat, value
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)

        #add brightness shift and remerge
        v = cv2.add(v, value)
        hsv = cv2.merge((h,s,v))

        #return convert back to rgb
        self.image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    def cv_add_blur(self, kernel_size: tuple = (25,25)):
        if not kernel_size[0]%2:
            kernel_size = (kernel_size[0]+1,kernel_size[1])
        if not kernel_size[1]%2:
            kernel_size = (kernel_size[0],kernel_size[1]+1)
        self.image = cv2.GaussianBlur(self.image, kernel_size, 0)
    
    def save_image(self, output_path: str):
        cv2.imwrite(output_path,self.image)

'''
#define root path
root = Path(__file__).parents[2]

#get test image
img_idx = 1
image = root / f"data/test/dry{img_idx}.png"

#output for data storage
output = root / f"data/augmented/output.png"
    
image = ImageAugmentor(image)
image.cv_zoom(1.2)
image.cv_change_brightness(-30)
image.cv_add_blur(kernel_size = (40,40))
image.save_image(output)
'''