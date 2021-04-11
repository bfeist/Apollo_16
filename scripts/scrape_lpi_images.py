__author__ = "Feist"
import csv
import urllib.request
import re
import os

mission_images = []

outputDest = "E:/lpi_mirror"

inputFilePath = "..\\MISSION_DATA\\scraped_data\\temp\\flickr_listing.txt"
data = open(inputFilePath, "r", encoding="utf-8")
pageAscii = data.read()
lines = pageAscii.split("\n")

# type = "thumb"
type = "browse"
# type = "print"

for line in lines:
    filename_match = re.search(r"AS16-(\d\d\d)-(\d\d\d\d.?)", line)
    if filename_match is not None:
        rollNum = filename_match.group(1)
        imgNum = filename_match.group(2)

        outputPath = outputDest + "/" + type + "/AS16/" + rollNum + "/"
        if not os.path.isdir(outputDest + "/" + type):
            os.mkdir(outputDest + "/" + type)
            if not os.path.isdir(outputDest + "/" + type + "/AS16"):
                os.mkdir(outputDest + "/" + type + "/AS16")
        if not os.path.isdir(outputPath):
            os.mkdir(outputPath)
        imageURL = (
            "https://www.lpi.usra.edu/resources/apollo/images/" + type + "/AS16/" + rollNum + "/" + imgNum + ".jpg"
        )
        if not os.path.isfile(outputPath + imgNum + ".jpg"):
            print("downloading: " + outputPath + imgNum + ".jpg")
            try:
                urllib.request.urlretrieve(imageURL, outputPath + imgNum + ".jpg")
            except:
                print("can't download: " + outputPath + imgNum + ".jpg")

        else:
            print("skipping: " + outputPath + imgNum + ".jpg")

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
