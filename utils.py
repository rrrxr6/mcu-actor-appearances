from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import collections
# import sys


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same


def print_conventions(convention_to_actor):
    print('---------------------------')
    for convention, actors in convention_to_actor.items():
        print(convention.name + ' (' + convention.date + ')')
        for actor in actors:
            print('\t' + actor)
        print('')


def print_actors(actor_to_convention):
    print('---------------------------')
    ordered = collections.OrderedDict(sorted(actor_to_convention.items()))
    for actor, conventions in ordered.items():
        print(actor)
        for convention in conventions:
            print('\t' + convention.name + ' (' + convention.date + ')')
        print('')


def exception(convention_name, actor_name):
    if actor_name == 'karen gillan' and convention_name == 'Fan Expo Dallas':
        return True
    return False


def get_name_from_tag(tag):
    name = tag.text.strip().lower()
    if not name:
        if 'alt' in tag.attrs:
            name = tag.attrs['alt'].strip().lower()
    return name


def get_raw_text(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    response = ''
    try:
        response = urlopen(req)
    except:
        # e = sys.exc_info()[0]
        print('[ERROR] Failed to retrieve contents from ' + url)
    if response:
        return response.read().decode(UTF_8)
    else:
        return response


def get_html(convention):
    req = Request(convention.url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    try:
        response = urlopen(req)
    except:
        # e = sys.exc_info()[0]
        print('[ERROR] Failed to retrieve ' + convention.name + ' contents from ' + convention.url)
        return ''
    return response


def parse_html(html, convention):
    if not html:
        return
    temp_actors = set([])
    try:
        print('[INFO] Parsing HTML for ' + convention.name)
        soup = BeautifulSoup(html, HTML_PARSER)
    except:
        print('[ERROR] Failed to parse HTML for ' + convention.name)
        return ''

    for tag in soup.select(convention.selector):
        actor_name = get_name_from_tag(tag)
        if actor_name in MCU_ACTORS and not exception(convention.name, actor_name):
            temp_actors.add(actor_name.title())
    return temp_actors


UTF_8 = 'utf-8'
HTML_PARSER = 'html.parser'
print('[INFO] Downloading actor list')
MCU_ACTORS = get_raw_text('https://raw.githubusercontent.com/rrrxr6/mcu-actor-appearances/master/actors.txt').split('\n')
MCU_ACTORS.remove('')
