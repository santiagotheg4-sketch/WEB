"""Director de eventos canónicos + escondite entre jugadores.

Director: cada atardecer (desde el día 2) puede empezar un EVENTO CANÓNICO nocturno, y cada
amanecer uno diurno. #canon_ev dv.dev = id activo, #canon_t dv.dev = ticks desde que empezó.
Eventos: 1 Luna de sangre (zombies), 2 La niebla, 3 La noche de Diana, 4 Visita de Dani,
6 La noche del Mirón, 12 Apagón.

Escondite: /trigger dv.juego set 1 (con 2+ jugadores). Uno busca (30 s ciego), los demás se esconden;
3 minutos. Si el buscador llega a 2 bloques de alguien, lo encuentra.
"""
from canon.shim import *  # noqa: F401,F403
from canon import shim

EV = {1: ('LUNA DE SANGRE', 'Los muertos tienen hambre esta noche.', '#8b0000'),
      2: ('LA NIEBLA', 'Lo que camina en la niebla conoce tu nombre.', '#cfcfcf'),
      3: ('LA NOCHE DE DIANA', 'Esta noche nadie puede olvidarla.', '#c94a4a'),
      4: ('VISITA DE DANI', 'Alguien despierto te está buscando.', '#9fc3a8'),
      6: ('LA NOCHE DEL MIRÓN', 'Hoy te miran desde todas partes.', '#9a9aa6'),
      12: ('APAGÓN', 'Ninguna luz dura. Usa la cámara.', '#d9a441')}


def build(c):
    shim.use(c)
    c.config('director', 'Eventos canónicos (uno por día o noche)', 1)
    c.objective('dv.juego', 'trigger')
    for n in (2, 3, 8, 10, 20):
        c.const(n)
    c.on('load', '''
execute unless score #canon_ev dv.dev matches -999999..999999 run scoreboard players set #canon_ev dv.dev 0
execute unless score #canon_t dv.dev matches -999999..999999 run scoreboard players set #canon_t dv.dev 0
execute unless score #dir_day dv.dev matches -999999..999999 run scoreboard players set #dir_day dv.dev -1
execute unless score #dir_last dv.dev matches -999999..999999 run scoreboard players set #dir_last dv.dev 0
execute unless score #jg_state dv.dev matches -999999..999999 run scoreboard players set #jg_state dv.dev 0
bossbar add canon:escondite {"text":"Escondite","color":"gold"}
bossbar set canon:escondite color yellow
''')
    c.on('second', '''
execute if score #canon_ev dv.dev matches 1.. run scoreboard players add #canon_t dv.dev 20
execute if score #director dv.cfg matches 1 run function canon:director/second
execute unless score #director dv.cfg matches 1 if score #canon_ev dv.dev matches 1.. run function canon:director/terminar
execute if score #canon_ev dv.dev matches 2 run function canon:director/niebla
execute if score #canon_ev dv.dev matches 6 run function canon:director/miron
execute if score #canon_ev dv.dev matches 12 run function canon:director/apagon
execute unless score #canon_ev dv.dev matches 12 run scoreboard players set #apagon dv.tmp 0
''')
    c.json('data/canon/predicates/vision_nocturna.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'effects': {'minecraft:night_vision': {}}}})
    c.on('player', 'scoreboard players enable @s dv.juego\nexecute if score @s dv.juego matches 1.. run function canon:juego/trigger')
    c.on('tick', 'execute if score #jg_state dv.dev matches 1.. run function canon:juego/tick')
    F('director/second', '''
execute store result score #dt dv.tmp run time query daytime
execute store result score #dd dv.tmp run time query day
execute if score #canon_ev dv.dev matches 1..3 if score #dt dv.tmp matches 0..400 if score #canon_t dv.dev matches 1200.. run function canon:director/terminar
execute if score #canon_ev dv.dev matches 6 if score #dt dv.tmp matches 0..400 if score #canon_t dv.dev matches 1200.. run function canon:director/terminar
execute if score #canon_ev dv.dev matches 12 if score #dt dv.tmp matches 0..400 if score #canon_t dv.dev matches 1200.. run function canon:director/terminar
execute if score #canon_ev dv.dev matches 4 if score #dt dv.tmp matches 12000..12400 run function canon:director/terminar
execute if score #canon_ev dv.dev matches 0 if score #dd dv.tmp matches 2.. unless score #dir_day dv.dev = #dd dv.tmp if score #dt dv.tmp matches 12600..13000 run function canon:director/noche
execute if score #canon_ev dv.dev matches 0 if score #dd dv.tmp matches 2.. unless score #dir_day dv.dev = #dd dv.tmp if score #dt dv.tmp matches 600..1000 run function canon:director/dia
''')
    F('director/noche', '''
scoreboard players operation #dir_day dv.dev = #dd dv.tmp
scoreboard players set #pick dv.tmp 0
execute if predicate canon:azar/50 run function canon:director/elegir_noche
''')
    pick('director/elegir_noche', [
        'scoreboard players set #pick dv.tmp 1',
        'scoreboard players set #pick dv.tmp 2',
        'execute if score #diana dv.cfg matches 1 run scoreboard players set #pick dv.tmp 3',
        'execute if score #miron dv.cfg matches 1 run scoreboard players set #pick dv.tmp 6',
        'scoreboard players set #pick dv.tmp 12',
    ])
    A('director/elegir_noche', 'execute if score #pick dv.tmp = #dir_last dv.dev run scoreboard players set #pick dv.tmp 0\n'
      'execute if score #pick dv.tmp matches 1.. run function canon:director/empezar')
    F('director/dia', '''
scoreboard players operation #dir_day dv.dev = #dd dv.tmp
scoreboard players set #pick dv.tmp 0
execute if score #dani dv.cfg matches 1 if predicate canon:azar/1en5 run scoreboard players set #pick dv.tmp 4
execute if score #pick dv.tmp = #dir_last dv.dev run scoreboard players set #pick dv.tmp 0
execute if score #pick dv.tmp matches 1.. run function canon:director/empezar
''')
    lines = ['scoreboard players operation #canon_ev dv.dev = #pick dv.tmp', 'scoreboard players operation #dir_last dv.dev = #pick dv.tmp',
             'scoreboard players set #canon_t dv.dev 0', 'title @a times 20 80 30']
    for i, (nom, sub, col) in EV.items():
        F(f'director/anuncio/e{i}', f'''
title @a subtitle {jt(sub, col, True)}
title @a title {jt('EVENTO CANÓNICO: ' + nom, col, bold=True)}
tellraw @a ["",{jt('☾ Evento canónico: ', '#d77a8a')},{jt(nom, col, bold=True)},{jt('. ' + sub, 'gray', True)}]
''')
        lines.append(f'execute if score #pick dv.tmp matches {i} run function canon:director/anuncio/e{i}')
    lines += ['playsound canon:fx.stinger master @a ~ ~ ~ 0.8 0.7', 'playsound minecraft:block.bell.use ambient @a ~ ~ ~ 0.6 0.5']
    F('director/empezar', '\n'.join(lines))
    F('director/terminar', '''
scoreboard players set #canon_ev dv.dev 0
scoreboard players set #canon_t dv.dev 0
scoreboard players set #apagon dv.tmp 0
tellraw @a {"text":"☾ El evento canónico terminó. Por ahora.","color":"gray","italic":true}
''')
    F('director/niebla', '''
execute as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s run particle minecraft:white_ash ~ ~1 ~ 8 3 8 0 60 normal @s
execute as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s run particle minecraft:ash ~ ~1 ~ 6 2 6 0 30 normal @s
execute if score #m200 dv.clock matches 0..19 as @a[gamemode=!spectator,predicate=canon:en_superficie] run effect give @s minecraft:darkness 4 0 true
execute as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if predicate canon:azar/1en20 run playsound canon:devota.whisper ambient @s ^ ^ ^-4 0.6 0.7
''')
    F('director/miron', '''
execute if predicate canon:de_noche if predicate canon:azar/1en12 as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s run function canon:director/miron_uno
''')
    F('director/miron_uno', 'scoreboard players set #mironcd dv.dev 0\nfunction canon:miron/try')
    F('director/apagon', '''
scoreboard players set #apagon dv.tmp 1
execute as @a[gamemode=!spectator,predicate=canon:en_superficie] unless predicate canon:vision_nocturna run effect give @s minecraft:darkness 3 0 true
execute as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if predicate canon:azar/1en12 run playsound canon:fx.blackout ambient @s ~ ~ ~ 0.4 1.2
''')
    for i in EV:
        F(f'admin/director/evento_{i}', f'scoreboard players set #pick dv.tmp {i}\nfunction canon:director/empezar')
        c.admin(f'/function canon:admin/director/evento_{i}', f'Evento canónico: {EV[i][0].lower()}')
    F('admin/director/terminar', 'function canon:director/terminar')
    c.admin('/function canon:admin/director/terminar', 'Terminar el evento canónico')

    # ================================================================ ESCONDITE
    F('juego/trigger', '''
scoreboard players set @s dv.juego 0
execute if score #jg_state dv.dev matches 1.. run tellraw @s {"text":"Ya hay un escondite en curso.","color":"gray","italic":true}
execute if score #jg_state dv.dev matches 0 run function canon:juego/empezar
''')
    F('juego/empezar', '''
execute store result score #jn dv.tmp if entity @a[gamemode=!spectator]
execute if score #jn dv.tmp matches ..1 run tellraw @s {"text":"El escondite necesita al menos 2 jugadores.","color":"gray","italic":true}
execute if score #jn dv.tmp matches 2.. run function canon:juego/empezar2
''')
    F('juego/empezar2', '''
tag @a remove dv_jbusca
tag @a remove dv_jesconde
tag @a[gamemode=!spectator,limit=1,sort=random] add dv_jbusca
tag @a[gamemode=!spectator,tag=!dv_jbusca] add dv_jesconde
scoreboard players set #jg_state dv.dev 1
scoreboard players set #jg_t dv.dev 600
bossbar set canon:escondite max 600
bossbar set canon:escondite players @a[tag=dv_jbusca]
bossbar set canon:escondite players @a[gamemode=!spectator]
bossbar set canon:escondite name {"text":"Escóndete... (el buscador está contando)","color":"gold"}
bossbar set canon:escondite visible true
effect give @a[tag=dv_jbusca] minecraft:blindness 31 0 true
effect give @a[tag=dv_jbusca] minecraft:slowness 31 255 true
effect give @a[tag=dv_jbusca] minecraft:jump_boost 31 128 true
title @a[tag=dv_jbusca] times 10 60 10
title @a[tag=dv_jbusca] subtitle {"text":"Cuenta hasta 30. No hagas trampa.","color":"gray"}
title @a[tag=dv_jbusca] title {"text":"TÚ BUSCAS","color":"gold","bold":true}
title @a[tag=dv_jesconde] times 10 60 10
title @a[tag=dv_jesconde] subtitle {"text":"Tienes 30 segundos.","color":"gray"}
title @a[tag=dv_jesconde] title {"text":"¡ESCÓNDETE!","color":"gold","bold":true}
tellraw @a ["",{"text":"☾ Escondite: ","color":"#d77a8a"},{"selector":"@a[tag=dv_jbusca]","color":"gold"},{"text":" busca. Los demás, a esconderse. Si te encuentra a 2 bloques, quedas fuera. Cada 30 segundos, los escondidos suenan.","color":"gray"}]
playsound minecraft:block.note_block.bell master @a ~ ~ ~ 1 1
''')
    F('juego/tick', '''
scoreboard players remove #jg_t dv.dev 1
execute if score #m20 dv.clock matches 0 store result bossbar canon:escondite value run scoreboard players get #jg_t dv.dev
execute unless entity @a[tag=dv_jbusca] run function canon:juego/fin_cancelado
execute if score #jg_state dv.dev matches 1 if score #jg_t dv.dev matches ..0 run function canon:juego/a_buscar
execute if score #jg_state dv.dev matches 2 run function canon:juego/buscando
''')
    F('juego/a_buscar', '''
scoreboard players set #jg_state dv.dev 2
scoreboard players set #jg_t dv.dev 3600
bossbar set canon:escondite max 3600
bossbar set canon:escondite name {"text":"¡A buscar!","color":"red"}
effect clear @a[tag=dv_jbusca] minecraft:blindness
effect clear @a[tag=dv_jbusca] minecraft:slowness
effect clear @a[tag=dv_jbusca] minecraft:jump_boost
title @a times 5 40 10
title @a title {"text":"¡LISTOS O NO, AHÍ VOY!","color":"red","bold":true}
playsound minecraft:entity.wither.ambient master @a ~ ~ ~ 0.4 1.6
''')
    F('juego/buscando', '''
execute as @a[tag=dv_jbusca] at @s as @a[tag=dv_jesconde,distance=..2] run function canon:juego/encontrado
scoreboard players operation #c dv.tmp = #jg_t dv.dev
scoreboard players operation #c dv.tmp %= #600 dv.math
execute if score #c dv.tmp matches 0 as @a[tag=dv_jesconde] at @s run playsound minecraft:block.note_block.chime player @a ~ ~ ~ 1.5 1.4
execute unless entity @a[tag=dv_jesconde] run function canon:juego/gana_buscador
execute if score #jg_t dv.dev matches ..0 run function canon:juego/ganan_escondidos
''')
    c.const(600)
    F('juego/encontrado', '''
tag @s remove dv_jesconde
effect give @s minecraft:glowing 10 0 true
playsound minecraft:entity.experience_orb.pickup master @a ~ ~ ~ 1 0.6
tellraw @a ["",{"text":"☾ ","color":"#d77a8a"},{"selector":"@s","color":"gold"},{"text":" fue encontrado.","color":"gray"}]
title @s times 5 30 10
title @s title {"text":"¡TE ENCONTRARON!","color":"red"}
''')
    F('juego/gana_buscador', '''
tellraw @a ["",{"text":"☾ ","color":"#d77a8a"},{"selector":"@a[tag=dv_jbusca]","color":"gold"},{"text":" encontró a todos. ¡Gana el buscador!","color":"gray"}]
title @a times 10 60 10
title @a title {"text":"GANA EL BUSCADOR","color":"gold"}
function canon:juego/fin
''')
    F('juego/ganan_escondidos', '''
effect give @a[tag=dv_jesconde] minecraft:glowing 8 0 true
tellraw @a ["",{"text":"☾ Se acabó el tiempo. Ganan los escondidos: ","color":"#d77a8a"},{"selector":"@a[tag=dv_jesconde]","color":"gold"}]
title @a times 10 60 10
title @a title {"text":"GANAN LOS ESCONDIDOS","color":"gold"}
function canon:juego/fin
''')
    F('juego/fin_cancelado', 'tellraw @a {"text":"☾ El buscador desapareció. Escondite cancelado.","color":"gray","italic":true}\nfunction canon:juego/fin')
    F('juego/fin', '''
scoreboard players set #jg_state dv.dev 0
bossbar set canon:escondite visible false
effect clear @a[tag=dv_jbusca] minecraft:blindness
effect clear @a[tag=dv_jbusca] minecraft:slowness
effect clear @a[tag=dv_jbusca] minecraft:jump_boost
tag @a remove dv_jbusca
tag @a remove dv_jesconde
tellraw @a ["",{"text":"[Jugar otra ronda]","color":"gold","clickEvent":{"action":"run_command","value":"/trigger dv.juego set 1"}}]
''')
    c.admin('/trigger dv.juego set 1', 'Empezar el escondite (cualquiera puede)')
    F('admin/juego/parar', 'function canon:juego/fin')
    c.admin('/function canon:admin/juego/parar', 'Parar el escondite')
