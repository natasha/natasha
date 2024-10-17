import json
import sys
import io

# вызов из php:
# $arg1 = escapeshellarg($addr);
# $command = "python C:/projects/py/addr/natashapi.py $arg1";

# Получаем аргументы
line = sys.argv[1]

from natasha import MorphVocab, AddrExtractor
morph = MorphVocab()
extractor = AddrExtractor(morph)

match = extractor.find(line)
response = {
    'start': match.start,
    'stop': match.stop,
    'address': []
}
for part in match.fact.parts:
    address_part = {
        'value': part.value,
        'type': part.type
    }
    response['address'].append(address_part)

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print(json.dumps(response, ensure_ascii=False))