"""Canon Event 8: la Luna falsa, abuelas en el techo, micro-sustos todo el tiempo, chat falso, la hora muerta (3:11),
el teléfono, aldeanos raros, el pozo, espantapájaros, el árbol de los colgados, la Llorona, el cuarto que no estaba,
ítems nuevos (ojo de vidrio, campanita, vela negra, collar de Luna, cintas VHS, llave oxidada, ectoplasma),
botín del mod en los cofres del mundo, crafteos difíciles, sustos al abrir cofres y animales que se defienden.
"""
from PIL import Image, ImageDraw
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon import skins as SK
from canon.ctx import item_nbt, loot_item

ESPANTA = dict(skin='#c8a86a', hair='#d8b84a', hair_style='messy', eyes='#000000', brows='#5a4a2a', lips='#3a2a1a', top='#7a3a2a',
               top_style='long', pants='#3a4a6a', shoes='#4a3a2a', extras=['cap'], cap='#6a5a3a')
LLORONA = dict(skin='#e8e4e0', hair='#0a0a0a', hair_style='long', eyes='#000000', brows='#0a0a0a', lips='#8a8a8a', top='#f0f0f0',
               top_style='dress', pants='#f0f0f0', pants_style='long_dress', shoes='#f0f0f0', extras=['dark_circles'])
NUEVOS = [  # id, nombre, color, lore, cmd, base, colores icono, receta (None = solo en cofres)
    ('ojo_vidrio', 'Ojo de vidrio', '#bfe3f2', ['Clic derecho: ves lo que siempre estuvo ahí.'], 7311130, 'carrot_on_a_stick', ((230, 240, 245), (40, 90, 160)),
     ['glass', 'ender_eye', 'ghast_tear', 'phantom_membrane']),
    ('campanita', 'Campanita', '#f2d36b', ['Clic derecho: lo que te acecha se aleja y se congela.'], 7311131, 'carrot_on_a_stick', ((230, 190, 70), (120, 80, 20)),
     ['gold_ingot', 'gold_ingot', 'amethyst_shard', 'phantom_membrane']),
    ('vela_negra', 'Vela negra', '#5a5a5a', ['Clic derecho: la prendes. Atrae cosas.', 'Más sustos, mejores premios.'], 7311132, 'carrot_on_a_stick',
     ((30, 30, 30), (255, 120, 40)), ['black_candle', 'soul_sand', 'phantom_membrane']),
    ('collar_luna', 'Collar de Luna', '#ffd27a', ['Clic derecho: ¿esa Luna es la de verdad?'], 7311133, 'carrot_on_a_stick', ((200, 60, 60), (255, 210, 122)),
     ['string', 'gold_nugget', 'bone', 'phantom_membrane']),
    ('cinta', 'Cinta VHS', '#9a9aa8', ['Clic derecho cerca de un televisor del mod.'], 7311134, 'carrot_on_a_stick', ((40, 40, 45), (200, 200, 210)), None),
    ('ectoplasma', 'Ectoplasma', '#8fe0b0', ['Lo que queda de un espíritu.', 'Sirve como membrana de phantom en los crafteos.'], 7311135, 'phantom_membrane',
     ((140, 224, 176), (220, 255, 235)), None),
    ('llave', 'Llave oxidada', '#a8704a', ['Abre cofres cerrados y cuartos que no existen.'], 7311136, 'tripwire_hook', ((168, 112, 74), (90, 50, 30)),
     ['iron_ingot', 'copper_ingot', 'phantom_membrane']),
]
CINTAS = ['Cumpleaños de Juan, marzo. Todos cantan. En la ventana de atrás, una chica pálida canta también. Nadie la invitó.',
          'El puente, 3:11 a.m. La cámara tiembla. Un muchacho de chaqueta gris mira el río. Alguien dice «Juan, vuelve». No es la voz de Valery.',
          'La casa de la abuela. Tres niños juegan en el patio. Uno mira a la cámara y deja de sonreír. La cinta se corta.',
          'La fiesta de Kevin. Todos bailan. En el fondo, entre los árboles, algo muy alto se agacha para mirar.',
          'El cuarto de Juli. Juli duerme. La cámara se acerca. Juli abre los ojos: «Apágala. Ella está mirando por la cámara».',
          'Negro. Una voz: «Si estás viendo esto, ya sabes dónde vives». Sale tu casa desde afuera, de noche. Hay alguien en tu ventana.']
PACIFICOS = ['cow', 'mooshroom', 'sheep', 'pig', 'chicken', 'rabbit', 'horse', 'donkey', 'mule', 'camel', 'sniffer', 'fox', 'ocelot', 'turtle', 'frog']
ANIMALES = ['cow', 'mooshroom', 'sheep', 'pig', 'chicken', 'horse', 'donkey', 'villager', 'goat', 'rabbit']


def icon(path, c1, c2):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 13, 13], fill=c1 + (255,), outline=tuple(max(0, v - 60) for v in c1) + (255,))
    d.ellipse([6, 6, 9, 9], fill=c2 + (255,))
    im.save(path)


def build(c):
    shim.use(c)
    c.config('sustos', 'Sustos nuevos (micro-sustos, Luna falsa, Llorona...)', 1)
    for o in ('dv.vnf', 'dv.pozo', 'dv.cuarto'):
        c.objective(o)
    c.objective('dv.cofreab', 'minecraft.custom:minecraft.open_chest')
    c.json('data/canon/tags/entity_types/pacificos.json', {'values': [f'minecraft:{x}' for x in PACIFICOS]})
    c.json('data/canon/tags/entity_types/animales.json', {'values': [f'minecraft:{x}' for x in ANIMALES]})
    c.json('data/canon/tags/blocks/cofres_mundo.json', {'values': ['minecraft:chest', 'minecraft:barrel', 'minecraft:trapped_chest']})
    c.json('data/canon/predicates/bosque.json', {'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:location_check', 'predicate': {'biome': f'minecraft:{b}'}} for b in
        ('forest', 'dark_forest', 'birch_forest', 'old_growth_birch_forest', 'flower_forest', 'taiga', 'old_growth_pine_taiga', 'old_growth_spruce_taiga')]})
    S = '#sustos dv.cfg matches 1'
    c.json('data/canon/predicates/azar/1en90.json', {'condition': 'minecraft:random_chance', 'chance': round(1 / 90, 6)})

    # ================================================================ ítems nuevos
    for iid, nom, col, lore, cmd, base, (c1, c2), rec in NUEVOS:
        icon(c.path(f'assets/canon/textures/item/s_{iid}.png'), c1, c2)
        parent = 'minecraft:item/handheld_rod' if base == 'carrot_on_a_stick' else 'minecraft:item/generated'
        c.json(f'assets/canon/models/item/s_{iid}.json', {'parent': parent, 'textures': {'layer0': f'canon:item/s_{iid}'}})
        c.item_model(base, cmd, f'canon:item/s_{iid}')
        extra = 'Unbreakable:1b' if base == 'carrot_on_a_stick' else ''
        if iid == 'cinta':
            for n in range(1, 7):
                c.json(f'data/canon/loot_tables/sus/cinta{n}.json', loot_item(base, item_nbt('cinta', f'Cinta VHS #{n}', col, lore, cmd, f'Unbreakable:1b,cinta:{n}')))
        else:
            c.json(f'data/canon/loot_tables/sus/{iid}.json', loot_item(base, item_nbt(iid, nom, col, lore, cmd, extra)))
        if rec:
            c.json(f'data/canon/recipes/s_{iid}.json', {'type': 'minecraft:crafting_shapeless', 'category': 'misc',
                                                       'ingredients': [{'item': 'minecraft:' + x} for x in rec], 'result': {'item': 'minecraft:knowledge_book', 'count': 1}})
            c.json(f'data/canon/advancements/sus/receta_{iid}.json', {'criteria': {'c': {'trigger': 'minecraft:recipe_crafted', 'conditions': {
                'recipe_id': f'canon:s_{iid}'}}}, 'rewards': {'function': f'canon:sus/craft/{iid}'}})
            F(f'sus/craft/{iid}', f'clear @s minecraft:knowledge_book 1\nloot give @s loot canon:sus/{iid}\nadvancement revoke @s only canon:sus/receta_{iid}')
        if base == 'carrot_on_a_stick':
            c.use_item(iid, f'sus/{iid}/usar', cooldown=True)
    c.on('player', 'execute unless entity @s[tag=dv_srecetas] run function canon:sus/recetas')
    F('sus/recetas', 'tag @s add dv_srecetas\n' + '\n'.join(f'recipe give @s canon:s_{x[0]}' for x in NUEVOS if x[7]))
    # ectoplasma: lo sueltan los espíritus al espantarlos
    c.patch('camara/espanta', lambda s: s if 'sus/ectoplasma' in s else 'execute if predicate canon:azar/1en2 run loot spawn ~ ~1 ~ loot canon:sus/ectoplasma\n' + s)
    # usos
    F('sus/ojo_vidrio/usar', '''
scoreboard players set @s dv.cool 300
playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.6
effect give @e[tag=dv_horror,distance=..64] minecraft:glowing 15 0 true
effect give @e[tag=dv_asomo,distance=..64] minecraft:glowing 15 0 true
effect give @e[tag=dv_lfalsa,distance=..64] minecraft:glowing 15 0 true
effect give @e[type=wolf,tag=dv_luna_atada,distance=..96] minecraft:glowing 15 0 true
scoreboard players operation #pid dv.tmp = @s dv.pid
function canon:acecho/elegir_quien
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^7 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:acecho/aparecer
kill @e[type=marker,tag=dv_spot]
tellraw @s {"text":"Por el ojo de vidrio ves cosas que siempre estuvieron ahí.","color":"#bfe3f2","italic":true}
''')
    F('sus/campanita/usar', '''
scoreboard players set @s dv.cool 200
playsound minecraft:block.bell.use player @a[distance=..24] ~ ~ ~ 1 2
particle minecraft:end_rod ~ ~1 ~ 3 1 3 0.02 40 normal
execute as @e[tag=dv_horror,tag=!dv_jefe,distance=..20] at @s run function canon:camara/espanta
effect give @e[type=#canon:hostiles,distance=..16] minecraft:slowness 5 9 true
execute as @e[type=zombie,tag=dv_jefe,distance=..20] run scoreboard players set @s dv.jstun 100
tellraw @s {"text":"La campanita suena. Todo se queda quieto.","color":"#f2d36b","italic":true}
''')
    F('sus/vela_negra/usar', '''
scoreboard players set @s dv.cool 100
clear @s minecraft:carrot_on_a_stick{canon:{id:"vela_negra"}} 1
setblock ~ ~ ~ minecraft:black_candle[lit=true,candles=1] keep
summon minecraft:marker ~ ~ ~ {Tags:["dv_vnegra"]}
playsound minecraft:item.flintandsteel.use player @s ~ ~ ~ 1 0.5
tellraw @s {"text":"La vela negra prende sola. Algo la vio desde lejos.","color":"#8a8a8a","italic":true}
''')
    F('sus/collar_luna/usar', '''
scoreboard players set @s dv.cool 40
execute if entity @e[tag=dv_lfalsa,distance=..48] run tellraw @s {"text":"El collar se pone frío y rojo. Esa no es Luna.","color":"#c94a4a","italic":true}
execute unless entity @e[tag=dv_lfalsa,distance=..48] run tellraw @s {"text":"El collar está tibio. Luna es Luna.","color":"#ffd27a","italic":true}
execute if entity @e[type=wolf,tag=dv_luna_atada] anchored eyes facing entity @e[type=wolf,tag=dv_luna_atada,limit=1] eyes run tp @s ~ ~ ~ ~ ~
execute if entity @e[type=wolf,tag=dv_luna_atada] run tellraw @s {"text":"El collar tira de tu mano hacia allá. Luna está por ese lado.","color":"#ffd27a","italic":true}
playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1
''')
    cin = ['scoreboard players set @s dv.cool 100', 'execute store result score #cn dv.tmp run data get entity @s SelectedItem.tag.cinta',
           'execute unless entity @e[type=item_display,tag=dv_mueble_tv,distance=..6] run tellraw @s {"text":"Necesitas un televisor del mod cerca para ver la cinta.","color":"gray","italic":true}']
    for n, t in enumerate(CINTAS, 1):
        F(f'sus/cinta/c{n}', f'playsound canon:items.radio_static player @a[distance=..12] ~ ~ ~ 1 0.8\ntitle @a[distance=..12] times 5 60 20\n'
          f'title @a[distance=..12] title {jt(f"CINTA #{n}", "#9a9aa8", bold=True)}\ntellraw @a[distance=..12] ["",{jt(f"[Cinta #{n}] ", "#9a9aa8", bold=True)},{jt(t, "#d0d0d8", True)}]'
          + ('\nschedule function canon:sus/cinta/susto 100t' if n == 6 else ''))
        cin.append(f'execute if entity @e[type=item_display,tag=dv_mueble_tv,distance=..6] if score #cn dv.tmp matches {n} run function canon:sus/cinta/c{n}')
    F('sus/cinta/usar', '\n'.join(cin))
    F('sus/cinta/susto', 'execute as @a at @s if entity @e[type=item_display,tag=dv_mueble_tv,distance=..12] run function canon:x/jumpscare')

    # ================================================================ botín del mod en cofres del mundo
    def lt(name, w):
        return {'type': 'minecraft:loot_table', 'name': name, 'weight': w}
    pool = [lt('canon:items/billete', 25), lt('canon:sus/ectoplasma', 12), lt('canon:sus/llave', 6), lt('canon:rel/foto_vieja', 4),
            lt('canon:extras/crucifijo', 3), lt('canon:extras/arepa', 4), lt('canon:extras/chocolate', 4), lt('canon:sus/collar_luna', 3),
            lt('canon:sus/ojo_vidrio', 2), lt('canon:sus/campanita', 2), lt('canon:sus/vela_negra', 3)]
    pool += [lt(f'canon:sus/cinta{n}', 2) for n in range(1, 7)] + [lt(f'canon:rel/pag/p{n}', 1) for n in range(1, 14)]
    pool += [lt(f'canon:para/{x}', 2) for x in ('ouija', 'velas', 'espejo', 'radio_esp', 'emf', 'muneca', 'caja_musica', 'sal', 'agua_bendita', 'libro_inv', 'grabadora')]
    c.json('data/canon/loot_tables/sus/cofre.json', {'type': 'minecraft:chest', 'pools': [{'rolls': {'type': 'minecraft:uniform', 'min': 1, 'max': 2}, 'entries': pool}]})
    c.json('data/canon/loot_tables/sus/pozo.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [
        lt('canon:items/billete', 10), lt('canon:sus/ectoplasma', 6), lt('canon:para/muneca', 2), lt('canon:sus/ojo_vidrio', 1),
        {'type': 'minecraft:item', 'name': 'minecraft:rotten_flesh', 'weight': 6}, {'type': 'minecraft:item', 'name': 'minecraft:emerald', 'weight': 4},
        {'type': 'minecraft:item', 'name': 'minecraft:bone', 'weight': 5}, lt('canon:rel/pag/p4', 1)]}]})
    ls = []
    for dx in range(-6, 7):
        for dy in range(-3, 4):
            for dz in range(-6, 7):
                ls.append(f'execute positioned ~{dx} ~{dy} ~{dz} if block ~ ~ ~ #canon:cofres_mundo if data block ~ ~ ~ LootTable unless data block ~ ~ ~ Items[0] run loot insert ~ ~ ~ loot canon:sus/cofre')
    F('sus/cofres_scan', '\n'.join(ls))
    c.on('second', 'execute if score #m200 dv.clock matches 0..19 as @a[gamemode=!spectator] at @s run function canon:sus/cofres_scan')
    # susto al abrir cofres de noche
    c.on('player', f'execute if score @s dv.cofreab matches 1.. run function canon:sus/cofre_abre')
    F('sus/cofre_abre', f'scoreboard players set @s dv.cofreab 0\nexecute if score {S} if predicate canon:de_noche if predicate canon:azar/1en40 run function canon:sus/screamer')
    F('sus/screamer', 'function canon:x/jumpscare\nplaysound canon:diana.scream master @s ~ ~ ~ 1 1.2\nscoreboard players add @s dv.miedo 20')

    # ================================================================ micro-sustos todo el tiempo
    c.on('second', f'''
execute if score {S} as @a[gamemode=!spectator] at @s if predicate canon:azar/1en150 run function canon:sus/micro
execute if score {S} as @e[type=marker,tag=dv_vnegra] at @s as @a[distance=..16,gamemode=!spectator] at @s if predicate canon:azar/1en15 run function canon:sus/micro
execute if score {S} as @a[gamemode=!spectator] at @s if predicate canon:azar/1en3000 run function canon:sus/screamer
execute if score {S} if predicate canon:azar/1en1800 run function canon:sus/chat_falso
''')
    c.pick('sus/micro', [
        'playsound canon:diana.step hostile @s ^ ^ ^-3 0.5 1\nplaysound canon:diana.step hostile @s ^ ^ ^-2.5 0.4 0.95',
        'tellraw @s ["",{"text":"<???> ","color":"dark_gray"},{"selector":"@s","color":"dark_gray"}]',
        'playsound canon:diana.breath hostile @s ^ ^ ^-0.7 0.35 1',
        'playsound minecraft:entity.zombie.attack_wooden_door hostile @s ^ ^ ^-14 0.5 0.7',
        'playsound minecraft:block.chest.open block @s ^4 ^ ^-4 0.7 0.7',
        'playsound canon:devota.giggle hostile @s ^ ^ ^-6 0.4 1.4',
        'playsound canon:devota.whisper hostile @s ^-1 ^ ^ 0.5 0.8',
        'title @s actionbar {"text":"...¿me oyes?...","color":"dark_gray","italic":true}',
        'playsound minecraft:block.glass.hit block @s ^3 ^1 ^-3 0.6 0.6',
        'tellraw @a {"translate":"chat.type.advancement.task","with":[{"selector":"@s"},{"text":"[Te vi]","color":"green"}]}',
        'effect give @s minecraft:darkness 2 0 true',
        'playsound minecraft:entity.wolf.howl ambient @s ^ ^ ^-30 0.5 0.7'])
    c.pick('sus/chat_falso', [
        'tellraw @a {"translate":"multiplayer.player.joined","with":["Juan"],"color":"yellow"}',
        'tellraw @a {"translate":"multiplayer.player.joined","with":["Diana"],"color":"yellow"}',
        'tellraw @a {"translate":"multiplayer.player.joined","with":["tantanto4"],"color":"yellow"}',
        'tellraw @a {"translate":"multiplayer.player.left","with":["Juli"],"color":"yellow"}',
        'tellraw @a {"translate":"death.attack.mob","with":[{"selector":"@r"},"Diana"]}',
        'tellraw @a ["",{"text":"<Juan> "},{"text":"hace frío en el río"}]'])

    # ================================================================ la hora muerta (3:11 = 21183)
    c.on('second', f'''
execute store result score #sd dv.tmp run time query daytime
execute store result score #sday dv.tmp run time query day
execute if score {S} if score #sd dv.tmp matches 21183..21240 unless score #hm_dia dv.dev = #sday dv.tmp run function canon:sus/hora_muerta
''')
    F('sus/hora_muerta', '''
scoreboard players operation #hm_dia dv.dev = #sday dv.tmp
title @a times 10 60 20
title @a title {"text":"3:11","color":"#c94a4a"}
playsound minecraft:block.bell.use ambient @a ~ ~ ~ 0.6 0.4
effect give @a minecraft:darkness 6 0 true
execute as @a at @s as @e[type=#canon:animales,tag=!dv_brain,distance=..40] run function canon:sus/hm_quieto
execute as @a[predicate=canon:en_superficie] at @s run function canon:sus/hm_figura
schedule function canon:sus/hora_muerta_fin 300t
''')
    F('sus/hm_quieto', 'tag @s add dv_hm\ndata merge entity @s {NoAI:1b}\nexecute at @s run tp @s ~ ~ ~ 180 0')
    F('sus/hora_muerta_fin', 'execute as @e[tag=dv_hm] run data merge entity @s {NoAI:0b}\ntag @e[tag=dv_hm] remove dv_hm')
    F('sus/hm_figura', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nscoreboard players set #quien dv.tmp 2\nscoreboard players set #ok dv.tmp 0\n'
      'execute positioned ^-10 ^ ^16 run function canon:util/spot_search\nexecute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:acecho/aparecer\n'
      'kill @e[type=marker,tag=dv_spot]\ntellraw @s {"text":"Todos los animales miran hacia el mismo lado. Algo está cruzando.","color":"gray","italic":true}')

    # ================================================================ teléfono
    c.on('second', f'''
execute if score {S} if predicate canon:de_noche as @a[gamemode=!spectator] at @s as @e[type=item_display,tag=dv_mueble_telefono,tag=!dv_tel_suena,distance=..12,limit=1] if predicate canon:azar/1en500 run tag @s add dv_tel_suena
execute as @e[type=item_display,tag=dv_tel_suena] at @s run function canon:sus/tel/sonando
''')
    F('sus/tel/sonando', '''
scoreboard players add @s dv.timer 1
playsound minecraft:block.note_block.bell block @a[distance=..20] ~ ~ ~ 1 1.6
execute if entity @a[distance=..2] run function canon:sus/tel/contesta
execute if score @s dv.timer matches 20.. run tellraw @a[distance=..16] {"text":"Dejó de sonar. En el contestador solo se oye a alguien respirando.","color":"gray","italic":true}
execute if score @s dv.timer matches 20.. run function canon:sus/tel/fin
''')
    F('sus/tel/fin', 'tag @s remove dv_tel_suena\nscoreboard players set @s dv.timer 0')
    c.pick('sus/tel/voz', [f'tellraw @a[distance=..3] ["",{jt("(teléfono) " + q + ": ", "#c9a46a", bold=True)},{jt(t, "#e8c9a8", True)}]' for q, t in [
        ('Juli', '¿Santi? Te escucho desde el sueño. No te duermas todavía.'), ('Diana', 'Estoy afuera. No. Mejor: estoy adentro.'),
        ('Juan', 'Valery... ¿estás ahí? Hace frío en el río.'), ('Abuela Esmeralda', 'Mijito, ¿dejó la puerta abierta? Porque yo ya entré.'),
        ('???', 'Te veo. Tienes puesta la misma ropa de ayer.'), ('Kevin', 'Jajaja te asusté. ...Kevin está a mi lado. No soy Kevin.')]])
    F('sus/tel/contesta', 'function canon:sus/tel/voz\nplaysound canon:items.radio_static player @a[distance=..3] ~ ~ ~ 0.6 1\nfunction canon:sus/tel/fin')

    # ================================================================ aldeanos raros + pozo
    c.on('second', f'''
execute if score {S} if predicate canon:de_noche as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s as @e[type=villager,tag=!dv_vraro,distance=..24,limit=1,sort=random] if predicate canon:azar/1en240 run function canon:sus/aldeano/raro
execute as @e[type=villager,tag=dv_vraro] at @s run function canon:sus/aldeano/tick
execute if score {S} as @a[x_rotation=45..90,gamemode=!spectator] at @s unless score @s dv.pozo matches 1.. if entity @e[type=villager,distance=..48] anchored eyes positioned ^ ^ ^3 if block ~ ~ ~ minecraft:water if predicate canon:azar/1en8 run function canon:sus/pozo/cara
scoreboard players remove @a[scores={{dv.pozo=1..}}] dv.pozo 1
execute as @e[type=item] at @s if block ~ ~ ~ minecraft:water if entity @e[type=villager,distance=..40] run function canon:sus/pozo/item
''')
    F('sus/aldeano/raro', 'tag @s add dv_vraro\nscoreboard players set @s dv.timer 0\ndata merge entity @s {NoAI:1b}')
    F('sus/aldeano/tick', '''
scoreboard players add @s dv.timer 1
tag @a remove dv_lookers
tag @a[distance=..24,limit=1,sort=nearest] add dv_lookers
function canon:x/seen
execute facing entity @a[tag=dv_lookers,limit=1] eyes run tp @s ~ ~ ~ ~ ~
execute if score #seen dv.tmp matches 0 if entity @a[tag=dv_lookers,distance=3..] facing entity @a[tag=dv_lookers,limit=1] feet rotated ~ 0 positioned ^ ^ ^1 if block ~ ~ ~ #canon:pasable run tp @s ~ ~ ~
execute if score @s dv.timer matches 5 run playsound canon:devota.whisper neutral @a[tag=dv_lookers] ~ ~ ~ 0.6 0.6
execute if score @s dv.timer matches 5 run tellraw @a[tag=dv_lookers] ["",{"text":"Un aldeano susurra: «","color":"#8a8a96","italic":true},{"selector":"@a[tag=dv_lookers]","color":"#8a8a96"},{"text":"...»","color":"#8a8a96","italic":true}]
tag @a remove dv_lookers
execute if score @s dv.timer matches 30.. run function canon:sus/aldeano/normal
''')
    F('sus/aldeano/normal', 'tag @s remove dv_vraro\ndata merge entity @s {NoAI:0b}')
    F('sus/pozo/cara', '''
scoreboard players set @s dv.pozo 120
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #quien dv.tmp 1
execute anchored eyes positioned ^ ^ ^3 positioned ~ ~-1.4 ~ run function canon:acecho/aparecer
playsound minecraft:entity.drowned.ambient_water hostile @s ~ ~-3 ~ 1 0.6
tellraw @s {"text":"Desde el fondo del pozo, una cara te está mirando.","color":"#c94a4a","italic":true}
''')
    c.json('data/canon/tags/blocks/pozo_borde.json', {'values': ['minecraft:cobblestone', 'minecraft:mossy_cobblestone', 'minecraft:stone_bricks',
                                                                 'minecraft:mossy_stone_bricks', 'minecraft:sandstone', 'minecraft:cut_sandstone', 'minecraft:smooth_sandstone']})
    F('sus/pozo/item', 'scoreboard players set #pz dv.tmp 0\n' + '\n'.join(f'execute if block {p} #canon:pozo_borde run scoreboard players set #pz dv.tmp 1'
                                                                         for p in ('~1 ~ ~', '~-1 ~ ~', '~ ~ ~1', '~ ~ ~-1', '~2 ~ ~', '~-2 ~ ~', '~ ~ ~2', '~ ~ ~-2')) +
      '\nexecute if score #pz dv.tmp matches 1 if block ~ ~-1 ~ minecraft:water run scoreboard players add @s dv.timer 1\nexecute if score @s dv.timer matches 3.. run function canon:sus/pozo/devuelve')
    F('sus/pozo/devuelve', 'loot spawn ~ ~1.5 ~ loot canon:sus/pozo\nplaysound minecraft:entity.generic.splash block @a[distance=..12] ~ ~ ~ 1 0.6\n'
      'tellraw @a[distance=..8] {"text":"El agua se tragó lo que tiraste... y te devolvió otra cosa.","color":"#8fb3c9","italic":true}\nkill @s')

    # ================================================================ modelos nuevos y rigs
    def char(prefix, cfg, poses, exprs, start):
        b, h = SK.build_character(prefix, cfg, c.out, poses, exprs)
        shim.models(b + h, start)
    char('espanta', ESPANTA, ('idle', 'brazos'), [('creepy', 'creepy')], 7321130)
    char('llorona', LLORONA, ('idle', 'walk_a', 'walk_b', 'cover', 'reach'), [('llora', 'cry'), ('vacia', 'void')], 7321140)
    K = shim.CMD

    def rig(prefix, tag, name, color, body, hd, tags=(), scale=1.0, base='zombie'):
        F(f'{prefix}/summon', rig_summon([tag, *tags], name, color, head=hd is not None, scale=scale, base=base) + '\n'
          f'execute as @e[type={base},tag=dv_new,tag={tag},distance=..2,limit=1,sort=nearest] at @s run function canon:{prefix}/init')
        F(f'{prefix}/init', 'function canon:rig/init_common\n' + set_cmd('body', body) + '\n' + (head(hd) + '\n' if hd else '') +
          'scoreboard players operation @s dv.target = #pid dv.tmp\nscoreboard players set @s dv.state 0\nscoreboard players set @s dv.timer 0\nscoreboard players set @s dv.watch 0')
    HEAD = '''scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..64] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run tag @a[distance=..48,gamemode=!spectator,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_wtgt] add dv_lookers
'''

    def tick(prefix, tag, body):
        c.npc(tag, f'{prefix}/tick')
        F(f'{prefix}/tick', HEAD + f'execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn\nexecute if entity @a[tag=dv_wtgt] run function canon:{prefix}/piensa\n'
          'tag @a remove dv_wtgt\ntag @a remove dv_lookers')
        F(f'{prefix}/piensa', body)

    def spot(fn, pos='~ ~ ~'):
        return (f'scoreboard players set #ok dv.tmp 0\nexecute positioned {pos} run function canon:util/spot_search\n'
                f'execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:{fn}\nkill @e[type=marker,tag=dv_spot]')

    # ================================================================ LA LUNA FALSA
    rig('sus/lfalsa', 'dv_lfalsa', 'Luna', '#ffd27a', 7320104, None, ['dv_horror'], base='wolf')
    rig('sus/lbicho', 'dv_lbicho', '???', '#8b0000', 7320144, None, ['dv_horror'], scale=2.2)
    c.patch('tick', lambda s: s.replace('as @e[type=wolf,tag=dv_luna] at @s run function canon:luna/tick', 'as @e[type=wolf,tag=dv_luna,tag=!dv_luna_atada] at @s run function canon:luna/tick'))
    c.on('second', f'''
execute if score {S} if predicate canon:de_noche unless entity @e[tag=dv_lfalsa] unless entity @e[tag=dv_lbicho] unless entity @e[type=wolf,tag=dv_luna_atada] as @e[type=wolf,tag=dv_luna] at @s if entity @a[distance=6..20,gamemode=!spectator,predicate=canon:en_superficie] if predicate canon:azar/1en1200 run function canon:sus/luna/cambio
execute as @e[type=wolf,tag=dv_luna_atada] at @s run function canon:sus/luna/atada
''')
    F('sus/luna/cambio', '''
scoreboard players operation #pid dv.tmp = @a[distance=..20,gamemode=!spectator,limit=1,sort=nearest] dv.pid
function canon:sus/lfalsa/summon
tag @s add dv_luna_atada
scoreboard players set #ok dv.tmp 0
execute rotated ~180 0 positioned ^ ^ ^220 run spreadplayers ~ ~ 0 30 false @s
execute at @s run forceload add ~ ~
execute on passengers run data merge entity @s {Glowing:1b,glow_color_override:16765562}
''')
    F('sus/luna/atada', '''
execute if score #m200 dv.clock matches 0..19 run playsound minecraft:entity.wolf.whine neutral @a[distance=..320] ~ ~ ~ 20 1.2
execute if score #m200 dv.clock matches 100..119 run playsound minecraft:entity.wolf.ambient neutral @a[distance=..320] ~ ~ ~ 20 1
execute if entity @a[distance=..3,gamemode=!spectator] run function canon:sus/luna/rescate
''')
    F('sus/luna/rescate', '''
forceload remove ~ ~
tag @s remove dv_luna_atada
execute on passengers run data merge entity @s {Glowing:0b}
execute as @e[tag=dv_lfalsa] at @s run function canon:sus/lfalsa/grita
execute as @e[tag=dv_lbicho] at @s run function canon:sus/lfalsa/grita
title @a[distance=..16] times 10 50 20
title @a[distance=..16] title {"text":"¡ES LUNA!","color":"#ffd27a","bold":true}
tellraw @a {"text":"Encontraron a la Luna de verdad, amarrada y temblando. Lo que los seguía no era ella.","color":"#ffd27a","italic":true}
playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.3
''')
    F('sus/lfalsa/grita', 'playsound canon:diana.scream hostile @a[distance=..48] ~ ~ ~ 1 0.5\nparticle minecraft:large_smoke ~ ~1 ~ 0.5 1 0.5 0.05 40 normal\nfunction canon:rig/despawn')
    tick('sus/lfalsa', 'dv_lfalsa', '''
execute unless entity @a[tag=dv_wtgt,distance=..3] if entity @a[tag=dv_wtgt,distance=..30] run function canon:x/walk_slow
execute if entity @a[tag=dv_wtgt,distance=30..] at @a[tag=dv_wtgt,limit=1] rotated ~ 0 run tp @s ^ ^ ^-3
execute if score @s dv.timer matches 400 run tellraw @a[tag=dv_wtgt] {"text":"Luna no mueve la cola. Se quedó mirando la pared. A lo lejos, otro perro ladra igual que ella.","color":"gray","italic":true}
execute if score @s dv.timer matches 900 run playsound minecraft:entity.wolf.growl neutral @a[tag=dv_wtgt] ~ ~ ~ 1 0.5
execute if score @s dv.timer matches 900 run tellraw @a[tag=dv_wtgt] {"text":"Luna te gruñe. Luna nunca te gruñe.","color":"#c94a4a","italic":true}
execute if score @s dv.timer matches 3600.. if entity @a[tag=dv_wtgt,distance=..5] if predicate canon:oscuro run function canon:sus/lfalsa/transforma
execute if score @s dv.timer matches 9000.. if entity @a[tag=dv_wtgt,distance=..8] run function canon:sus/lfalsa/transforma
''')
    F('sus/lfalsa/transforma', '''
scoreboard players operation #pid dv.tmp = @s dv.target
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
playsound minecraft:entity.ravager.roar hostile @a[distance=..48] ~ ~ ~ 1 0.5
playsound canon:diana.crack hostile @a[distance=..32] ~ ~ ~ 1 0.6
particle minecraft:large_smoke ~ ~1 ~ 0.6 1.5 0.6 0.05 60 normal
tellraw @a[distance=..48] {"text":"«Luna» se estira, se rompe y se levanta. Ya no tiene forma de perro.","color":"#c94a4a","italic":true}
function canon:sus/lbicho/summon
function canon:rig/despawn
''')
    tick('sus/lbicho', 'dv_lbicho', '''
execute if score #m2 dv.clock matches 0 run function canon:x/face
execute unless entity @a[tag=dv_wtgt,distance=..2.6] run function canon:x/walk
execute unless entity @a[tag=dv_wtgt,distance=..2.6] run function canon:x/walk_slow
scoreboard players remove @s[scores={dv.cool=1..}] dv.cool 1
execute if entity @a[tag=dv_wtgt,distance=..3] unless score @s dv.cool matches 1.. run function canon:sus/lbicho/ataca
execute if score #m20 dv.clock matches 0 run playsound minecraft:entity.warden.heartbeat hostile @a[distance=..24] ~ ~ ~ 1 0.6
execute if score @s dv.timer matches 700.. run function canon:sus/lfalsa/grita
''')
    F('sus/lbicho/ataca', 'scoreboard players set @s dv.cool 30\ndamage @a[tag=dv_wtgt,limit=1] 9 minecraft:mob_attack by @s\nplaysound minecraft:entity.ravager.attack hostile @a[distance=..16] ~ ~ ~ 1 0.5')

    # ================================================================ ABUELAS EN EL TECHO
    rig('sus/abutecho', 'dv_abutecho', 'Abuela', '#c9a27a', 7321010, 7321016, ['dv_horror'])
    c.on('second', f'''
execute if score {S} if predicate canon:de_noche as @a[gamemode=!spectator] at @s unless block ~ ~3 ~ #canon:pasable if entity @e[type=villager,distance=..32] unless entity @e[tag=dv_abutecho,distance=..48] if predicate canon:azar/1en200 run function canon:sus/abutecho/aparecer
execute if score {S} if predicate canon:de_noche as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if entity @s[y=40,dy=300] unless block ~ ~3 ~ #canon:pasable unless entity @e[tag=dv_abutecho,distance=..48] if predicate canon:azar/1en600 run function canon:sus/abutecho/aparecer
execute if score {S} if predicate canon:de_noche if score #abucasa dv.build matches 1 as @a[gamemode=!spectator] at @s unless block ~ ~3 ~ #canon:pasable unless entity @e[tag=dv_abutecho,distance=..48] if predicate canon:azar/1en60 run function canon:sus/abutecho/en_casa
''')
    F('sus/abutecho/en_casa', 'execute store result score #px dv.tmp run data get entity @s Pos[0]\nexecute store result score #pz dv.tmp run data get entity @s Pos[2]\n'
      'scoreboard players operation #px dv.tmp -= #abx dv.build\nscoreboard players operation #pz dv.tmp -= #abz dv.build\n'
      'execute if score #px dv.tmp matches -5..5 if score #pz dv.tmp matches -5..5 run function canon:sus/abutecho/aparecer')
    F('sus/abutecho/aparecer', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nscoreboard players set #zs dv.tmp 0\nscoreboard players set #ok dv.tmp 0\n'
      'execute anchored eyes positioned ^ ^ ^3 if block ~ ~ ~ #canon:pasable run function canon:sus/abutecho/buscar')
    F('sus/abutecho/buscar', '''scoreboard players add #zs dv.tmp 1
execute unless block ~ ~1 ~ #canon:pasable align y positioned ~ ~-0.83 ~ run function canon:sus/abutecho/poner
execute if score #ok dv.tmp matches 0 if score #zs dv.tmp matches ..5 if block ~ ~1 ~ #canon:pasable positioned ~ ~1 ~ run function canon:sus/abutecho/buscar''')
    F('sus/abutecho/poner', 'scoreboard players set #ok dv.tmp 1\nfunction canon:sus/abutecho/summon\nplaysound minecraft:block.wood.hit hostile @a[distance=..12] ~ ~1 ~ 0.6 0.5')
    tick('sus/abutecho', 'dv_abutecho', '''
execute on passengers run data merge entity @s {transformation:{left_rotation:[0f,0f,1f,0f]}}
execute if score #m4 dv.clock matches 0 run function canon:x/face
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score @s dv.watch matches 4.. run function canon:sus/abutecho/cae
execute if score @s dv.timer matches 1200.. run function canon:rig/despawn
''')
    F('sus/abutecho/cae', '''
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
playsound canon:devota.scream master @a[tag=dv_wtgt] ~ ~ ~ 1 0.7
damage @a[tag=dv_wtgt,distance=..6,limit=1] 3 minecraft:mob_attack by @s
tellraw @a[tag=dv_wtgt] {"text":"Estaba pegada del techo. Boca abajo. Sonriendo.","color":"#c94a4a","italic":true}
function canon:rig/despawn
''')

    # ================================================================ ESPANTAPÁJAROS
    rig('sus/espanta', 'dv_espanta', 'Espantapájaros', '#c8a86a', K['espanta_idle'], K['espanta_cabeza_creepy'], ['dv_horror'])
    c.frames('dv_espanta', 'sus/espanta/frames')
    F('sus/espanta/frames', 'scoreboard players set #frame dv.tmp 1')
    c.on('second', f'''
execute if score {S} as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if entity @e[type=villager,distance=..40] unless entity @e[tag=dv_espanta,distance=..64] if predicate canon:azar/1en400 run function canon:sus/espanta/aparecer
execute if score {S} if predicate canon:de_noche as @a[gamemode=!spectator,scores={{dv.home=1}}] at @s unless entity @e[tag=dv_espanta,distance=..64] if predicate canon:azar/1en1500 run function canon:sus/espanta/en_casa
''')
    F('sus/espanta/aparecer', 'scoreboard players operation #pid dv.tmp = @s dv.pid\n' + spot('sus/espanta/summon', '^ ^ ^16'))
    F('sus/espanta/en_casa', 'scoreboard players operation #pid dv.tmp = @s dv.pid\n' + spot('sus/espanta/summon', '^ ^ ^-6') +
      '\ntellraw @s {"text":"Huele a paja mojada. Algo hecho de paja está parado detrás de ti.","color":"#c8a86a","italic":true}')
    tick('sus/espanta', 'dv_espanta', '''
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players set @s dv.watch 0
execute if score #seen dv.tmp matches 0 run scoreboard players add @s dv.watch 1
execute if score #seen dv.tmp matches 0 if score #m4 dv.clock matches 0 run function canon:x/face
execute if score @s dv.watch matches 60.. if entity @a[tag=dv_wtgt,distance=4..32] run function canon:sus/espanta/mover
execute if score @s dv.watch matches 30.. if entity @a[tag=dv_wtgt,distance=..3] run function canon:sus/espanta/susto
execute if score @s dv.timer matches 12000.. run function canon:rig/despawn
''')
    F('sus/espanta/mover', 'scoreboard players set @s dv.watch 0\nexecute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^4 if block ~ ~ ~ #canon:pasable run tp @s ~ ~ ~\n'
      'execute at @s run function canon:diana/ground\nplaysound minecraft:block.grass.step hostile @a[tag=dv_wtgt] ~ ~ ~ 0.6 0.6')
    F('sus/espanta/susto', 'execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare\nplaysound minecraft:entity.ravager.roar hostile @a[distance=..16] ~ ~ ~ 0.6 1.6\nfunction canon:rig/despawn')

    # ================================================================ EL ÁRBOL DE LOS COLGADOS
    rig('sus/colgado', 'dv_colgado', '???', '#555555', 7321100, 7321102)
    c.on('second', f'''
execute if score #arbol_cd dv.dev matches 1.. run scoreboard players remove #arbol_cd dv.dev 1
execute if score {S} unless score #arbol_cd dv.dev matches 1.. as @a[gamemode=!spectator,predicate=canon:en_superficie,predicate=canon:bosque,limit=1,sort=random] at @s if predicate canon:azar/1en900 run function canon:sus/arbol/aparecer
''')
    F('sus/arbol/aparecer', 'scoreboard players operation #pid dv.tmp = @s dv.pid\n' + spot('sus/arbol/construir', '^ ^ ^30'))
    F('sus/arbol/construir', '''
scoreboard players set #arbol_cd dv.dev 12000
fill ~-4 ~ ~-4 ~4 ~10 ~4 minecraft:air
fill ~ ~ ~ ~1 ~9 ~1 minecraft:dark_oak_log
fill ~-4 ~8 ~ ~5 ~8 ~ minecraft:dark_oak_log[axis=x]
fill ~ ~7 ~-4 ~ ~7 ~5 minecraft:dark_oak_log[axis=z]
fill ~-4 ~6 ~ ~-4 ~7 ~ minecraft:chain
fill ~5 ~6 ~ ~5 ~7 ~ minecraft:chain
fill ~ ~5 ~-4 ~ ~6 ~-4 minecraft:chain
setblock ~1 ~10 ~1 minecraft:cobweb
setblock ~-2 ~8 ~1 minecraft:cobweb
setblock ~2 ~ ~2 minecraft:chest[facing=south]{LootTable:"canon:sus/colgados",Lock:"Llave oxidada"}
execute positioned ~-3.5 ~3.2 ~0.5 run function canon:sus/colgado/summon
execute positioned ~5.5 ~3.2 ~0.5 run function canon:sus/colgado/summon
execute positioned ~0.5 ~2.2 ~-3.5 run function canon:sus/colgado/summon
playsound minecraft:block.chain.step hostile @a[distance=..48] ~ ~5 ~ 1 0.5
tellraw @a[distance=..48] {"text":"Entre los árboles cruje algo. Como cadenas.","color":"gray","italic":true}
''')
    c.json('data/canon/loot_tables/sus/colgados.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': 3, 'entries': [lt('canon:sus/cofre', 1)]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:diamond', 'functions': [{'function': 'minecraft:set_count', 'count': 2}]}]}]})
    tick('sus/colgado', 'dv_colgado', '''
scoreboard players set @s dv.timer 0
execute if entity @a[tag=dv_wtgt,distance=..24] if score #m4 dv.clock matches 0 run function canon:x/face
execute if entity @a[tag=dv_wtgt,distance=..10] if score #m200 dv.clock matches 0 run playsound minecraft:block.chain.step hostile @a[distance=..16] ~ ~2 ~ 0.6 0.5
''')

    # ================================================================ LA LLORONA
    rig('sus/llorona', 'dv_llorona', 'La Llorona', '#e8e4e0', K['llorona_idle'], K['llorona_cabeza_llora'], ['dv_horror'])
    c.frames('dv_llorona', 'sus/llorona/frames')
    F('sus/llorona/frames', 'execute if score @s dv.state matches 0 run scoreboard players set #frame dv.tmp 3')
    agua = ' '.join(f'if block ~{x} ~-1 ~{z} minecraft:water' for x, z in ((4, 0),))
    c.on('second', f'''
execute if score {S} if predicate canon:de_noche unless entity @e[tag=dv_llorona] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:azar/1en300 run function canon:sus/llorona/agua
''')
    F('sus/llorona/agua', 'scoreboard players set #ag dv.tmp 0\n' + '\n'.join(
        f'execute if block ~{x} ~-1 ~{z} minecraft:water run scoreboard players set #ag dv.tmp 1' for x, z in ((5, 0), (-5, 0), (0, 5), (0, -5), (8, 8), (-8, -8), (8, -8), (-8, 8))) +
      '\nexecute if score #ag dv.tmp matches 1 run function canon:sus/llorona/aparecer')
    F('sus/llorona/aparecer', 'scoreboard players operation #pid dv.tmp = @s dv.pid\n' + spot('sus/llorona/summon', '^ ^ ^14') +
      '\ntellraw @s {"text":"Cerca del agua, una mujer llora. «¡Ay, mis hijos!»","color":"#d0d8e0","italic":true}')
    tick('sus/llorona', 'dv_llorona', '''
execute if score #m4 dv.clock matches 0 run function canon:x/face
execute if score #m40 dv.clock matches 0 run playsound minecraft:entity.ghast.ambient hostile @a[distance=..32] ~ ~ ~ 0.5 1.6
execute if score @s dv.state matches 0 if entity @a[tag=dv_wtgt,distance=..6] run function canon:sus/llorona/agarra
execute if score @s dv.timer matches 2400.. run function canon:rig/despawn
''')
    F('sus/llorona/agarra', f'''
scoreboard players set @s dv.state 1
{head(K['llorona_cabeza_vacia'])}
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
playsound canon:devota.scream master @a[tag=dv_wtgt] ~ ~ ~ 1 0.5
tp @a[tag=dv_wtgt,limit=1] @s
damage @a[tag=dv_wtgt,limit=1] 4 minecraft:mob_attack by @s
effect give @a[tag=dv_wtgt] minecraft:slowness 5 2 true
tellraw @a[tag=dv_wtgt] {{"text":"«¡Tú no eres mi hijo!»","color":"#c94a4a","italic":true}}
function canon:rig/despawn
''')

    # ================================================================ EL CUARTO QUE NO ESTABA (arriba, en el cielo de tu casa)
    c.patch('para/despertar', lambda s: s if 'sus/cuarto' in s else s.rstrip('\n') + f'\nexecute if score {S} if score @s dv.home matches 1 if predicate canon:azar/1en6 run function canon:sus/cuarto/aparece\n')
    F('sus/cuarto/aparece', 'execute store result score #cd dv.tmp run time query day\nscoreboard players operation #cd2 dv.tmp = #cd dv.tmp\nscoreboard players operation #cd dv.tmp -= @s dv.cuarto\nexecute if score #cd dv.tmp matches 3.. run function canon:sus/cuarto/aparece2')
    F('sus/cuarto/aparece2', 'scoreboard players operation @s dv.cuarto = #cd2 dv.tmp\nscoreboard players set #vf dv.tmp 0\n' + '\n'.join(
        f'execute if score #vf dv.tmp matches 0 anchored eyes rotated {a} 0 positioned ^ ^ ^1 run function canon:sus/cuarto/ray0' for a in (0, 90, 180, 270)))
    F('sus/cuarto/ray0', 'scoreboard players set #vs dv.tmp 0\nfunction canon:sus/cuarto/ray')
    F('sus/cuarto/ray', '''scoreboard players add #vs dv.tmp 1
execute unless block ~ ~ ~ #canon:pasable positioned ^ ^ ^-0.48 align y positioned ~ ~-0.5 ~ run function canon:sus/cuarto/puerta
execute if score #vf dv.tmp matches 0 if score #vs dv.tmp matches ..8 if block ~ ~ ~ #canon:pasable positioned ^ ^ ^1 run function canon:sus/cuarto/ray''')
    F('sus/cuarto/puerta', '''
scoreboard players set #vf dv.tmp 1
summon minecraft:item_display ~ ~1 ~ {Tags:["dv_cuarto_vis"],item_display:"fixed",item:{id:"minecraft:dark_oak_door",Count:1b},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,2f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=item_display,tag=dv_cuarto_vis,distance=..2,limit=1,sort=nearest] at @s rotated as @p run tp @s ~ ~ ~ ~180 0
summon minecraft:interaction ~ ~ ~ {Tags:["dv_cuarto_click","dv_click","dv_npc_click"],width:1.0f,height:2.0f,response:1b}
summon minecraft:marker ~ ~ ~ {Tags:["dv_cuarto_mk"]}
tellraw @a[distance=..12] {"text":"En la pared hay una puerta que ayer no estaba.","color":"#c94a4a","italic":true}
''')
    F('sus/cuarto/a_cama', 'execute store result score @s dv.rx run data get entity @s SpawnX\nexecute store result score @s dv.ry run data get entity @s SpawnY\nexecute store result score @s dv.rz run data get entity @s SpawnZ\nscoreboard players set @s dv.rdim 0')
    c.on('second', 'execute as @e[type=marker,tag=dv_cuarto_mk] at @s run function canon:sus/cuarto/tiempo')
    F('sus/cuarto/tiempo', 'scoreboard players add @s dv.timer 1\nexecute if score @s dv.timer matches 1200.. run function canon:sus/cuarto/borrar')
    F('sus/cuarto/borrar', 'kill @e[type=item_display,tag=dv_cuarto_vis,distance=..2]\nkill @e[type=interaction,tag=dv_cuarto_click,distance=..2]\nkill @s')
    c.click('dv_cuarto_click', 'sus/cuarto/entrar')
    F('sus/cuarto/entrar', 'execute as @a[tag=dv_talker,limit=1] at @s run function canon:sus/cuarto/entrar2\nkill @e[type=item_display,tag=dv_cuarto_vis,distance=..2]\nkill @e[type=marker,tag=dv_cuarto_mk,distance=..2]\nkill @s')
    F('sus/cuarto/entrar2', '''
function canon:travel/store_return
execute positioned ~ 300 ~ run function canon:sus/cuarto/construir
tp @s ~ 301 ~
playsound minecraft:block.wooden_door.open block @s ~ ~ ~ 1 0.5
tellraw @s {"text":"El cuarto huele a encierro. Hay una nota en la pared: «No debiste entrar».","color":"#c94a4a","italic":true}
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #quien dv.tmp 6
execute positioned ~2 301 ~2 run function canon:acecho/aparecer
''')
    F('sus/cuarto/construir', '''
fill ~-3 ~ ~-3 ~3 ~4 ~3 minecraft:blackstone hollow
fill ~-2 ~1 ~-2 ~2 ~3 ~2 minecraft:air
setblock ~ ~3 ~ minecraft:lantern[hanging=true]
setblock ~-2 ~1 ~-2 minecraft:chest[facing=south]{LootTable:"canon:sus/colgados",Lock:"Llave oxidada"}
setblock ~2 ~1 ~-2 minecraft:candle[lit=true,candles=2]
summon minecraft:interaction ~ ~1 ~2.4 {Tags:["dv_cuarto_salida","dv_click","dv_npc_click"],width:1.0f,height:2.0f,response:1b}
summon minecraft:item_display ~ ~2 ~2.45 {Tags:["dv_cuarto_salvis"],item_display:"fixed",item:{id:"minecraft:dark_oak_door",Count:1b},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,2f,1f],right_rotation:[0f,0f,0f,1f]}}
''')
    c.click('dv_cuarto_salida', 'sus/cuarto/salir')
    F('sus/cuarto/salir', '''
execute positioned ~ ~-1 ~-2.4 run fill ~-3 ~ ~-3 ~3 ~4 ~3 minecraft:air
kill @e[type=item_display,tag=dv_cuarto_salvis,distance=..4]
execute as @a[tag=dv_talker] if data entity @s SpawnX run function canon:sus/cuarto/a_cama
execute as @a[tag=dv_talker] run function canon:util/tp_return
tellraw @a[tag=dv_talker] {"text":"Despiertas en tu cama. La puerta ya no está. ¿Fue un sueño?","color":"gray","italic":true}
kill @s
''')

    # ================================================================ VELA NEGRA (premios) + ANIMALES QUE SE DEFIENDEN
    c.on('second', 'execute as @e[type=marker,tag=dv_vnegra] at @s run function canon:sus/vnegra')
    F('sus/vnegra', '''
scoreboard players add @s dv.timer 1
execute if score @s dv.timer matches 60 run function canon:sus/vnegra_premio
execute if score @s dv.timer matches 120 run function canon:sus/vnegra_premio
execute if score @s dv.timer matches 180 run function canon:sus/vnegra_premio
execute if score @s dv.timer matches 300.. run setblock ~ ~ ~ minecraft:air destroy
execute if score @s dv.timer matches 300.. run kill @s
''')
    F('sus/vnegra_premio', 'loot spawn ~ ~1 ~ loot canon:sus/cofre\nplaysound canon:devota.whisper hostile @a[distance=..16] ~ ~ ~ 0.7 0.6\n'
      'tellraw @a[distance=..16] {"text":"Junto a la vela negra apareció algo. Alguien lo dejó ahí.","color":"#8a8a8a","italic":true}')
    c.json('data/canon/advancements/sus/pega_animal.json', {'criteria': {'c': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'type': '#canon:pacificos'}}]}}},
        'rewards': {'function': 'canon:sus/animal/pegado'}})
    F('sus/animal/pegado', 'advancement revoke @s only canon:sus/pega_animal\nexecute as @e[type=#canon:pacificos,tag=!dv_brain,distance=..8,nbt=!{HurtTime:0s},limit=1,sort=nearest] run function canon:sus/animal/furia')
    F('sus/animal/furia', 'tag @s add dv_furia\nscoreboard players set @s dv.timer 0\nscoreboard players set @s dv.cool 0\nscoreboard players set @s dv.mode 0')
    c.on('tick', 'execute as @e[tag=dv_furia] at @s run function canon:sus/animal/tick')
    F('sus/animal/tick', '''
scoreboard players add @s dv.timer 1
scoreboard players remove @s[scores={dv.cool=1..}] dv.cool 1
execute facing entity @p[gamemode=!spectator,gamemode=!creative] feet rotated ~ 0 positioned ^ ^ ^0.22 if block ~ ~ ~ #canon:pasable run tp @s ~ ~ ~ ~ ~
execute if score #m10 dv.clock matches 0 run particle minecraft:angry_villager ~ ~1 ~ 0.3 0.3 0.3 0 1 normal
execute if entity @p[distance=..1.8,gamemode=!spectator,gamemode=!creative] unless score @s dv.cool matches 1.. run function canon:sus/animal/muerde
execute if score @s dv.timer matches 240.. run tag @s remove dv_furia
''')
    F('sus/animal/muerde', 'scoreboard players set @s dv.cool 20\nscoreboard players add @s dv.mode 1\nexecute if score @s dv.mode matches 2.. run tag @s remove dv_furia\ndamage @p[gamemode=!spectator,gamemode=!creative] 2 minecraft:mob_attack by @s\nplaysound minecraft:entity.player.hurt_sweet_berry_bush hostile @a[distance=..8] ~ ~ ~ 0.6 0.6')

    # ================================================================ admin
    adm = [('luna_falsa', 'execute as @e[type=wolf,tag=dv_luna,limit=1,sort=nearest] at @s run function canon:sus/luna/cambio', 'La Luna falsa (cambia a Luna)'),
           ('bicho', 'execute as @e[tag=dv_lfalsa,limit=1,sort=nearest] at @s run function canon:sus/lfalsa/transforma', 'La Luna falsa se transforma'),
           ('abuela_techo', 'function canon:sus/abutecho/aparecer', 'Abuela en el techo (bajo techo)'),
           ('espanta', 'function canon:sus/espanta/aparecer', 'Espantapájaros'),
           ('arbol', 'function canon:sus/arbol/aparecer', 'Árbol de los colgados'),
           ('llorona', 'function canon:sus/llorona/aparecer', 'La Llorona'),
           ('cuarto', 'function canon:sus/cuarto/aparece', 'El cuarto que no estaba'),
           ('hora', 'function canon:sus/hora_muerta', 'La hora muerta (3:11)'),
           ('micro', 'function canon:sus/micro', 'Un micro-susto'),
           ('items', '\n'.join(f'loot give @s loot canon:sus/{x[0]}' for x in NUEVOS if x[0] != 'cinta') +
            '\n' + '\n'.join(f'loot give @s loot canon:sus/cinta{n}' for n in range(1, 7)), 'Todos los ítems nuevos')]
    for nm, body, desc in adm:
        F(f'admin/sus/{nm}', body)
        c.admin(f'/function canon:admin/sus/{nm}', desc)
