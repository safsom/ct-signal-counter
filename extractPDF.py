from PyPDF2 import PdfReader
import sys
import re
import pandas as pd

sigdictemp = {
        "R": [],
        "F": [],
        "RF": [],
        "PR": [],
        "PF": [],
        "RR": [],
        "Ca": [],
        "Ms": [],
        "Gr": [],
        "Su": [],
        "Eu": [],
        "Eg": [],
        "FA": [],
    }

def genSignals(text):
    signals = sigdictemp
    signalRegex = re.compile("[A-Za-z]+-[0-9]+ [^:]+: [0-9]+")
    matches = signalRegex.findall(text)
    for match in matches:
        signame = str(match)[:str(match).find(' ') - 2]
        signum = int(str(match)[str(match).find(' ') - 1:str(match).find(' ')])
        sigcount = int(re.search(r'\d+', str(match)[str(match).find(' ') + 1:]).group())
        signals[signame].append((signum, sigcount))
    return signals

def genTruncatedSignals(text):
    sigs = genSignals(text)
    signals = sigdictemp
    for s in sigs:
        total = 0
        for sigpair in sigs[s]:
            total += sigpair[1]
        signals[s] = total
    return signals

if len(sys.argv) < 3:
    print("Please specify an output mode (full or trunc), and at least one report filename to generate a spreadsheet for.")
    exit(-1)

reports = []
filenames = sys.argv[2:]
for fn in filenames:
    raw = ''
    reader = PdfReader(fn)
    for n in range(len(reader.pages)):
        page = reader.pages[n]
        raw += page.extract_text()
    pdf_text = re.sub(r"VIDEO URL:[\s]+https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", '', raw)
    if sys.argv[1] == "full":
        reports.append(genSignals(pdf_text))
    elif sys.argv[1] == "trunc":
        reports.append(genTruncatedSignals(pdf_text))
    else:
        print("Please use a valid output mode")
        exit(-1)

out = pd.DataFrame(reports)
out.to_excel("out-" + sys.argv[1] + ".xlsx")