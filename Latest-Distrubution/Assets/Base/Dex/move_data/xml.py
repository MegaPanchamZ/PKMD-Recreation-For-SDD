letter = 'é'
from os import path
from os import listdir
from os.path import isfile, join

locale = path.dirname(__file__)

def encode():
    onlyfiles = [f for f in listdir(locale) if f != "xml.py" if isfile(join(locale, f))]
    for i in onlyfiles:
        lst = []
        outfolder = locale + "\edited" + "\\"
        f = open(i)
        outfile = open(outfolder + i[1:], "w")
        for d in f:
            outfile.write(d.replace(letter, "e"))
        outfile.close()
        f.close()

#print(locale)

encode()
