from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon.models import *  # noqa: F401,F403
import random, json

def models_miron():
    at = Atlas('miron', 41)
    skin = '#1d1b1f'
    c = dict(skin=skin, pants=skin, shoes='#0d0c0e', belt=skin, shirt='#242128', sleeve='#1a181c')
    P = humanoid_parts(at, c, 'thin')
    H = head_parts(at, dict(skin='#2a272d', hair='#0c0b0d'), 'bald')
    r = face_rect(at)
    fe = face_element(at, r, '#2a272d', dict(eyes='glow', mouth='grin', nose=False), 'face')
    head = all_elements(H) + [fe]
    write_model('miron_idle', 'miron', pose(P, 'idle') + head)
    # asomándose: cabeza ladeada (los elementos de la cabeza giran en z)
    tilt = []
    for e in head:
        e = json.loads(json.dumps(e))
        e['rotation'] = {'angle': 22.5, 'axis': 'z', 'origin': [8, 8, 8]}
        tilt.append(e)
    write_model('miron_peek', 'miron', pose(P, 'reach') + tilt)
    at.save()






def gen_miron():
    F('miron/try', '''
execute if score #mironcd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_miron] run function canon:miron/try2
''')
    F('miron/try2', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^20 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^6 ^ ^16 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^-6 ^ ^14 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:miron/spawn_here
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run function canon:miron/announce
''')
    F('miron/announce', '''
scoreboard players set #mironcd dv.dev 420
playsound canon:miron.aparece ambient @s ~ ~ ~ 0.9 0.9
playsound canon:fx.heartbeat ambient @s ~ ~ ~ 0.7 1
execute as @e[type=wolf,tag=dv_luna,distance=..24] at @s run function canon:luna/alarm_watch
''')
    F('miron/spawn_here', rig_summon(['dv_miron'], '???', '#2a272d', head=False, scale=1.3) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_miron,distance=..2,limit=1,sort=nearest] at @s run function canon:miron/init')
    F('miron/init', f'''
function canon:rig/init_common
{set_cmd('body', CMD['miron_idle'])}
scoreboard players operation @s dv.target = #pid dv.tmp
scoreboard players set @s dv.watch 0
''')
    F('miron/tick', '''
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..80] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run tag @a[distance=..48,gamemode=!spectator,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_wtgt] add dv_lookers
execute unless entity @a[tag=dv_wtgt] run function canon:miron/gone
execute if entity @a[tag=dv_wtgt] run function canon:miron/think
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('miron/think', '''
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players add @s dv.timer 1
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #60 dv.math
execute if score #c dv.tmp matches 0..29 run tag @s add dv_mpeek
execute if score #c dv.tmp matches 30.. run tag @s remove dv_mpeek
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #80 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:miron.respira hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.9
execute if score @s dv.watch matches 12.. run function canon:miron/seen_react
execute if entity @a[tag=dv_wtgt,distance=..8] run function canon:miron/close_react
execute if score @s dv.timer matches 300.. run function canon:miron/gone
''')
    pick('miron/seen_react', [
        'playsound canon:miron.estatica hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.8\nfunction canon:miron/gone',
        'playsound canon:miron.estatica hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.6\nfunction canon:miron/gone',
        'playsound canon:miron.grito hostile @a[tag=dv_wtgt] ~ ~ ~ 1 1\nfunction canon:miron/gone',
    ])
    F('miron/close_react', '''
playsound canon:miron.grito master @a[tag=dv_wtgt] ~ ~ ~ 1 1
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
function canon:miron/gone
''')
    F('miron/gone', '''
particle minecraft:large_smoke ~ ~1.2 ~ 0.25 0.8 0.25 0.01 25 normal
function canon:rig/despawn
''')


# =================================================================== CASA BLANCA (sueño de los demás)



def build(c):
    shim.use(c)
    shim.models(['miron_idle', 'miron_peek'], 7320142)
    models_miron()
    c.config('miron', 'El Mirón (algo te mira a lo lejos)', 1)
    for n in (60, 80):
        c.const(n)
    c.on('load', 'execute unless score #mironcd dv.dev matches -999999..999999 run scoreboard players set #mironcd dv.dev 1200')
    c.on('second', '''
execute if score #mironcd dv.dev matches 1.. run scoreboard players remove #mironcd dv.dev 1
execute if score #miron dv.cfg matches 1 as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if predicate canon:azar/1en600 run function canon:miron/try
execute if score #miron dv.cfg matches 1 as @a[gamemode=!spectator,predicate=canon:en_pueblo] at @s if predicate canon:azar/1en250 run function canon:miron/try
execute unless score #miron dv.cfg matches 1 as @e[type=zombie,tag=dv_miron] at @s run function canon:rig/despawn
''')
    c.npc('dv_miron', 'miron/tick')
    c.frames('dv_miron', 'miron/frames')
    F('miron/frames', 'execute if entity @s[tag=dv_mpeek] run scoreboard players set #frame dv.tmp 1')
    gen_miron()
    c.admin('/function canon:admin/spawn/miron', 'Traer al Mirón')
    F('admin/spawn/miron', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^12 run function canon:miron/spawn_here')
