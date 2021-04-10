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

outputFilePath = "../MISSION_DATA/scraped_data/scraped_commentary_ALSJ.csv"
outputFile = open(outputFilePath, "w", encoding="utf-8")
outputFile.write("")
outputFile.close()
outputFile = open(outputFilePath, "a", encoding="utf-8")

for url in urlArray:
    # request = requests.get("https://www.hq.nasa.gov/alsj/a16/" + url)
    # pageAscii = request.text.encode("ascii", "ignore").decode("ascii")
    # lines = pageAscii.split("\r\n")
    data = open("../alsj16/" + url, "r", encoding="utf-8")
    pageAscii = data.read()
    lines = pageAscii.split("\n")

    timestamp = ""
    started = False
    writeRecord = False
    comment = ""
    linecounter = 0
    for line in lines:
        linecounter += 1
        if linecounter == 40:
            print("test area")

        line_match = re.search(r"<b>(\d{3}(:| )\d{2}(:| )\d{2})</b>", line)
        if line_match is not None:
            timestamp = line_match.group(1)

        line_match = re.search(r".*?\[(.*)", line)
        if line_match is not None:
            comment = line_match.group(1)

            line_match = re.search(r"Comm Break", comment)
            if line_match is None:
                started = True

            commentSplit = comment.split(" - &quot;")
            if started and len(commentSplit) == 2:
                who = commentSplit[0]
                comment = commentSplit[1]
                comment = re.sub(r"\&quot;", "", comment)
            else:
                who = ""

            if started:
                line_match = re.search(r"\]", comment)
                if started and line_match is not None:
                    comment = re.sub(r"\](</i></blockquote>)?", "", comment)
                    writeRecord = True
                    started = False

        else:
            if started:
                if line == "":
                    started = False
                    writeRecord = True
                else:
                    comment = comment + " " + line.rstrip()

        if writeRecord:
            writeRecord = False

            match = re.search(r"http", comment)
            if match is not None:
                comment = re.sub(
                    r'<a href="(.*?)">',
                    r'<a href="\1" target="alsj">',
                    comment,
                )
            else:
                comment = re.sub(
                    r'<a href="(.*?)">',
                    r'<a href="https://www.hq.nasa.gov/alsj/a16/\1" target="alsj">',
                    comment,
                )

            line_match = re.search(r"from the 1972 Technical Debrief", who)
            if line_match is not None:
                who = re.sub(r"from the 1972 Technical Debrief", "", who)
                who = re.sub(r",", "", who)
                who = who.strip()
                credit = "tech"
            else:
                credit = "alsj"

            comment = comment.strip()
            comment = comment.strip('"')
            comment = comment.strip()
            comment = comment.removesuffix("<p>")

            dataLine = timestamp + "|" + who.strip() + "|" + credit + "|" + comment + "\n"
            print(str(linecounter) + ": " + dataLine)
            outputFile.write(dataLine)

    print("************* DONE page:", url)
