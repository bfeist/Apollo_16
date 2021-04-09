__author__ = "Feist"
import requests
import re


def cleanseString(str):
    result = re.sub('<a name=".*"></a>', "", str)
    result = re.sub(" +", " ", result).strip()
    return result


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

outputFilePath = "../MISSION_DATA/scraped_data/scraped_utterances_AFJ.csv"
outputFile = open(outputFilePath, "w")
outputFile.write("")
outputFile.close()
outputFile = open(outputFilePath, "a")

for url in urlArray:
    # request = requests.get("https://history.nasa.gov/afj/ap16fj/" + url)
    # pageAscii = request.text.encode("ascii", "ignore").decode("ascii")
    # lines = pageAscii.split("\r")
    data = open("../ap16fj/" + url, "r")
    pageAscii = data.read()
    lines = pageAscii.split("\n")

    timestamp = ""
    utterance = ""
    who = ""
    utterance_type = ""
    linecounter = 0
    new_line_to_write = False
    multiline_start = False
    startLineNum = 0

    for line in lines:
        linecounter += 1
        if linecounter == 1444:
            print("test area")

        line_match = re.search(r"<p class=\"?(tech|ob|pao)\"?>.*", line)
        if line_match is not None:
            multiline_start = True

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

            line_match = re.search(
                r"<p class=\"?(.*?)\"?><b>(<a.*?<\/a>)?-?(\d{3}(:| )\d{2}(:| )?\d{2}?) ?(.*?( \(onboard\))?):? ?<\/b> ?(.*)(<\/p>)",
                line,
            )
            if line_match is not None:
                who = line_match.group(6)
                who = re.sub(r" \(onboard\)", "", who)
                if "Young" in who:
                    who = "CDR"
                elif "Duke" in who:
                    who = "LMP"
                elif "Mattingly" in who:
                    who = "CMP"
                else:
                    capcoms = [
                        "Peterson",
                        "Fullerton",
                        "Irwin",
                        "Haise",
                        "Roosa",
                        "Mitchell",
                        "Hartsfield",
                        "England",
                        "Overmyer",
                    ]
                    if any(x in who for x in capcoms):
                        utterance_type = "C"
                        who = who[0:3]

                utterance = line_match.group(8)
                utterance_type = "T"
                startLineNum = linecounter

            pao_match = re.search(r"<p class=\"?pao\"?>.*?\"?(.*)\"?", line)
            if pao_match is not None:
                who = "PAO"
                utterance = pao_match.group(1)
                utterance_type = "P"
                utterance = re.sub(r"<b>(.*)?Public Affairs Officer:?</b>:?", "", utterance)

            onboard_match = re.search(r"<p class=ob>(.*)</p>", line)
            if onboard_match is not None:
                utterance_type = "O"

            cc_match = re.search(r"<p class=cc>(.*)</p>", line)
            if cc_match is not None:
                utterance_type = "C"

        if multiline_start:
            line_match = re.search(r"(.*)<\/p>", line)
            if line_match is not None:
                if linecounter != startLineNum:
                    utterance = utterance + " " + line_match.group(1)
                new_line_to_write = True
                multiline_start = False
            else:
                if linecounter != startLineNum:
                    utterance = utterance + " " + line

        if new_line_to_write:
            utterance = re.sub(r"\[((L|l)ong )?(P|p)ause.*?\]", "", utterance)
            utterance = re.sub(r"\.\.\.", " - ", utterance)
            utterance = re.sub(r"\[(G|g)arble.?\]", "...", utterance)
            utterance = re.sub(r"\[Apollo\]", "", utterance)
            utterance = re.sub(r"\&nbsp;", " ", utterance)
            utterance = re.sub(r"\.\.\.\.", "...", utterance)
            utterance = re.sub(r"  ", " ", utterance)
            utterance = utterance.strip()
            utterance = utterance.strip('"')
            utterance = utterance.strip()
            print(str(linecounter) + " " + timestamp + "|" + utterance_type + "|" + who.strip() + "|" + utterance)
            outputFile.write(timestamp + "|" + utterance_type + "|" + who.strip() + "|" + utterance.strip() + "\n")
            new_line_to_write = False

            utterance_type = ""
            who = ""
            utterance = ""

    print("************* DONE page:", url)
outputFile.close()
