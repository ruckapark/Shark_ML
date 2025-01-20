import numpy as np
import pandas as pd
from pathlib import Path
import cv2

class ImageAugmentor:
    def __init__(self, image_path, augment = True):
        #Functions not properly developped for PIL
        #self.image = Image.open(image_path)
        self.image = cv2.imread(image_path)
        self.factors = {'zoom': 1, 'rotate': 1, 'brightness': 1, 'blur': 1, 'flip_hor': 0, 'flip_vert': 0}
        if augment:
            self.init_factors()
            self.augment()

    def init_factors(self):
        "Randomly initialize factors for data augmentation"

        #Set zoom factor between 1 and 1.2
        zoom_factor = np.random.triangular(left=1, mode=1, right=1.2)
        if zoom_factor >= 1.05: #Only zoom in if factor is above 1.05
            self.factors['zoom'] = zoom_factor
        
        #Get rotation factor between 0 and 10 and inverse randomly
        rotate_factor = np.clip(np.random.normal(4, 2.5), 0, 10)
        rotate_cap = self.rotate_max(zoom_factor)
        rotate_factor = min(rotate_factor,rotate_cap)
        rotate_factor = (2*np.random.randint(0,2) - 1) * rotate_factor #random inverse of rotation
        self.factors['rotate'] = rotate_factor

        #Change brightness between -30 and 30
        brightness_factor = np.clip(np.random.normal(0,15),-30,30)
        self.factors['brightness'] = brightness_factor
        
        #Change blur kernel size using triangular distribution
        blur_kernel_factor = int(np.random.triangular(left=0, mode=0, right=50))
        self.factors['blur'] = blur_kernel_factor
        
        flip_hor,flip_vert = np.random.randint(0,2),np.random.randint(0,2)
        self.factors['flip_hor'] = flip_hor
        self.factors['flip_vert'] = flip_vert
    
    def cv_zoom(self, factor: float) -> np.array:
        height,width,depth = self.image.shape
        new_height,new_width = int(height/factor),int(width/factor)
        dy,dx = height - new_height, width - new_width
        crop = self.image[int(dy/2):-int(dy/2), int(dx/2):-int(dx/2),:]
        if height != new_height:
            self.image = cv2.resize(crop, (width,height))

    def cv_rotate(self, factor: int) -> np.array:
        """Rotate an image using C based OpenCV rotation function"""
        #Get image dimensions and center
        (h,w) = self.image.shape[:2]
        center = (w/2,h/2)

        #cap rotation angle at 10deg
        factor = min(factor,10)

        #Compute rotation matrix - scale = 1
        zoom_factor = self.calculate_min_zoom(w,h,abs(factor))
        M = cv2.getRotationMatrix2D(center, factor, zoom_factor)

        rotated_image = cv2.warpAffine(self.image, M, (w,h))

        self.image = rotated_image

    def rotate_max(self,zoom):
        #Get max rotation for a given zoom level according to linear fit
        """
        y =  ax + b 
        y1 = 8 x1 = 1
        y2 = 3 x2 = 1.2
        a = -25
        b = 33
        """
        return -25*zoom + 33
    
    def cv_change_brightness(self, b_value: float):

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
    
    def cv_flip(self,horizontal:int = 1, vertical:int = 1):
        """ Vertical or horizontal axis flips """
        if horizontal and vertical:
            # Flip both horizontally and vertically
            self.image = cv2.flip(self.image, -1)
        elif horizontal:
            # Flip horizontally
            self.image = cv2.flip(self.image, 1)
        elif vertical:
            # Flip vertically
            self.image = cv2.flip(self.image, 0)

    def augment(self):

        self.cv_zoom(self.factors["zoom"])
        self.cv_rotate(self.factors["rotate"])
        self.cv_change_brightness(self.factors["brightness"])
        self.cv_add_blur(kernel_size = (self.factors["blur"],self.factors["blur"]))
        self.cv_flip(self.factors["flip_hor"],self.factors["flip_vert"])
    
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