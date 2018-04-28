from urllib.request import Request, urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
import collections
import sys


class NullDevice:
    def write(self, s):
        pass


def suppress_err():
    sys.stderr = NullDevice()


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same


def print_actors(actor_to_convention, all_conventions):
    ordered = collections.OrderedDict(sorted(actor_to_convention.items()))
    for actor, conventions in ordered.items():
        print(actor)
        if not conventions:
            print('\tNone')
        for convention in conventions:
            print('\t' + convention + ' (' + all_conventions[convention].date + ')')
        print('')
    print('---------------------------')


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
    html, error = get_html(url)
    return html.read().decode(UTF_8)


def get_html(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    error = ''
    response = ''
    try:
        response = urlopen(req)
    except URLError as e:
        error = 'The server at ' + url + ' couldn\'t fulfill the request.\n'
        if hasattr(e, 'reason'):
            error = error + 'Reason: ' + e.reason + '\n'
        if hasattr(e, 'code'):
            error = error + 'Error code: ' + str(e.code) + '\n'
        error = error + '---------------------------\n'
    return response, error


def parse_html(html, selector, convention_name):
    if not html:
        return
    temp_actors = set([])
    soup = BeautifulSoup(html, HTML_PARSER)
    # print(soup)
    for tag in soup.select(selector):
        actor_name = get_name_from_tag(tag)
        if actor_name in MCU_ACTORS and not exception(convention_name, actor_name):
            temp_actors.add(actor_name.title())
    return temp_actors


UTF_8 = 'utf-8'
HTML_PARSER = 'html.parser'
MCU_ACTORS = get_raw_text('https://raw.githubusercontent.com/rrrxr6/mcu-actor-appearances/master/actors.txt').split('\n')
MCU_ACTORS.remove('')
