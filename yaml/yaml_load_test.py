# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 02:55:20 2017

@author: zhaoy
"""

import yaml

yaml_content = yaml.load("""
- Hesperiidae
- Papilionidae
- Apatelodidae
- Epiplemidae
""")

print yaml_content


###
stream = file('./sample.yaml', 'r')
yaml_content = yaml.load(stream)
print yaml_content
stream.close()


###
documents = """
---
name: The Set of Gauntlets 'Pauraegen'
description: >
    A set of handgear with sparks that crackle
    across its knuckleguards.
---
name: The Set of Gauntlets 'Paurnen'
description: >
  A set of gauntlets that gives off a foul,
  acrid odour yet remains untarnished.
---
name: The Set of Gauntlets 'Paurnimmen'
description: >
  A set of handgear, freezing with unnatural cold.
"""

for data in yaml.load_all(documents):
    print data

###
yaml_content = yaml.load("""
none: [~, null]
bool: [true, false, on, off]
int: 42
float: 3.14159
list: [LITE, RES_ACID, SUS_DEXT]
dict: {hp: 13, sp: 5}
""")

print yaml_content


###
class Hero:
    def __init__(self, name, hp, sp):
        self.name = name
        self.hp = hp
        self.sp = sp
    def __repr__(self):
        return "%s(name=%r, hp=%r, sp=%r)" % (
            self.__class__.__name__, self.name, self.hp, self.sp)

yaml_content = yaml.load("""
!!python/object:__main__.Hero
name: Welthyr Syxgon
hp: 1200
sp: 0
""")

print yaml_content
