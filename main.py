from convention import Convention
from utils import *
from pathlib import Path
import json
import os

run_with_local_con_data = False
actorToConventionFromFile = dict()
filename = os.path.join(os.path.dirname(__file__), 'actorToConvention.txt')
if Path(filename).is_file():
    with open(filename, 'r') as file:
        actorToConventionFromFile = json.load(file)

all_conventions = []
if run_with_local_con_data:
    print('[INFO] Using local convention list')
    filename = os.path.join(os.path.dirname(__file__), 'conventions.txt')
    if Path(filename).is_file():
        with open(filename, 'r') as file:
            for text_line in file:
                if text_line.startswith('#'):
                    continue
                con = text_line.split(',')
                all_conventions.append(Convention(con[0].strip(), con[1].strip(), con[2].strip(), con[3].strip()))
else:
    print('[INFO] Downloading convention list')
    convention_data = urlopen('https://raw.githubusercontent.com/rrrxr6/mcu-actor-appearances/master/conventions.txt')
    for byte_line in convention_data:
        text_line = byte_line.decode('utf-8')
        if text_line.startswith('#'):
            continue
        con = text_line.split(',')
        all_conventions.append(Convention(con[0].strip(), con[1].strip(), con[2].strip(), con[3].strip()))

num_of_conventions = len(all_conventions)

conventionToActor = {}
for index, convention in enumerate(all_conventions):
    print('[INFO][' + str(index + 1) + '/' + str(num_of_conventions) + '] Downloading content for ' + convention.name)
    html = get_html(convention)
    if html:
        actorSet = parse_html(html, convention)
        if actorSet:
            conventionToActor[convention] = list(actorSet)

print_conventions(conventionToActor)
actorToConvention = dict()
for convention, actors in conventionToActor.items():
    for actor in actors:
        if actor in actorToConvention:
            actorToConvention[actor].append(convention)
        else:
            actorToConvention[actor] = [convention]

print_actors(actorToConvention)

if not run_with_local_con_data:
    simpleActorToConvention = dict()
    for actor, conventions in actorToConvention.items():
        convention_names = []
        for con in conventions:
            convention_names.append(con.name)
        simpleActorToConvention[actor] = convention_names

    added, removed, modified, same = dict_compare(simpleActorToConvention, actorToConventionFromFile)
    print('Added: ', end='')
    print(added)
    print('Removed: ', end='')
    print(removed)
    print('Modified: ')
    for key, val in modified.items():
        print('\t', key, val)
    print('Same: ', end='')
    print(same)
    print('---------------------------')

    with open(filename, 'w') as file:
        json.dump(simpleActorToConvention, file)
