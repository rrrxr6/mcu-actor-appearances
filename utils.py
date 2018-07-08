from urllib.request import Request, urlopen
from colorama import init, Fore, Style


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if set(d1[o]) != set(d2[o])}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same


def print_conventions(convention_to_actor):
    init(convert=True)
    print('---------------------------')
    for convention, actors in convention_to_actor.items():
        print(convention.name + ' (' + convention.date + ')')
        for actor in actors:
            print('\t', end='')
            print_actor_color(actor)
            print()
        print('')


def print_actors(actor_to_convention):
    init(convert=True)
    print('---------------------------')
    for actor, conventions in actor_to_convention.items():
        print_actor_color(actor)
        print()
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
        return response.read().decode()
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


def print_actor_color(actor):
    if is_actor_gotten(actor):
        print(f'{Fore.LIGHTGREEN_EX}'+actor+f'{Style.RESET_ALL}', end='')
    elif is_actor_super_wanted(actor):
        print(f'{Fore.LIGHTCYAN_EX}'+actor+f'{Style.RESET_ALL}', end='')
    elif is_actor_wanted(actor):
        print(f'{Fore.CYAN}'+actor+f'{Style.RESET_ALL}', end='')
    else:
        print(f'{Fore.WHITE}'+actor+f'{Style.RESET_ALL}', end='')


def get_actor_color(actor):
    if is_actor_gotten(actor):
        return 4
    elif is_actor_super_wanted(actor):
        return 1
    elif is_actor_wanted(actor):
        return 2
    else:
        return 3


def print_actor_set(actors):
    print('{', end='')
    sorted_actors = sorted(actors, key=lambda actor:get_actor_color(actor))
    for actor in sorted_actors:
        print_actor_color(actor)
        print(', ', end='')
    print('}')


def print_removed_actor_set(actors):
    print('{', end='')
    for actor in actors:
        print(f'{Fore.LIGHTRED_EX}' + actor + f'{Style.RESET_ALL}', end='')
        print(', ', end='')
    print('}')


def print_added_actor_set(actors):
    print('{', end='')
    for actor in actors:
        print(f'{Fore.GREEN}' + actor + f'{Style.RESET_ALL}', end='')
        print(', ', end='')
    print('}')


def is_actor_wanted(actor):
    return actor.lower() in ["anthony russo",
                "benedict wong",
                "brie larson",
                "cobie smulders",
                "danai gurira",
                "evangeline lilly",
                "jeremy renner",
                "joe russo",
                "kevin feige",
                "paul rudd",
                "samuel l. jackson",
                "samuel jackson"]


def is_actor_super_wanted(actor):
    return actor.lower() in ["anthony mackie",
                "benedict cumberbatch",
                "bradley cooper",
                "chadwick boseman",
                "chris evans",
                "chris hemsworth",
                "chris pratt",
                "don cheadle",
                "josh brolin",
                "karen gillan",
                "letitia wright",
                "mark ruffalo",
                "robert downey jr.",
                "scarlett johansson",
                "vin diesel",
                "zoe saldana"]


def is_actor_gotten(actor):
    return actor.lower() in ["clark gregg",
                "dave bautista",
                "elizabeth olsen",
                "hayley atwell",
                "paul bettany",
                "pom klementieff",
                "sebastian stan",
                "tom hiddleston",
                "tom holland"]


def get_actors():
    actors = ["aaron taylor-johnson",
                "aaron taylor johnson",
                "andy serkis",
                "angela bassett",
                "anthony hopkins",
                "anthony mackie",
                "anthony russo",
                "ben kingsley",
                "ben mendelsohn",
                "benedict cumberbatch",
                "benedict wong",
                "benicio del toro",
                "bobby cannavale",
                "bradley cooper",
                "brie larson",
                "cate blanchett",
                "chadwick boseman",
                "chiwetel ejiofor",
                "chris evans",
                "chris hemsworth",
                "chris pratt",
                "chris sullivan",
                "christopher eccleston",
                "clancy brown",
                "clark gregg",
                "cobie smulders",
                "corey stoll",
                "danai gurira",
                "daniel bruhl",
                "daniel kaluuya",
                "dave bautista",
                "david dastmalchian",
                "djimon hounsou",
                "dominic cooper",
                "don cheadle",
                "donald glover",
                "elizabeth debicki",
                "elizabeth olsen",
                "emily vancamp",
                "evangeline lilly",
                "faran tahir",
                "florence kasumba",
                "forest whitaker",
                "frank grillo",
                "gemma chan",
                "glenn close",
                "guy pearce",
                "gwyneth paltrow",
                "hannah john-kamen",
                "hannah john kamen",
                "hayley atwell",
                "hugo weaving",
                "idris elba",
                "jacob batalon",
                "james spader",
                "jamie alexander",
                "jeff bridges",
                "jeff goldblum",
                "jeremy renner",
                "joe russo",
                "john c. reilly",
                "john kani",
                "john slattery",
                "jon favreau",
                "josh brolin",
                "jude law",
                "judy greer",
                "karen gillan",
                "karl urban",
                "kat dennings",
                "kevin feige",
                "kurt russel",
                "laura haddock",
                "laura harrier",
                "laurence fishburne",
                "lee pace",
                "letitia wright",
                "linda cardellini",
                "lupita nyong'o",
                "mads mikkelsen",
                "marisa tomei",
                "mark ruffalo",
                "martin freeman",
                "maximilliano hernandez",
                "michael b. jordan",
                "michael douglas",
                "michael keaton",
                "michael pena",
                "michael rooker",
                "michelle pfeiffer",
                "mickey rourke",
                "natalie portman",
                "neal mcdonough",
                "paul bettany",
                "paul rudd",
                "peter dinklage",
                "peter serafinowicz",
                "pom klementieff",
                "rachel house",
                "rachel mcadams",
                "ray stevenson",
                "rene russo",
                "robert downey jr.",
                "robert redford",
                "sam rockwell",
                "samuel l. jackson",
                "samuel jackson",
                "scarlett johansson",
                "sean gunn",
                "sebastian stan",
                "shaun toub",
                "stanley tucci",
                "stellan skarsgard",
                "sterling k. brown",
                "sylvester stallone",
                "t.i.",
                "tip harris",
                "tadanobu asano",
                "taika waititi",
                "tessa thompson",
                "thomas kretschmann",
                "tilda swinton",
                "toby jones",
                "tom hiddleston",
                "tom holland",
                "tom vaughan-lawlor",
                "tom vaughan lawlor",
                "tommy lee jones",
                "tony revolori",
                "vin diesel",
                "walter goggins",
                "william hurt",
                "winston duke",
                "zachary levi",
                "zendaya",
                "zoe saldana"]
    return actors