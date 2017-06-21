# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 03:24:07 2017

@author: zhaoy
"""

import yaml

data = {'name': 'Silenthand Olleander', 'race': 'Human',
'traits': ['ONE_HAND', 'ONE_EYE']}

print yaml.dump(data)


stream = file('document.yaml', 'w')
yaml.dump(data, stream)    # Write a YAML representation of data to 'document.yaml'.
print yaml.dump(data)      # Output the document to the screen.
stream.close()

print yaml.dump([1,2,3], explicit_start=True)

print yaml.dump_all([1,2,3], explicit_start=True)

class Hero:
    def __init__(self, name, hp, sp):
        self.name = name
        self.hp = hp
        self.sp = sp
    def __repr__(self):
        return "%s(name=%r, hp=%r, sp=%r)" % (
            self.__class__.__name__, self.name, self.hp, self.sp)

print yaml.dump(Hero("Galain Ysseleg", hp=-3, sp=2))

print yaml.dump(range(50))
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
  23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
  43, 44, 45, 46, 47, 48, 49]

print yaml.dump(range(50), width=50, indent=4)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
    40, 41, 42, 43, 44, 45, 46, 47, 48, 49]

print yaml.dump(range(5), canonical=True)

print yaml.dump(range(5), default_flow_style=False)

print yaml.dump(range(5), default_flow_style=True, default_style='"')

class Monster(yaml.YAMLObject):
    yaml_tag = u'!Monster'
    def __init__(self, name, hp, ac, attacks):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attacks = attacks
    def __repr__(self):
        return "%s(name=%r, hp=%r, ac=%r, attacks=%r)" % (
            self.__class__.__name__, self.name, self.hp, self.ac, self.attacks)

yaml.load("""
--- !Monster
name: Cave spider
hp: [2,6]    # 2d6
ac: 16
attacks: [BITE, HURT]
""")


print yaml.dump(Monster(
    name='Cave lizard', hp=[3,6], ac=16, attacks=['BITE','HURT']))

class Dice(tuple):
    def __new__(cls, a, b):
        return tuple.__new__(cls, [a, b])
    def __repr__(self):
        return "Dice(%s,%s)" % self

print Dice(3,6)

print yaml.dump(Dice(3,6))

print yaml.dump(Dice(3,6))


def dice_representer(dumper, data):
    return dumper.represent_scalar(u'!dice', u'%sd%s' % data)

yaml.add_representer(Dice, dice_representer)

print yaml.dump({'gold': Dice(10,6)})

def dice_constructor(loader, node):
    value = loader.construct_scalar(node)
    a, b = map(int, value.split('d'))
    return Dice(a, b)

yaml.add_constructor(u'!dice', dice_constructor)

print yaml.load("""
initial hit points: !dice 8d4
""")

import re
pattern = re.compile(r'^\d+d\d+$')
yaml.add_implicit_resolver(u'!dice', pattern)

print yaml.dump({'treasure': Dice(10,20)})

print yaml.load("""
damage: 5d10
""")