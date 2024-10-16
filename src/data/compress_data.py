# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 10:05:20 2024

Check best compression format to obtain jpeg images of size 224*224 and 384*384 (as in CCT model)

@author: George
"""

import cv2
from pathlib import Path

if __name__ == "__main__":
    
    root_path = Path(__file__).parents[2]
    data_path = root_path / "data/processed/SharkEggs/BlondeRay/dry"
    test_images = [file for file in data_path.iterdir() if file.is_file()][:2]
    
    test_image = test_images[0]
    
    image = cv2.imread(test_image)
    cv2.imshow('egg',image)
    
    #initial test quality - ok for firs training
    imS = cv2.resize(image, (224, 224))
    cv2.imshow("output", imS)