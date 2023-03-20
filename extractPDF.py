from PyPDF2 import PdfReader
import sys
import re
import pandas as pd

def genSignals(text):
    signals = {
        "R-1": 0,
        "R-2": 0,
        "R-3": 0,
        "R-4": 0,
        "R-5": 0,
        "F-1": 0,
        "F-2": 0,
        "F-3": 0,
        "F-4": 0,
        "F-5": 0,
        "PR-1": 0,
        "PR-2": 0,
        "PR-3": 0,
        "PR-4": 0,
        "PR-5": 0,
        "RR-1": 0,
        "RR-2": 0,
        "RR-3": 0,
        "RR-4": 0,
        "RR-5": 0,
        "PF-1": 0,
        "PF-2": 0,
        "PF-3": 0,
        "PF-4": 0,
        "PF-5": 0,
        "RF-1": 0,
        "RF-2": 0,
        "RF-3": 0,
        "RF-4": 0,
        "RF-5": 0,
        "Ca-1": 0,
        "Ca-2": 0,
        "Ca-3": 0,
        "Ca-4": 0,
        "Ca-5": 0,
        "Ca-6": 0,
        "Ca-7": 0,
        "Ca-8": 0,
        "Ca-9": 0,
        "Ms-1": 0,
        "Ms-2": 0,
        "Ms-3": 0,
        "Ms-4": 0,
        "Ms-5": 0,
        "Ms-6": 0,
        "Ms-7": 0,
        "Ms-8": 0,
        "Ms-9": 0,
        "Gr-1": 0,
        "Gr-2": 0,
        "Gr-3": 0,
        "Gr-4": 0,
        "Gr-5": 0,
        "Gr-6": 0,
        "Gr-7": 0,
        "Gr-8": 0,    
        "Su-1": 0,
        "Su-2": 0,
        "Su-3": 0,
        "Su-4": 0,
        "Su-5": 0,
        "Su-6": 0,
        "Su-7": 0,
        "Su-8": 0,    
        "Eu-1": 0,
        "Eu-2": 0,
        "Eu-3": 0,    
        "Eg-1": 0,
        "Eg-2": 0,
        "Eg-3": 0,    
        "FA-1": 0,
    }
    signalRegex = re.compile("[A-Za-z]+-[0-9]+ [^:]+: [0-9]+")
    matches = signalRegex.findall(text)
    for match in matches:
        signame = str(match)[:str(match).find(' ')]
        sigcount = int(re.search(r'\d+', str(match)[str(match).find(' ') + 1:]).group())
        signals[signame] += sigcount
    return signals

def genTruncatedSignals(text):
    signals = {
        "R": 0,
        "F": 0,
        "RF": 0,
        "PR": 0,
        "PF": 0,
        "RR": 0,
        "Ca": 0,
        "Ms": 0,
        "Gr": 0,
        "Su": 0,
        "Eu": 0,
        "Eg": 0,
        "FA": 0,
    }
    signalRegex = re.compile("[A-Za-z]+-[0-9]+ [^:]+: [0-9]+")
    matches = signalRegex.findall(text)
    for match in matches:
        signame = str(match)[:str(match).find(' ') - 2]
        signum = int(str(match)[str(match).find(' ') - 1:str(match).find(' ')])
        sigcount = int(re.search(r'\d+', str(match)[str(match).find(' ') + 1:]).group())
        signals[signame] += sigcount
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