# Type chk

from random import randint

'''
key = Normal, Fight, Flying, Poison, Ground, Rock, Bug, Ghost, Steel, Fire,
      Water, Grass, Electric, Pyschic, Ice, Dragon, Dark

    Need to Create a 2D array which holds type Factor
'''
Type_array = [
    ['Normal',1,1,1,1,1,0.5,1,0,0.5,1,1,1,1,1,1,1,1],
    ['Fight',2,1,0.5,0.5,1,2,0.5,0,2,1,1,1,1,0.5,2,1,2],
    ['Flying',1,2,1,1,1,0.5,2,1,0.5,1,1,2,0.5,1,1,1,1],
    ['Poison',1,1,1,0.5,0.5,0.5,1,0.5,0,1,1,2,1,1,1,1,1],
    ['Ground',1,1,0.5,2,1,2,0.5,1,2,2,1,0.5,2,1,1,1,1],
    ['Rock',1,0.5,2,1,0.5,1,2,1,0.5,2,1,1,1,1,2,1,1],
    ['Bug',1,0.5,0.5,0.5,1,1,1,0.5,0.5,0.5,1,2,1,2,1,1,2],
    ['Ghost',0,1,1,1,1,1,1,2,0.5,1,1,1,1,2,1,1,0.5],
    ['Steel',1,1,1,1,1,2,1,1,0.5,0.5,0.5,1,0.5,1,2,1,1],
    ['Fire',1,1,1,1,1,0.5,2,1,2,0.5,0.5,2,1,1,2,0.5,1],
    ['Water',1,1,1,1,2,2,1,1,1,2,0.5,0.5,1,1,1,0.5,1],
    ['Grass',1,1,0.5,0.5,2,2,0.5,1,0.5,0.5,2,0.5,1,1,1,0.5,1],
    ['Electric',1,1,2,1,0,1,1,1,1,1,2,0.5,0.5,1,1,0.5,1],
    ['Pyschic',1,2,1,2,1,1,1,1,0.5,1,1,1,1,0.5,1,1,0],
    ['Ice',1,1,2,1,2,1,1,1,0.5,0.5,0.5,2,1,1,0.5,2,1],
    ['Dragon',1,1,1,1,1,1,1,1,0.5,1,1,1,1,1,1,2,1],
    ['Dark',1,0.5,1,1,1,1,1,2,0.5,1,1,1,1,2,1,1,0.5]
    ]

Type_indexes= {'Normal':1, 'Fight':2, 'Flying':3, 'Poison':4, 'Ground':5,
               'Rock':6, 'Bug':7, 'Ghost':8, 'Steel':9, 'Fire':10,
               'Water':11, 'Grass':12, 'Electric':13, 'Pyschic':14,
               'Ice':15, 'Dragon':16, 'Dark':17}

def Multiplier(Poketype, MoveType):
    multipliers = Type_array[Type_indexes[Poketype] -1 ]
    factor = multipliers[Type_indexes[MoveType]]
    return factor

# Test Multiplier factor Poison atk v bug type
#print(Multiplier('Poison', 'Bug'))

def Calculate_Damage(level, Power, Atk_user, Def_target, target_type, movetype, usertype):
    Damage = (((((2 * level)/5) + 2)*(Power * (Atk_user/Def_target)))/50) + 1
    factor = Multiplier(movetype, target_type)
    STAB = 1
    if usertype == movetype:
        STAB = 1.5
    Modifier = factor * STAB * (randint(217, 255)/255)
    Damage = Damage * Modifier
    if Damage > 999:
        return 999
    return int(Damage)

# Test values
# level, Power, Atk_user, Def_target, target_type, movetype, usertype
#print(Calculate_Damage(100, 120, 50, 30, 'Fire', 'Water', 'Water'))
    
