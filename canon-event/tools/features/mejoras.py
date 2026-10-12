"""Canon Event 9: gigantes en el horizonte, Nicolás en las cuevas de muchas formas (ojos en la oscuridad, en el techo,
corriendo, la cámara se gira hacia él), la luna roja se ve y se siente, Diana elige a un nuevo «Juan» si Juan no juega,
Kevin ofrece las catacumbas y esconde tus cosas, y la cámara de Juli la sigue cuando se eleva.
"""
from canon.shim import *  # noqa: F401,F403
from canon import shim


def build(c):
    shim.use(c)
    S = '#sustos dv.cfg matches 1'

    def rig(prefix, tag, name, color, body, hd, tags=(), scale=1.0):
        F(f'{prefix}/summon', rig_summon([tag, *tags], name, color, head=hd is not None, scale=scale) + '\n'
          f'execute as @e[type=zombie,tag=dv_new,tag={tag},distance=..2,limit=1,sort=nearest] at @s run function canon:{prefix}/init')
        F(f'{prefix}/init', 'function canon:rig/init_common\n' + set_cmd('body', body) + '\n' + (head(hd) + '\n' if hd else '') +
          'scoreboard players operation @s dv.target = #pid dv.tmp\nscoreboard players set @s dv.state 0\nscoreboard players set @s dv.timer 0\nscoreboard players set @s dv.watch 0')
    HEAD = '''scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..96] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run tag @a[distance=..64,gamemode=!spectator,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_wtgt] add dv_lookers
'''

    def tick(prefix, tag, body):
        c.npc(tag, f'{prefix}/tick')
        F(f'{prefix}/tick', HEAD + f'execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn\nexecute if entity @a[tag=dv_wtgt] run function canon:{prefix}/piensa\n'
          'tag @a remove dv_wtgt\ntag @a remove dv_lookers')
        F(f'{prefix}/piensa', body)
    MIRA = 'execute as @a[tag=dv_wtgt] at @s anchored eyes facing entity @e[type=zombie,tag={t},limit=1,sort=nearest] eyes run tp @s ~ ~ ~ ~ ~'

    # ================================================================ GIGANTES en el horizonte
    rig('mej/gigante', 'dv_gigante', '???', '#555555', 7321100, 7321102, ['dv_horror'], scale=5.0)
    c.on('second', f'execute if score {S} if predicate canon:de_noche unless entity @e[tag=dv_gigante] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:azar/1en1500 run function canon:mej/gigante/aparecer')
    F('mej/gigante/aparecer', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^-30 ^ ^60 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] rotated ~90 0 run function canon:mej/gigante/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 run tellraw @s {"text":"A lo lejos, entre la niebla, camina algo enorme.","color":"gray","italic":true}
''')
    tick('mej/gigante', 'dv_gigante', '''
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score @s dv.watch matches ..60 if score @s dv.state matches 0 run tp @s ^ ^ ^0.06
execute if score @s dv.watch matches 61.. if score #m4 dv.clock matches 0 run function canon:x/face
execute at @s run function canon:diana/ground
execute if score #m40 dv.clock matches 0 run playsound minecraft:entity.warden.step hostile @a[distance=..160] ~ ~ ~ 10 0.4
execute if entity @a[tag=dv_wtgt,distance=..28] run function canon:mej/gigante/se_va
execute if score @s dv.timer matches 2400.. run function canon:mej/gigante/se_va
''')
    F('mej/gigante/se_va', 'particle minecraft:large_smoke ~ ~6 ~ 2 6 2 0.02 120 normal\nplaysound minecraft:entity.warden.sonic_boom hostile @a[distance=..96] ~ ~ ~ 2 0.4\nfunction canon:rig/despawn')

    # ================================================================ NICOLÁS en las cuevas, de muchas formas
    c.on('second', f'''
execute if score #nicolas dv.cfg matches 1 as @a[gamemode=!spectator,gamemode=!creative] at @s if entity @s[y=-64,dy=104] if predicate canon:oscuro unless entity @e[tag=dv_nicx,distance=..48] if predicate canon:azar/1en120 run function canon:mej/nico/elegir
''')
    c.pick('mej/nico/elegir', ['function canon:mej/nico/ojos', 'function canon:mej/nico/ojos', 'function canon:mej/nico/techo', 'function canon:mej/nico/corre'])
    # ojos en la oscuridad
    F('mej/nico/ojos', '''
scoreboard players set #ok dv.tmp 0
execute rotated ~ 0 positioned ^ ^ ^10 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run summon minecraft:text_display ~ ~1.6 ~ {Tags:["dv_nojos","dv_nicx"],text:'{"text":"• •","color":"white","bold":true}',billboard:"center",brightness:{sky:15,block:15},background:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,1.4f,1.4f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 anchored eyes facing entity @e[type=text_display,tag=dv_nojos,limit=1,sort=nearest] feet run tp @s ~ ~ ~ ~ ~
execute if score #ok dv.tmp matches 1 run playsound canon:nicolas.risa hostile @s ~ ~ ~ 0.4 0.7
''')
    c.on('second', 'execute as @e[type=text_display,tag=dv_nojos] at @s run function canon:mej/nico/ojos_tick')
    F('mej/nico/ojos_tick', 'scoreboard players add @s dv.timer 1\nexecute if entity @a[distance=..5] run function canon:mej/nico/ojos_fin\nexecute if score @s dv.timer matches 12.. run function canon:mej/nico/ojos_fin')
    F('mej/nico/ojos_fin', 'playsound canon:nicolas.risa hostile @a[distance=..16] ~ ~ ~ 0.8 0.6\ntellraw @a[distance=..16] {"text":"Los ojos parpadean una vez. Ya no están.","color":"#8a8a96","italic":true}\nkill @s')
    # Nicolás pegado del techo de la cueva
    rig('mej/nictecho', 'dv_nictecho', 'Nicolás', '#8a8a96', 7320126, 7320132, ['dv_horror', 'dv_nicx'])
    F('mej/nico/techo', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nscoreboard players set #zs dv.tmp 0\nscoreboard players set #ok dv.tmp 0\n'
      'execute anchored eyes positioned ^ ^ ^4 if block ~ ~ ~ #canon:pasable run function canon:mej/nico/techo_buscar')
    F('mej/nico/techo_buscar', '''scoreboard players add #zs dv.tmp 1
execute unless block ~ ~1 ~ #canon:pasable align y positioned ~ ~-0.83 ~ run function canon:mej/nico/techo_poner
execute if score #ok dv.tmp matches 0 if score #zs dv.tmp matches ..6 if block ~ ~1 ~ #canon:pasable positioned ~ ~1 ~ run function canon:mej/nico/techo_buscar''')
    F('mej/nico/techo_poner', 'scoreboard players set #ok dv.tmp 1\nfunction canon:mej/nictecho/summon\nplaysound canon:diana.crack hostile @a[distance=..12] ~ ~1 ~ 0.6 0.9')
    tick('mej/nictecho', 'dv_nictecho', '''
execute on passengers run data merge entity @s {transformation:{left_rotation:[0f,0f,1f,0f]}}
execute if score #m4 dv.clock matches 0 run function canon:x/face
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score @s dv.watch matches 10.. run function canon:mej/nictecho/cae
execute if score @s dv.timer matches 900.. run function canon:rig/despawn
''')
    F('mej/nictecho/cae', MIRA.format(t='dv_nictecho') + '''
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
playsound canon:nicolas.risa master @a[tag=dv_wtgt] ~ ~ ~ 1 0.6
tellraw @a[tag=dv_wtgt] {"text":"Nicolás estaba en el techo de la cueva, boca abajo, mirándote.","color":"#8a8a96","italic":true}
function canon:rig/despawn
''')
    # Nicolás cruza corriendo el túnel
    rig('mej/niccorre', 'dv_niccorre', 'Nicolás', '#8a8a96', 7320126, 7320130, ['dv_horror', 'dv_nicx'])
    F('mej/nico/corre', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nscoreboard players set #ok dv.tmp 0\n'
      'execute rotated ~ 0 positioned ^-5 ^ ^8 run function canon:util/spot_search\n'
      'execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] rotated ~-90 0 run function canon:mej/niccorre/summon\nkill @e[type=marker,tag=dv_spot]')
    tick('mej/niccorre', 'dv_niccorre', '''
execute if block ^ ^ ^0.6 #canon:pasable run tp @s ^ ^ ^0.45
execute at @s run function canon:diana/ground
execute if score @s dv.timer matches 1 run playsound canon:nicolas.risa hostile @a[tag=dv_wtgt] ~ ~ ~ 0.7 1.2
execute if score #m4 dv.clock matches 0 run playsound minecraft:entity.player.small_fall hostile @a[distance=..16] ~ ~ ~ 0.5 0.7
execute if score @s dv.timer matches 40.. run function canon:rig/despawn
''')
    # la cámara se gira hacia Nicolás cuando te mira en la cueva (la aparición del módulo de acecho)
    c.patch('acecho/cueva', lambda s: s if 'mej/nico/mirar' in s else s.rstrip('\n') + '\nschedule function canon:mej/nico/mirar 5t replace\n')
    F('mej/nico/mirar', 'execute as @a at @s if entity @e[type=zombie,tag=dv_as_nicolas,distance=..32] anchored eyes facing entity @e[type=zombie,tag=dv_as_nicolas,limit=1,sort=nearest] eyes run tp @s ~ ~ ~ ~ ~\n'
      'execute as @a at @s if entity @e[type=zombie,tag=dv_as_nicolas2,distance=..32] unless entity @e[type=zombie,tag=dv_as_nicolas,distance=..32] anchored eyes facing entity @e[type=zombie,tag=dv_as_nicolas2,limit=1,sort=nearest] eyes run tp @s ~ ~ ~ ~ ~')

    # ================================================================ LUNA ROJA: que se vea y se sienta
    c.on('second', '''
execute if score #canon_ev dv.dev matches 1 if predicate canon:de_noche as @a[predicate=canon:en_superficie] at @s run function canon:mej/luna_roja
''')
    F('mej/luna_roja', '''
particle minecraft:dust 0.75 0.02 0.02 1.6 ~ ~10 ~ 14 3 14 0 60 normal @s
particle minecraft:dust 0.4 0 0 1.2 ~ ~1 ~ 10 2 10 0 25 normal @s
execute if score #m200 dv.clock matches 0..19 run title @s actionbar {"text":"☾ La luna está roja. Los muertos tienen hambre.","color":"#c41e1e"}
execute if score #m200 dv.clock matches 100..119 run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 0.6 0.5
''')

    # ================================================================ DIANA: si Juan no juega, elige a otro
    c.on('second', '''
execute store result score #mday dv.tmp run time query day
execute if score #diana dv.cfg matches 1 unless score #di_dia dv.dev = #mday dv.tmp unless entity @a[tag=dv_bana] as @a[tag=!dv_santi,gamemode=!spectator,limit=1,sort=random] run function canon:mej/diana_elige
execute if score #diana dv.cfg matches 1 unless score #di_dia dv.dev = #mday dv.tmp unless entity @a[tag=dv_bana] as @a[gamemode=!spectator,limit=1,sort=random] run function canon:mej/diana_elige
''')
    F('mej/diana_elige', '''
scoreboard players operation #di_dia dv.dev = #mday dv.tmp
tag @s add dv_bana
tellraw @s ["",{"text":"Diana (muy cerca de tu oído): ","color":"#c94a4a","bold":true},{"text":"Te pareces a Juan. Caminas como él. Desde hoy, eres mío.","color":"#e8c9a8","italic":true}]
playsound canon:devota.whisper hostile @s ~ ~ ~ 1 0.8
''')

    # ================================================================ KEVIN: las catacumbas y te esconde cosas
    c.patch('kevin/clicked', lambda s: s if 'dv.kv set 13' in s else s.rstrip('\n') + '\nexecute unless score #kev dv.dev matches 1.. run ' +
            menu('@a[tag=dv_talker]', '', '#ffb347', [('¿Vamos a las catacumbas?', '/trigger dv.kv set 13')]) + '\n')
    c.pick('mej/kevin/esconde', [f'''data remove storage canon:tmp robo
data modify storage canon:tmp robo set from entity @s Inventory[{{Slot:{k}b}}]
execute if data storage canon:tmp robo run function canon:mej/kevin/esc{k}''' for k in range(9)])
    for k in range(9):
        F(f'mej/kevin/esc{k}', f'''
item replace entity @s hotbar.{k} with minecraft:air
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-7 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run summon minecraft:item ~ ~0.5 ~ {{Tags:["dv_robado"],Item:{{id:"minecraft:stone",Count:1b}},PickupDelay:0s,Glowing:1b}}
execute unless score #ok dv.tmp matches 1 run summon minecraft:item ~ ~1 ~ {{Tags:["dv_robado"],Item:{{id:"minecraft:stone",Count:1b}},PickupDelay:0s,Glowing:1b}}
kill @e[type=marker,tag=dv_spot]
execute as @e[type=item,tag=dv_robado] run data modify entity @s Item set from storage canon:tmp robo
execute as @e[type=item,tag=dv_robado] run data remove entity @s Item.Slot
tag @e[type=item,tag=dv_robado] remove dv_robado
tellraw @s {{"text":"Kevin: Jajaja, te escondí algo. Está brillando por ahí atrás. Búscalo.","color":"#ffb347","italic":true}}
''')
    c.on('second', 'execute as @e[type=zombie,tag=dv_kevin] at @s as @a[distance=..8,gamemode=!spectator,limit=1,sort=nearest] if predicate canon:azar/1en400 run function canon:mej/kevin/esconde')

    # ================================================================ JULI: la cámara la sigue cuando se eleva
    c.patch('juli/scene_run', lambda s: s if 'mej/juli_look' in s else s.replace(
        'execute as @e[type=marker,tag=dv_jlook] if score @s dv.id = #id dv.tmp run tag @s add dv_jl_me',
        'function canon:mej/juli_look\nexecute as @e[type=marker,tag=dv_jlook] if score @s dv.id = #id dv.tmp run tag @s add dv_jl_me'))
    F('mej/juli_look', '''
execute store result score #by dv.tmp run data get entity @s Pos[1] 1000
scoreboard players set #py dv.tmp -1
execute on passengers if entity @s[tag=dv_head] store result score #py dv.tmp run data get entity @s Pos[1] 1000
execute on passengers if entity @s[tag=dv_head] store result score #hy dv.tmp run data get entity @s transformation.translation[1] 1000
scoreboard players operation #ly dv.tmp = #py dv.tmp
scoreboard players operation #ly dv.tmp += #hy dv.tmp
scoreboard players operation #ly dv.tmp -= #by dv.tmp
scoreboard players add #ly dv.tmp 1550
execute if score #py dv.tmp matches -1 run scoreboard players set #ly dv.tmp 1550
execute unless score #ly dv.tmp matches 600..4500 run scoreboard players set #ly dv.tmp 1550
execute as @e[type=marker,tag=dv_jlook] if score @s dv.id = #id dv.tmp at @e[type=zombie,tag=dv_juli,limit=1,sort=nearest] run function canon:diana/look_marker_move
''')

    # ================================================================ admin
    for nm, body, desc in [('gigante', 'function canon:mej/gigante/aparecer', 'Un gigante en el horizonte'),
                           ('nico_ojos', 'function canon:mej/nico/ojos', 'Ojos de Nicolás en la oscuridad'),
                           ('nico_techo', 'function canon:mej/nico/techo', 'Nicolás en el techo'),
                           ('nico_corre', 'function canon:mej/nico/corre', 'Nicolás cruza corriendo'),
                           ('kevin_esconde', 'function canon:mej/kevin/esconde', 'Kevin te esconde algo')]:
        F(f'admin/mej/{nm}', body)
        c.admin(f'/function canon:admin/mej/{nm}', desc)
