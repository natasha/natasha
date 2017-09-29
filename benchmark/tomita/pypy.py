
import sys
from natasha import NamesExtractor

extractor = NamesExtractor()

path = sys.argv[1]

with open(path) as file:
    for line in file:
        line = line.decode('utf8')
        matches = extractor(line)
        print len(list(matches))
