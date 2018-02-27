from convention import Convention
import utils
import json


with open('actorToConvention.txt', 'r') as file:
    actorToConventionFromFile = json.load(file)

convention_data = []
for x in utils.get_raw_text('https://raw.githubusercontent.com/rrrxr6/mcu-actor-appearances/master/conventions.txt').split(','):
    convention_data.append(x.strip())

all_conventions = dict()
for i in range(0, len(convention_data) - 1, 4):
    all_conventions[convention_data[i]] = Convention(convention_data[i + 1], convention_data[i + 2], convention_data[i + 3])

# Move to conventions.txt once guests are announced
# conventions['Edmonton Expo'] =            Convention('https://edmontonexpo.com/guests/media-guests/',                     '09-21-2018', 'div.name')
# conventions['New York Comic Con'] =       Convention('http://www.newyorkcomiccon.com/Guests/',                            '10-04-2018', '')
# conventions['Rhode Island Comic Con'] =   Convention('http://www.ricomiccon.com/guests',                                  '11-02-2018', '')
# conventions['Eternal Con'] =              Convention('http://eternalcon.com/celebrity-guests/',                           '06-16-2018', '')
# conventions[''] =                         Convention('', '', '')

conventionToActor = {}
for convention_name, convention in all_conventions.items():
    actorSet = utils.parse_html(utils.get_html(convention.url), convention.selector, convention_name)
    if actorSet:
        conventionToActor[convention_name] = list(actorSet)

actorToConvention = {}
for convention, actors in conventionToActor.items():
    for actor in actors:
        if actor in actorToConvention:
            actorToConvention[actor].append(convention)
        else:
            actorToConvention[actor] = [convention]

utils.print_dict(actorToConvention, all_conventions)

added, removed, modified, same = utils.dict_compare(actorToConvention, actorToConventionFromFile)
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

