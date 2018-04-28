from convention import Convention
from utils import *
from pathlib import Path
import json
import sys
import os


suppress_err()
actorToConventionFromFile = dict()
filename = os.path.join(os.path.dirname(__file__), 'actorToConvention.txt')
if Path(filename).is_file():
    with open(filename, 'r') as file:
        actorToConventionFromFile = json.load(file)

all_conventions = dict()
convention_data = urlopen('https://raw.githubusercontent.com/rrrxr6/mcu-actor-appearances/master/conventions.txt')
for byte_line in convention_data:
    text_line = byte_line.decode('utf-8')
    if text_line.startswith('#'):
        continue
    con = text_line.split(',')
    all_conventions[con[0].strip()] = Convention(con[1].strip(), con[2].strip(), con[3].strip())

conventionToActor = {}
errors = ''

sys.stdout.write('[%s]' % (' ' * len(all_conventions.keys())))
sys.stdout.flush()
sys.stdout.write('\b' * (len(all_conventions.keys()) + 1))

for convention_name, convention in all_conventions.items():
    html, error = get_html(convention.url)
    errors = errors + error
    actorSet = parse_html(html, convention.selector, convention_name)
    if actorSet:
        conventionToActor[convention_name] = list(actorSet)
    sys.stdout.write('#')
    sys.stdout.flush()

sys.stdout.write("\n")

actorToConvention = dict()
for convention, actors in conventionToActor.items():
    for actor in actors:
        if actor in actorToConvention:
            actorToConvention[actor].append(convention)
        else:
            actorToConvention[actor] = [convention]

print_actors(actorToConvention, all_conventions)

added, removed, modified, same = dict_compare(actorToConvention, actorToConventionFromFile)
print('Added: ', end='')
print(added)
print('Removed: ', end='')
print(removed)
print('Modified: ', end='')
print(modified)
print('Same: ', end='')
print(same)
print('---------------------------')
print('Errors:')
print(errors)
with open(filename, 'w') as file:
    json.dump(actorToConvention, file)
