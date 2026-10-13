"""Kevin se enoja cada vez que le dices que no: primero se queja, luego te acecha de noche, y al final te persigue.
«Perdón, Kevin» lo calma.
"""
from canon.shim import *  # noqa: F401,F403
from canon import shim

KB, KH, KHE = 7320115, 7320122, 7320124  # cuerpo quieto, cabeza normal, cabeza «drogada» (la de enojado)
KC = '#ffb347'


def build(c):
    shim.use(c)
    c.objective('dv.kno')
    ks = lambda t, sel='@a[distance=..20]': say('Kevin', KC, '#ffd27a', t, 140, sel)
    c.patch('kevin/clicked', lambda s: s if 'dv.kv set 15' in s else s.rstrip('\n') + '\nexecute unless score #kev dv.dev matches 1.. run ' +
            menu('@a[tag=dv_talker]', '', KC, [('No, Kevin', '/trigger dv.kv set 15'), ('Perdón, Kevin', '/trigger dv.kv set 16')]) + '\n')
    c.patch('kevin/c/run', lambda s: s if 'k2/no' in s else s.rstrip('\n') +
            '\nexecute if score #kc dv.tmp matches 15 run function canon:k2/no\nexecute if score #kc dv.tmp matches 16 run function canon:k2/perdon\n')
    F('k2/no', '''
scoreboard players add @a[tag=dv_ktalk] dv.kno 1
execute if score @a[tag=dv_ktalk,limit=1] dv.kno matches 1 run function canon:k2/no1
execute if score @a[tag=dv_ktalk,limit=1] dv.kno matches 2 run function canon:k2/no2
execute if score @a[tag=dv_ktalk,limit=1] dv.kno matches 3 run function canon:k2/no3
execute if score @a[tag=dv_ktalk,limit=1] dv.kno matches 4.. run function canon:k2/no4
''')
    F('k2/no1', ks('Bueno, bueno. Otro día. Tranquilo.'))
    F('k2/no2', ks('¿Otra vez no? Ok... ok. No pasa nada. Nada.'))
    F('k2/no3', head(KHE) + '\n' + ks('Siempre me dices que no. Siempre. ¿Sabes qué se siente?') +
      '\nplaysound canon:gen.voz_kevin_enojado hostile @a[tag=dv_ktalk] ~ ~ ~ 1 1')
    F('k2/no4', head(KHE) + '\n' + ks('Ya veremos quién le dice que no a quién. Esta noche.') +
      '\nplaysound canon:gen.voz_kevin_te_veo hostile @a[tag=dv_ktalk] ~ ~ ~ 1 0.9\nfunction canon:kevin/se_va')
    F('k2/perdon', '''
execute if score @a[tag=dv_ktalk,limit=1] dv.kno matches 1.. run function canon:k2/perdon_si
execute unless score @a[tag=dv_ktalk,limit=1] dv.kno matches 1.. run function canon:k2/perdon_nada
''')
    F('k2/perdon_si', head(KH) + '\n' + ks('Jajaja, tranquilo, mano. Ya pasó. ¿Fiesta?') + '\nscoreboard players set @a[tag=dv_ktalk] dv.kno 0')
    F('k2/perdon_nada', ks('¿Perdón por qué? Jaja, no me has hecho nada. Todavía.'))

    # ------------------------------------------------------------ Kevin acecha de noche
    F('k2/acecha/summon', rig_summon(['dv_kacecha', 'dv_horror'], 'Kevin', KC) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_kacecha,distance=..2,limit=1,sort=nearest] at @s run function canon:k2/acecha/init')
    F('k2/acecha/init', 'function canon:rig/init_common\n' + set_cmd('body', KB) + '\n' + head(KHE) + '\n'
      'scoreboard players operation @s dv.target = #pid dv.tmp\nscoreboard players set @s dv.timer 0\nscoreboard players set @s dv.watch 0\nscoreboard players set @s dv.state 0')
    c.on('second', '''
execute unless entity @e[tag=dv_kacecha] as @a[scores={dv.kno=2},gamemode=!spectator,predicate=canon:en_superficie] at @s if predicate canon:de_noche if predicate canon:azar/1en600 run function canon:k2/acecha/aparecer
execute unless entity @e[tag=dv_kacecha] as @a[scores={dv.kno=3..},gamemode=!spectator,predicate=canon:en_superficie] at @s if predicate canon:de_noche if predicate canon:azar/1en240 run function canon:k2/acecha/aparecer
''')
    F('k2/acecha/aparecer', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players operation #kno dv.tmp = @s dv.kno
scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^3 ^ ^20 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:k2/acecha/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 as @e[type=zombie,tag=dv_kacecha,limit=1] run scoreboard players operation @s dv.mode = #kno dv.tmp
''')
    c.npc('dv_kacecha', 'k2/acecha/tick')
    c.frames('dv_kacecha', 'k2/acecha/frames')
    F('k2/acecha/frames', '''scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2''')
    F('k2/acecha/tick', '''
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..80] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
tag @a[tag=dv_wtgt] add dv_lookers
execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn
execute if entity @a[tag=dv_wtgt] run function canon:k2/acecha/piensa
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('k2/acecha/piensa', '''
execute if score #m2 dv.clock matches 0 run function canon:x/face
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score #seen dv.tmp matches 0 run scoreboard players add @s dv.state 1
execute if score #seen dv.tmp matches 1 if score @s dv.state matches ..99 run scoreboard players set @s dv.state 0
execute if score @s dv.watch matches 20 run playsound canon:gen.voz_kevin_te_veo hostile @a[tag=dv_wtgt] ~ ~ ~ 1.2 1
execute if score @s dv.watch matches 50.. if score @s dv.state matches ..99 run function canon:k2/acecha/se_va
execute if score @s dv.mode matches 4.. if score @s dv.state matches 100.. unless entity @a[tag=dv_wtgt,distance=..1.8] run function canon:x/walk
execute if score @s dv.mode matches 4.. if score @s dv.state matches 100.. unless entity @a[tag=dv_wtgt,distance=..1.8] run function canon:x/walk_slow
execute if score @s dv.state matches 100 run playsound canon:gen.stinger hostile @a[tag=dv_wtgt] ~ ~ ~ 1 1
execute if entity @a[tag=dv_wtgt,distance=..1.8] run function canon:k2/acecha/atrapa
execute if score @s dv.timer matches 1800.. run function canon:k2/acecha/se_va
''')
    F('k2/acecha/se_va', 'tellraw @a[tag=dv_wtgt] {"text":"Kevin ya no está. Pero sabe dónde vives.","color":"#ffb347","italic":true}\n'
      'particle minecraft:large_smoke ~ ~1 ~ 0.3 0.8 0.3 0.02 20 normal\nfunction canon:rig/despawn')
    F('k2/acecha/atrapa', '''
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
damage @a[tag=dv_wtgt,limit=1] 2 minecraft:mob_attack by @s
tellraw @a[tag=dv_wtgt] {"text":"Kevin: ¿Ves? Así se siente cuando te dicen que no. ...Perdón. Me pasé. ¿Fiesta mañana?","color":"#ffd27a","italic":true}
scoreboard players set @a[tag=dv_wtgt] dv.kno 1
function canon:rig/despawn
''')
    F('admin/k2/acecha', 'scoreboard players set @s dv.kno 4\nfunction canon:k2/acecha/aparecer')
    c.admin('/function canon:admin/k2/acecha', 'Kevin enojado te acecha y te persigue')
