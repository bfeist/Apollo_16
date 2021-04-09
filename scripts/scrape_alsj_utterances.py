__author__ = "Feist"
import requests
import re

urlArray = [
    "a16.landing.html",
    "a16.postland.html",
    "a16.window.html",
    "a16.eva1wake.html",
    "a16.eva1prep.html",
    "a16.eva1prelim.html",
    "a16.lrvdep.html",
    "a16.lrvload.html",
    "a16.alsepoff.html",
    "a16.heatflow.html",
    "a16.deepcore.html",
    "a16.thumper.html",
    "a16.geoprep1.html",
    "a16.trvsta1.html",
    "a16.sta1.html",
    "a16.trvsta2.html",
    "a16.sta2.html",
    "a16.trvlm1.html",
    "a16.clsout1.html",
    "a16.eva1post.html",
    "a16.debrief1.html",
    "a16.CMP-site.html",
    "a16.eva2wake.html",
    "a16.eva2prep.html",
    "a16.eva2prelim.html",
    "a16.trvsta4.html",
    "a16.sta4.html",
    "a16.sta5.html",
    "a16.sta6.html",
    "a16.trv6to8.html",
    "a16.sta8.html",
    "a16.trvsta9.html",
    "a16.sta9.html",
    "a16.trvlm2.html",
    "a16.sta10.html",
    "a16.clsout2.html",
    "a16.eva2post.html",
    "a16.eva3wake.html  ",
    "a16.eva3prep.html  ",
    "a16.eva3prelim.html  ",
    "a16.trvsta11.html  ",
    "a16.sta11.html  ",
    "a16.house_rock.html  ",
    "a16.trvsta13.html  ",
    "a16.sta13.html  ",
    "a16.trvlm3.html",
    "a16.sta10prime.html",
    "a16.clsout3.html",
    "a16.vip.html",
    "a16.eva3post.html",
    "a16.launch.html",
]

# urlArray = ["a16.landing.html"]

outputFilePath = "../MISSION_DATA/scraped_data/scraped_utterances_ALSJ.csv"
outputFile = open(outputFilePath, "w", encoding="utf-8")
outputFile.write("")
outputFile.close()
outputFile = open(outputFilePath, "a", encoding="utf-8")

for url in urlArray:
    # request = requests.get("https://www.hq.nasa.gov/office/pao/History/alsj/a11/" + url)
    # pageAscii = request.text.encode("ascii", "ignore").decode("ascii")
    # lines = pageAscii.split("\r\n")
    data = open("../alsj16/" + url, "r", encoding="utf-8")
    pageAscii = data.read()
    lines = pageAscii.split("\n")

    timestamp = ""
    started = False
    writeRecord = False
    gConcatenatedLine = ""
    linecounter = 0
    for line in lines:
        linecounter += 1
        if linecounter == 138:
            print("test area")

        line_match = re.search(r"<b>(\d{3}(:| )\d{2}(:| )\d{2})</b> (.*): (.*)", line)
        if line_match is not None:
            timestamp = line_match.group(1)
            started = True
            utterance_type = "T"

            who = line_match.group(4)
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

            utterance = line_match.group(5)
            line_match = re.search(r"\(On-board\) ", line)
            if line_match is not None:
                utterance_type = "O"
                utterance = re.sub(r"\(On-board\) ", "", utterance)
        else:
            if started:
                if line == "":
                    started = False
                    writeRecord = True
                else:
                    utterance = utterance + " " + line.rstrip()

        if writeRecord:
            writeRecord = False
            utterance = re.sub(r"\[((L|l)ong )?(P|p)ause.*?\]", "", utterance)
            utterance = re.sub(r"\.\.\.", " - ", utterance)
            utterance = re.sub(r"\[(G|g)arble.?\]", "...", utterance)
            utterance = re.sub(r"\((G|g)arble.?\)", "...", utterance)
            utterance = re.sub(r"\[Apollo\]", "", utterance)
            utterance = re.sub(r"\&nbsp;", " ", utterance)
            utterance = re.sub(r"\.\.\.\.", "...", utterance)
            utterance = re.sub(r"  ", " ", utterance)
            utterance = utterance.strip()
            utterance = utterance.strip('"')
            utterance = utterance.strip()
            utterance = utterance.removesuffix("<p>")

            print(str(linecounter) + " " + timestamp + "|" + utterance_type + "|" + who.strip() + "|" + utterance)
            outputFile.write(timestamp + "|" + utterance_type + "|" + who.strip() + "|" + utterance.strip() + "\n")
            new_line_to_write = False

    print("************* DONE page:", url)
