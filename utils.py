from urllib.request import Request, urlopen
from colorama import init, Fore, Style
import sys


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


def is_actor_of_interest(actor):
    if len(sys.argv) is 2:
        actor_group = sys.argv[1]
        if actor_group == "mcu":
            return actor.lower() in get_mcu_actors()
        elif actor_group == "office":
            return actor.lower() in get_office_actors()
        elif actor_group == "potter":
            return actor.lower() in get_potter_actors()
    return actor.lower() in get_mcu_actors()


def print_actor_color(actor):
    if is_actor_gotten(actor):
        print(f'{Fore.LIGHTGREEN_EX}'+actor+f'{Style.RESET_ALL}', end='')
    elif is_actor_super_wanted(actor):
        print(f'{Fore.LIGHTCYAN_EX}'+actor+f'{Style.RESET_ALL}', end='')
    elif is_actor_wanted(actor):
        print(f'{Fore.CYAN}'+actor+f'{Style.RESET_ALL}', end='')
    elif actor.lower() in get_mcu_actors():
        print(f'{Fore.YELLOW}'+actor+f'{Style.RESET_ALL}', end='')
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
        if is_actor_of_interest(actor):
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
    return actor.lower() in ["brie larson",
                "chadwick boseman",
                "cobie smulders",
                "danai gurira",
                "kevin feige",
                "letitia wright",
                "samuel l. jackson",
                "samuel jackson",
                "vin diesel"]


def is_actor_super_wanted(actor):
    return actor.lower() in ["benedict cumberbatch",
                "bradley cooper",
                "chris hemsworth",
                "chris pratt",
                "mark ruffalo",
                "robert downey jr.",
                "scarlett johansson"]


def is_actor_gotten(actor):
    return actor.lower() in ["anthony mackie",
                "anthony russo",
                "benedict wong",
                "chris evans",
                "clark gregg",
                "dave bautista",
                "don cheadle",
                "elizabeth olsen",
                "evangeline lilly",
                "hayley atwell",
                "jeremy renner",
                "joe russo",
                "josh brolin",
                "karen gillan",
                "neal mcdonough",
                "paul bettany",
                "paul rudd",
                "pom klementieff",
                "sebastian stan",
                "tom hiddleston",
                "tom holland",
                "zoe saldana"]


def get_mcu_actors():
    actors = ["aaron taylor johnson",
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
                "terry notary",
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
	
	
def get_office_actors():
    actors = ["rainn wilson",
                "jenna fischer",
                "steve carell",
                "john krasinski",
                "angela kinsey",
                "ed helms",
                "mindy kaling",
                "brian baumgartner",
                "oscar nunez",
                "oscar nuñez",
                "bj novak",
                "b.j. novak",
                "leslie david baker",
                "ellie kemper",
                "creed bratton",
                "paul lieberstein",
                "phyllis smith",
                "kate flannery",
                "craig t. robinson",
                "craig robinson",
                "melora hardin",
                "catherine tate",
                "zach woods",
                "jake lacy",
                "david denman",
                "amy ryan",
                "clark duke",
                "rashida jones"]
    return actors


def get_potter_actors():
    actors = ["daniel radcliffe",
                "emma watson",
                "rupert grint",
                "tom felton",
                "robbie coltrane",
                "michael gambon",
                "maggie smith",
                "bonnie wright",
                "ralph fiennes",
                "matthew lewis",
                "helena bonham carter",
                "gary oldman",
                "warwick davis",
                "evanna lynch",
                "david thewlis",
                "julie walters",
                "emma thompson",
                "brendan gleeson",
                "richard griffiths",
                "domhnall gleeson",
                "robert pattinson",
                "fiona shaw",
                "jason isaacs",
                "alfred enoch",
                "oliver phelps",
                "james phelps",
                "james and oliver phelps",
                "harry melling",
                "helen mccrory",
                "john cleese",
                "natalia tena",
                "kenneth branagh",
                "devon murray",
                "david bradley",
                "geraldine somerville",
                "timothy spell",
                "mark williams",
                "katie leung",
                "imelda staunton",
                "ian hart",
                "jim broadbent"]
    return actors
