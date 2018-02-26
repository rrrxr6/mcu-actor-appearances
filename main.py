from convention import Convention
import urllib.request
from bs4 import BeautifulSoup
import json


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same


def print_dict(multimap):
    for key, vals in multimap.items():
        print(key)
        if not vals:
            print('\tNone')
        for val in vals:
            print('\t' + val + ' (' + conventions[val].date + ')')
        print('')
    print('----------')


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


def get_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    with urllib.request.urlopen(req) as response:
        return response.read()


def parse_html(html, selector, convention_name):
    temp_actors = set([])
    soup = BeautifulSoup(html, HTML_PARSER)
    for tag in soup.select(selector):
        actor_name = get_name_from_tag(tag)
        if actor_name in MCU_ACTORS and not exception(convention_name, actor_name):
            temp_actors.add(actor_name.title())
    return temp_actors


UTF_8 = 'utf-8'
HTML_PARSER = 'html.parser'
MCU_ACTORS = {'vin diesel', 'chris hemsworth', 'tom hiddleston', 'chris pratt', 'paul bettany', 'elizabeth olsen',
         'anthony mackie', 'chris evans', 'scarlett johansson', 'josh brolin', 'mark ruffalo', 'jeremy renner',
         'don cheadle', 'tom holland', 'chadwick boseman', 'benedict cumberbatch', 'zoe saldana', 'robert downey jr.',
         'bradley cooper', 'sean gunn', 'dave bautista', 'sebastian stan', 'pom klementieff', 'karen gillan',
         'michael rooker', 'karl urban', 'jeff goldblum', 'idris elba', 'anthony hopkins', 'evangeline lilly',
         'cate blanchett', 'taika waititi', 'tessa thompson', 'tilda swinton', 'benedict wong', 'chiwetel ejiofor',
         'mads mikkelsen', 'emily vancamp', 'cobie smulders', 'james spader', 'samuel l. jackson', 'samuel jackson',
         'hayley atwell', 'clark gregg', 'benicio del toro', 'brie larson'}

with open('actorToConvention.txt', 'r') as file:
    actorToConventionFromFile = json.load(file)

conventions = {}
conventions['Planet Comicon'] =             Convention('http://planetcomicon.com/celebrity/',                               '02-16-2018', 'h1')
conventions['ECCC'] =                       Convention('https://www.emeraldcitycomiccon.com/Guests/Entertainment-Guests/',  '03-01-2018', 'div.guest-name')
conventions['Wizard World Cleveland'] =     Convention('https://wizardworld.com/comiccon/cleveland',                        '03-02-2018', 'div.overview h3')
conventions['Lexington Comic Con'] =        Convention('http://lexingtoncomiccon.com/guests.html',                          '03-09-2018', 'div.title h2')
conventions['Toronto Comic Con'] =          Convention('http://comicontoronto.com/guests/',                                 '03-16-2018', 'h2.category-guest-title a')
conventions['Awesome Con'] =                Convention('http://awesome-con.com/guestsdc/',                                  '03-30-2018', 'article.celebrity-guests h4.fusion-rollover-title a')
conventions['Indiana Comic Con'] =          Convention('https://indianacomiccon.com/',                                      '03-30-2018', 'div.entry-content img')
conventions['C2E2'] =                       Convention('https://www.c2e2.com/Guests/Entertainment-Guests/',                 '04-06-2018', 'div.guest-info h3')
conventions['Fan Expo Dallas'] =            Convention('http://fanexpodallas.com/guests/',                                  '04-06-2018', 'h2.category-guest-title a')
conventions['Wizard World Portland'] =      Convention('https://wizardworld.com/comiccon/portland',                         '04-13-2018', 'div.overview h3')
conventions['Calgary Expo'] =               Convention('https://calgaryexpo.com/guests/media-guests/',                      '04-26-2018', 'div.name')
conventions['Conque'] =                     Convention('http://conque.mx/invitados.php',                                    '05-04-2018', 'div.caption-invited h3')
conventions['Fan Expo Regina'] =            Convention('http://fanexporegina.com/guests/',                                  '05-05-2018', 'h2.category-guest-title a')
conventions['Wizard World Philly'] =        Convention('https://wizardworld.com/comiccon/philadelphia',                     '05-17-2018', 'div.overview h3')
conventions['Motor City Comic Con'] =       Convention('http://www.motorcitycomiccon.com/category/media-guests/',           '05-18-2018', 'h2.entry-title a')
conventions['Megacon Orlando'] =            Convention('http://megaconorlando.com/guests/',                                 '05-24-2018', 'h2.category-guest-title a')
conventions['Comic Palooza'] =              Convention('https://www.comicpalooza.com/guests/2018-guests/',                  '05-25-2018', 'div.guestItem h2')
conventions['Wizard World DesMoines'] =     Convention('https://wizardworld.com/comiccon/des-moines',                       '06-01-2018', 'div.overview h3')
conventions['Wizard World Columbus'] =      Convention('https://wizardworld.com/comiccon/columbus',                         '06-08-2018', 'div.overview h3')
conventions['New Jersey Comic Expo'] =      Convention('http://newjerseycomicexpo.com/guests/',                             '06-10-2018', 'p.guestName')
conventions['Denver Comic Con'] =           Convention('https://denvercomiccon.com/guests/',                                '06-15-2018', 'span.et_portfolio_image img')
conventions['Florida Supercon'] =           Convention('http://floridasupercon.com/all-guests-florida-supercon/',           '07-12-2018', 'h3.entry-title a')
conventions['Wizard World Boise'] =         Convention('https://wizardworld.com/comiccon/boise',                            '07-13-2018', 'div.overview h3')
conventions['London Film and Comic Con'] =  Convention('https://www.londonfilmandcomiccon.com/index.php/allguests',         '07-27-2018', 'h3.aidanews2_title a')
conventions['Tampa Bay Comic Con'] =        Convention('https://tampabaycomiccon.com/',                                     '08-03-2018', 'div.entry-content img')
conventions['Boston Comic Con'] =           Convention('http://bostoncomiccon.com/celebrity-guests/',                       '08-10-2018', 'div.cg-name-in-headline a')
conventions['Wizard World Chicago'] =       Convention('https://wizardworld.com/comiccon/chicago',                          '08-23-2018', 'div.overview h3')
conventions['Fan Expo Canada'] =            Convention('https://www.fanexpocanada.com/en/guests/celebrities.html',          '08-30-2018', 'div.callToActionPara b')
conventions['Dragon Con'] =                 Convention('http://www.dragoncon.org/?q=featured_list',                         '08-30-2018', 'td a')
conventions['Salt Lake Comic Con'] =        Convention('https://www.fanxsaltlake.com/guests/',                              '09-06-2018', 'h3.team-member-name')
conventions['Wizard World Madison'] =       Convention('https://wizardworld.com/comiccon/madison',                          '09-21-2018', 'div.overview h3')
conventions['Megacon Tampa Bay'] =          Convention('http://megacontampabay.com/guests/',                                '09-21-2018', 'h2.category-guest-title a')
conventions['Baltimore Comic Con'] =        Convention('http://baltimorecomiccon.com/guests/',                              '09-28-2018', 'ul li')
conventions['Dallas Fan Days'] =            Convention('http://dallasfandays.com/guests/',                                  '10-19-2018', 'h2.category-guest-title a')
conventions['Wizard World Oklahoma City'] = Convention('https://wizardworld.com/comiccon/oklahoma-city-2018',               '10-26-2018', 'div.overview h3')
conventions['LA Comic Con'] =               Convention('http://www.stanleeslacomiccon.com/guests/media-guests',             'mm-dd-2018', 'h4.guest-title a')
conventions['Memphis Comic Expo'] =         Convention('http://www.memphiscomicexpo.com/guests/',                           'mm-dd-2018', 'div.textwidget strong')
conventions['Fan Expo Vancouver'] =         Convention('http://fanexpovancouver.com/guests/',                               'mm-dd-2018', 'h2.category-guest-title a')
conventions['Wizard World Montgomery'] =    Convention('https://wizardworld.com/comiccon/montgomery',                       'mm-dd-2018', 'div.overview h3')
conventions['Wizard World Springfield'] =   Convention('https://wizardworld.com/comiccon/springfield',                      'mm-dd-2018', 'div.overview h3')
conventions['Wizard World Biloxi'] =        Convention('https://wizardworld.com/comiccon/biloxi',                           'mm-dd-2018', 'div.overview h3')
conventions['Wizard World Winston Salem'] = Convention('https://wizardworld.com/comiccon/winston-salem',                    'mm-dd-2018', 'div.overview h3')
conventions['Wizard World Peoria'] =        Convention('https://wizardworld.com/comiccon/peoria',                           'mm-dd-2018', 'div.overview h3')
conventions['Wizard World Austin'] =        Convention('https://wizardworld.com/comiccon/austin-2018',                      'mm-dd-2018', 'div.overview h3')

# conventions['Edmonton Expo'] =            Convention('https://edmontonexpo.com/guests/media-guests/',                     '09-21-2018', 'div.name')
# conventions['New York Comic Con'] =       Convention('http://www.newyorkcomiccon.com/Guests/',                            '10-04-2018', '')
# conventions['Rhode Island Comic Con'] =   Convention('http://www.ricomiccon.com/guests',                                  '11-02-2018', '')
# conventions['Eternal Con'] =              Convention('http://eternalcon.com/celebrity-guests/',                           '06-16-2018', '')
# conventions[''] =                         Convention('', '', '')

conventionToActor = {}
for convention_name, convention in conventions.items():
    conventionToActor[convention_name] = list(parse_html(get_html(convention.url), convention.selector, convention_name))

actorToConvention = {}
for convention, actors in conventionToActor.items():
    for actor in actors:
        if actor in actorToConvention:
            actorToConvention[actor].append(convention)
        else:
            actorToConvention[actor] = [convention]

print_dict(actorToConvention)

added, removed, modified, same = dict_compare(actorToConvention, actorToConventionFromFile)
print("Added: ", end='')
print(added)
print("Removed: ", end='')
print(removed)
print("Modified: ", end='')
print(modified)
print("Same: ", end='')
print(same)

with open('actorToConvention.txt', 'w') as file:
    json.dump(actorToConvention, file)

