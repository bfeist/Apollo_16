__author__ = "Feist"
import os
from PIL import Image

mission_images = []

inputPath = "E:/lpi_mirror/mapping/browse/"
outputPath = "E:/lpi_mirror/mapping/thumb/"
size = 120, 120

for filename in os.listdir(inputPath):
    if not os.path.isfile(outputPath + "/" + filename):
        print("Saving thumbnail: " + outputPath + "/" + filename)
        im1 = Image.open(inputPath + "/" + filename)
        im1.thumbnail(size)
        im1.save(outputPath + "/" + filename, "JPEG")
    else:
        print("Thumbnail already exists: " + outputPath + "/" + filename)
