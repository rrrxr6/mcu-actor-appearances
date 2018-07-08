from convention import Convention
from utils import *
from pathlib import Path
import json
import os
import numpy as np
import multiprocessing as multi
from bs4 import BeautifulSoup
import collections


def perform_extraction(conventions, c2a_map, actors):
    for convention in conventions:
        print('[INFO]' + ' Downloading content for ' + convention.name)
        html = get_html(convention)
        if html:
            actorSet = parse_html(html, convention, actors)
            if actorSet:
                c2a_map[convention] = list(actorSet)
    return 9


def parse_html(html, convention, actors):
    if not html:
        return
    temp_actors = set([])
    try:
        print('[INFO] Parsing HTML for ' + convention.name)
        soup = BeautifulSoup(html, 'html.parser')
    except:
        print('[ERROR] Failed to parse HTML for ' + convention.name)
        return ''

    for tag in soup.select(convention.selector):
        actor_name = get_name_from_tag(tag)
        if actor_name in actors and not exception(convention.name, actor_name):
            temp_actors.add(actor_name.title())
    return temp_actors


if __name__ == '__main__':
    run_with_local_con_data = False
    actorToConventionFromFile = dict()
    filename = os.path.join(os.path.dirname(__file__), 'actorToConvention.txt')
    if Path(filename).is_file():
        with open(filename, 'r') as file:
            actorToConventionFromFile = json.load(file)

    print('[INFO] Downloading actor list')
    MCU_ACTORS = get_raw_text('https://raw.githubusercontent.com/rrrxr6/mcu-actor-appearances/master/actors.txt').split('\n')
    MCU_ACTORS.remove('')
    # MCU_ACTORS.append('roy thomas')

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
    conventionToActor = multi.Manager().dict()

    cpus = multi.cpu_count()
    workers = []
    convention_bins = np.array_split(all_conventions, cpus)
    for cpu in range(cpus):
        worker = multi.Process(name=str(cpu), target=perform_extraction, args=(convention_bins[cpu], conventionToActor, MCU_ACTORS))
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()

    conventionToActor = collections.OrderedDict(sorted(conventionToActor.items(), key=lambda con_tuple: con_tuple[0].date))
    print_conventions(conventionToActor)
    actorToConvention = dict()
    for convention, actors in conventionToActor.items():
        for actor in actors:
            if actor in actorToConvention:
                actorToConvention[actor].append(convention)
            else:
                actorToConvention[actor] = [convention]

    actorToConvention = collections.OrderedDict(sorted(actorToConvention.items()))
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
        print_added_actor_set(added)
        print('Removed: ', end='')
        print_removed_actor_set(removed)
        print('Modified: ')
        for key, val in modified.items():
            print('\t', end='')
            print_actor_color(key)
            print(val)
        print('Same: ', end='')
        print_actor_set(same)
        print('---------------------------')

        with open(filename, 'w') as file:
            json.dump(simpleActorToConvention, file)
