__author__ = "Feist"
import csv
import urllib.request
import re
import os
from PIL import Image

mission_images = []

outputDest = "E:/lpi_mirror/panoramic/"

inputFilePath = "..\\MISSION_DATA\\scraped_data\\temp\\a16_panoramic_images.csv"
data = open(inputFilePath, "r", encoding="utf-8")
pageAscii = data.read()
lines = pageAscii.split("\n")

# type = "thumb"
type = "browse"
# type = "print"

for line in lines:
    filename_match = re.search(r"AS16-([A-Z])-(\d\d\d\d)", line)
    if filename_match is not None:
        rollNum = filename_match.group(1)
        imgNum = filename_match.group(2)

        outputPath = outputDest + "/" + type
        if not os.path.isdir(outputPath):
            os.mkdir(outputPath)
        filename = "AS16-" + rollNum + "-" + imgNum + ".png"
        # Mapping:
        # https://wms.lroc.asu.edu/apollo/view?camera=M&image_name=AS16-M-0029
        # http://apollo.sese.asu.edu/data/metric/AS16/png/AS16-M-0029_SML.png
        #
        # Panoramic:
        # https://wms.lroc.asu.edu/apollo/view?camera=P&image_name=AS16-P-4094
        # http://apollo.sese.asu.edu/data/pancam/AS16/png/AS16-P-4094_FULL_SML.png
        imageURL = (
            "http://apollo.sese.asu.edu/data/pancam/AS16/png/" + "AS16-" + rollNum + "-" + imgNum + "_FULL_SML.png"
        )
        if not os.path.isfile(outputPath + "/" + filename.replace("png", "jpg")):
            print("downloading: " + imageURL)
            try:
                urllib.request.urlretrieve(imageURL, outputPath + "/" + filename)
                im1 = Image.open(outputPath + "/" + filename)
                im1.save(outputPath + "/" + filename.replace("png", "jpg"), quality=80)
                os.remove(outputPath + "/" + filename)
            except:
                print("can't download: " + imageURL)

        else:
            print("skipping: " + imageURL)

# for line in lines:
#     filename_match = re.search(r"AS16-(\d\d)-(\d\d\d\d.?)", imageitem[1])
#     if filename_match is not None:
#         rollNum = filename_match.group(1)
#         imgNum = filename_match.group(2)

#         outputPath = outputDest + "/browse/AS16/" + rollNum + "/"
#         if not os.path.isdir(outputDest + "/browse"):
#             os.mkdir(outputDest + "/browse")
#             if not os.path.isdir(outputDest + "/browse/AS16"):
#                 os.mkdir(outputDest + "/browse/AS16")
#         if not os.path.isdir(outputPath):
#             os.mkdir(outputPath)
#         imageURL = "https://www.lpi.usra.edu/resources/apollo/images/browse/AS16/" + rollNum + "/" + imgNum + ".jpg"
#         if not os.path.isfile(outputPath + imgNum + ".jpg"):
#             print("downloading: " + outputPath + imgNum + ".jpg")
#             urllib.request.urlretrieve(imageURL, outputPath + imgNum + ".jpg")
#         else:
#             print("skipping: " + outputPath + imgNum + ".jpg")

# for line in lines:
#     filename_match = re.search(r"AS16-(\d\d)-(\d\d\d\d.?)", imageitem[1])
#     if filename_match is not None:
#         rollNum = filename_match.group(1)
#         imgNum = filename_match.group(2)

#         outputPath = outputDest + "/print/AS16/" + rollNum + "/"
#         if not os.path.isdir(outputDest + "/print"):
#             os.mkdir(outputDest + "/print")
#             if not os.path.isdir(outputDest + "/print/AS16"):
#                 os.mkdir(outputDest + "/print/AS16")
#         if not os.path.isdir(outputPath):
#             os.mkdir(outputPath)
#         imageURL = "https://www.lpi.usra.edu/resources/apollo/images/print/AS16/" + rollNum + "/" + imgNum + ".jpg"
#         if not os.path.isfile(outputPath + imgNum + ".jpg"):
#             print("downloading: " + outputPath + imgNum + ".jpg")
#             urllib.request.urlretrieve(imageURL, outputPath + imgNum + ".jpg")
#         else:
#             print("skipping: " + outputPath + imgNum + ".jpg")
