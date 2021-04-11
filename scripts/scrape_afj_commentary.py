__author__ = "Feist"
import requests
import re

urlArray = [
    "01_Day1_Pt1.html",
    "02_Day1_Pt2.html",
    "03_Day1_Pt3.html",
    "04_Day1_Pt4.html",
    "05_Day1_Pt5.html",
    "06_Day2_Pt1.html",
    "07_Day2_Pt2.html",
    "08_Day3_Pt1.html",
    "09_Day3_Pt2.html",
    "10_Day4_Pt1.html",
    "11_Day4_Pt2.html",
    "12_Day4_Pt3.html",
    "13_Day5_Pt1.html",
    "14_Day5_Pt2.html",
    "15_Day5_pt3.html",
    "16_Day5_Pt4.html",
    "17_Day5_Pt5.html",
    "18_Day5_Pt6.html",
    "19_Day6_Pt1.html",
    "20_Day6_Pt2.html",
    "21_Day7.html",
    "22_Day8_Pt1.html",
    "23_Day8_Pt2.html",
    "24_Day9_Pt1.html",
    "25_Day9_Pt2.html",
    "26_Day10_Pt1.html",
    "27_Day10_Pt2.html",
    "28_Day11_Pt1.html",
    "29_Day11_Pt2.html",
    "30_Day12.html",
]

# urlArray = ["02_Day1_Pt2.html"]

outputFilePath = "../MISSION_DATA/scraped_data/scraped_commentary_AFJ.csv"
outputFile = open(outputFilePath, "w", encoding="utf-8")
outputFile.write("")
outputFile.close()
outputFile = open(outputFilePath, "a", encoding="utf-8")

for url in urlArray:
    # request = requests.get('https://history.nasa.gov/afj/ap16fj/' + url)
    # pageAscii = request.text.encode('ascii', 'ignore').decode('ascii')
    # lines = pageAscii.split("\r\n")
    data = open("../MISSION_DATA/journals/ap16fj/" + url, "r", encoding="utf-8")
    pageAscii = data.read()
    lines = pageAscii.split("\n")

    timestamp = ""
    commentary = ""
    linecounter = 0

    for line in lines:
        linecounter += 1
        if linecounter == 165:
            print("test area")

        line_match = re.search(r"(\d{3}(:| )\d{2}(:| )\d{2})", line)
        if line_match is not None:
            timestamp = line_match.group(1)

        timestamp_match = re.search(r"<b>-(\d{3}(:| )\d{2})", line)
        if timestamp_match is not None:
            timestamp = "-" + timestamp_match.group(1)[1:] + ":00"

        timestamp_match = re.search(r"<b>-(\d{3}(:| )\d{2}(:| )\d{2})", line)
        if timestamp_match is not None:
            timestamp = "-" + timestamp_match.group(1)[1:]

        timestamp = re.sub(r" ", ":", timestamp)

        line_match = re.search(r"<p class=\"?(ed)\"?>\[(.*)\]", line)
        if line_match is not None:

            if "omm break." not in line_match.group(2):
                commentary = line_match.group(2).strip()
                commentary = re.sub(r"\&nbsp;", " ", commentary)
                commentary = re.sub(r"\.\.\.\.", "...", commentary)
                commentary = re.sub(r"  ", " ", commentary)
                match = re.search(r"http", commentary)
                if match is not None:
                    commentary = re.sub(
                        r'<a href="(.*?)">',
                        r'<a href="\1" target="afj">',
                        commentary,
                    )
                else:
                    commentary = re.sub(
                        r'<a href="(.*?)">',
                        r'<a href="https://history.nasa.gov/afj/ap16fj/\1" target="afj">',
                        commentary,
                    )
                commentary = commentary.strip()
                commentary = commentary.strip('"')
                commentary = commentary.strip()
                dataLine = timestamp + "||afj|" + commentary + "\n"
                print(str(linecounter) + ": " + dataLine)
                outputFile.write(dataLine)
                commentary = ""

    print("************* DONE page:", url)
outputFile.close()
