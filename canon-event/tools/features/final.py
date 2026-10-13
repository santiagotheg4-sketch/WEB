"""Canon Event 11 (definitiva): la casa cuenta aunque no hayas dormido en una cama, fantasmas y demonios en el mundo
normal, zombis que tiran piedritas, la cara del miedo en la barra (con %), cartas bajo la
puerta y un libro guía para entender todo.
"""
import json
from PIL import Image, ImageDraw
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon import skins as SK
from canon.ctx import loot_item

CARTAS = [
    ('Juli', 'Para quien lea esto: no dejes la ventana abierta de noche. Yo la cierro desde el sueño, pero a veces no alcanzo. —J.', None),
    ('Diana', 'Te vi hoy. Caminas igual que él. Igual que Juan. ¿Sabías que eso no es casualidad? Nada es casualidad. —D.', None),
    ('Abuela Esmeralda', 'Mijo: le dejé sopita en la puerta. Si de noche alguien toca y dice que es la abuela, no le abra. La abuela tiene llave. —E.', None),
    ('Kevin', 'Mano, fiesta mañana. Lleva arepas. Si no llevas arepas no entras. Si llevas arepas tampoco, es broma, sí entras. —K.', None),
    ('???', 'Sé dónde duermes. Sé cuántas antorchas tienes. Te falta una en el pasillo.', None),
]
GUIA = [
    'GUÍA DE CANON EVENT\n\nTodo pasa solo. Juega normal: construye, explora, duerme. El mundo se va poniendo raro.\n\nDuerme en tu cama: así el mod sabe cuál es tu casa.',
    'TU CASA DE NOCHE\n\nPuertas que se abren, cofres que se pasan cosas, antorchas que se apagan, carteles «Te vi», gente en las ventanas, golpes en la puerta y abuelas en el techo.',
    'AFUERA\n\nDiana en las esquinas. El Mirón se acerca si lo miras. Gigantes en el horizonte. La Llorona cerca del agua. El árbol de los colgados en el bosque. Espantapájaros en las aldeas.',
    'EN LAS CUEVAS\n\nNicolás: ojos en la oscuridad, pegado al techo, corriendo por los túneles. Lleva luz siempre: en la oscuridad algo muerde.',
    'PERSONAJES\n\nClic derecho para hablar: Juli (en sueños), Dani, Kevin, la Abuela Esmeralda, Don Severo, el Narrador, Felipe y Mariana.',
    'OBJETOS\n\nMira el Recetario y el Catálogo:\n/trigger dv.items set 1\n\nOuija, velas, espejo, radio, EMF, sal, agua bendita, campanita, ojo de vidrio, collar de Luna...',
    'CADA DÍA\n\nMisión del día: /trigger dv.mision set 1\nCuaderno: se llena con lo que descubres.\nRachas: sobrevive noches sin morir.\nCartas: a veces te dejan una al amanecer.',
    'EL FINAL\n\nJunta las 13 páginas del diario de Diana. Te dirán cómo terminar esto.\n\nSi te quedas atrapado en un sueño:\n/trigger dv.despertar set 1',
]


def face(path, k):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    skin = [(232, 200, 170), (225, 200, 150), (220, 190, 120), (215, 150, 110), (190, 90, 90)][k]
    d.ellipse([1, 1, 14, 14], fill=skin + (255,), outline=(40, 25, 25, 255))
    eye = (20, 20, 20, 255)
    if k == 0:
        d.point([(5, 6), (10, 6)], fill=eye); d.line([5, 10, 10, 10], fill=eye); d.point([(4, 9), (11, 9)], fill=eye)
    elif k == 1:
        d.point([(5, 6), (10, 6)], fill=eye); d.line([5, 11, 10, 11], fill=eye)
    elif k == 2:
        d.rectangle([4, 5, 6, 7], fill=(255, 255, 255, 255)); d.rectangle([9, 5, 11, 7], fill=(255, 255, 255, 255))
        d.point([(5, 6), (10, 6)], fill=eye); d.ellipse([6, 9, 9, 12], fill=eye)
    elif k == 3:
        d.rectangle([3, 4, 6, 7], fill=(255, 255, 255, 255)); d.rectangle([9, 4, 12, 7], fill=(255, 255, 255, 255))
        d.point([(5, 6), (10, 6)], fill=eye); d.ellipse([5, 9, 10, 14], fill=(60, 0, 0, 255))
    else:
        d.rectangle([3, 4, 6, 7], fill=eye); d.rectangle([9, 4, 12, 7], fill=eye)
        d.line([4, 8, 4, 12], fill=(140, 0, 0, 255)); d.line([11, 8, 11, 13], fill=(140, 0, 0, 255)); d.ellipse([5, 9, 10, 14], fill=(20, 0, 0, 255))
    im.save(path)


def bars(path):
    """bars.png propio: barras oscuras de terror para todos los colores; la blanca (la del miedo) es invisible."""
    im = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cols = [(220, 110, 170), (80, 130, 230), (190, 25, 25), (80, 180, 80), (220, 190, 60), (150, 70, 210)]
    for i, col in enumerate(cols):
        y = i * 10
        d.rectangle([0, y, 181, y + 4], fill=(22, 14, 14, 230), outline=(60, 20, 20, 255))
        d.rectangle([0, y + 5, 181, y + 9], fill=col + (255,), outline=tuple(max(0, v - 80) for v in col) + (255,))
        d.line([1, y + 6, 180, y + 6], fill=tuple(min(255, v + 50) for v in col) + (255,))
    im.save(path)


def build(c):
    shim.use(c)
    S = '#sustos dv.cfg matches 1'

    # ================================================================ la casa cuenta aunque no hayas dormido en una cama
    c.patch('acoso/second', lambda s: s if 'dv_casa_techo' in s else s.replace(
        'scoreboard players remove @s[scores={dv.hcd=1..}] dv.hcd 1',
        'execute unless data entity @s SpawnX if entity @s[y=40,dy=300] unless block ~ ~2 ~ #canon:pasable run scoreboard players set @s dv.home 1\n'
        'execute unless data entity @s SpawnX if entity @s[y=40,dy=300] unless block ~ ~3 ~ #canon:pasable run scoreboard players set @s dv.home 1\n'
        'tag @s[scores={dv.home=1}] add dv_casa_techo\nscoreboard players remove @s[scores={dv.hcd=1..}] dv.hcd 1', 1))

    # ================================================================ HUD del miedo: caras + barra blanca invisible
    for k in range(5):
        face(c.path(f'assets/canon/textures/font/miedo{k}.png'), k)
    c.json('assets/canon/font/hud.json', {'providers': [{'type': 'bitmap', 'file': f'canon:font/miedo{k}.png', 'ascent': 11, 'height': 16,
                                                         'chars': [chr(0xE500 + k)]} for k in range(5)]})
    import os
    os.makedirs(os.path.dirname(c.path('assets/minecraft/textures/gui/bars.png')), exist_ok=True)
    bars(c.path('assets/minecraft/textures/gui/bars.png'))

    # ================================================================ rigs y ayudas
    def rig(prefix, tag, name, color, body, hd, tags=(), scale=1.0, click=None):
        F(f'{prefix}/summon', rig_summon([tag, *tags], name, color, head=hd is not None, scale=scale) + '\n'
          f'execute as @e[type=zombie,tag=dv_new,tag={tag},distance=..2,limit=1,sort=nearest] at @s run function canon:{prefix}/init')
        link = ''
        if click:
            link = (f'summon minecraft:interaction ~ ~ ~ {{Tags:["dv_link","dv_click","dv_npc_click","dv_xclick","{click}","dv_new_link"],width:0.9f,height:2.1f,response:1b}}\n'
                    'scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id\ntag @e[tag=dv_new_link] remove dv_new_link\nfunction canon:x/add_bubble\n')
        F(f'{prefix}/init', 'function canon:rig/init_common\n' + set_cmd('body', body) + '\n' + (head(hd) + '\n' if hd else '') +
          'scoreboard players operation @s dv.target = #pid dv.tmp\nscoreboard players set @s dv.state 0\nscoreboard players set @s dv.timer 0\n'
          'scoreboard players set @s dv.watch 0\nscoreboard players set @s dv.say -1\n' + link)
    HEAD = '''function canon:x/links_follow
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
tag @a remove dv_lookers
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..80] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
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
    WALKF = '''scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
'''

    # ================================================================ FANTASMAS y DEMONIO en el mundo normal
    rig('fin/fant', 'dv_fmundo', '???', '#c8d4dc', 7321021, 7321025, ['dv_horror'])
    rig('fin/dem', 'dv_dmundo', 'El de la cara roja', '#8b0000', 7321040, 7321046, ['dv_horror'])
    c.on('second', f'''
execute if score {S} if predicate canon:de_noche unless entity @e[tag=dv_fmundo] as @a[gamemode=!spectator,scores={{dv.home=1}}] at @s if predicate canon:azar/1en400 run function canon:fin/fant/aparecer
execute if score {S} if predicate canon:de_noche unless entity @e[tag=dv_dmundo] as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if entity @s[y=50,dy=300] if predicate canon:azar/1en1500 run function canon:fin/dem/aparecer
''')
    F('fin/fant/aparecer', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute rotated ~ 0 positioned ^-6 ^ ^5 align xyz positioned ~0.5 ~ ~0.5 rotated ~90 0 run function canon:fin/fant/summon\n'
      'playsound canon:devota.whisper hostile @s ~ ~ ~ 0.6 0.5')
    tick('fin/fant', 'dv_fmundo', '''
tp @s ^ ^ ^0.035
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score #m40 dv.clock matches 0 run playsound minecraft:entity.vex.ambient hostile @a[distance=..16] ~ ~ ~ 0.4 0.5
execute if score @s dv.watch matches 30.. run function canon:fin/fant/se_va
execute if score @s dv.timer matches 400.. run function canon:fin/fant/se_va
''')
    F('fin/fant/se_va', 'particle minecraft:soul ~ ~1 ~ 0.3 0.7 0.3 0.02 20 normal\ntellraw @a[tag=dv_wtgt] {"text":"Algo transparente cruzó la pared y se fue.","color":"#c8d4dc","italic":true}\nfunction canon:rig/despawn')
    F('fin/dem/aparecer', 'scoreboard players operation #pid dv.tmp = @s dv.pid\n' + spot('fin/dem/summon', '^ ^ ^24'))
    tick('fin/dem', 'dv_dmundo', '''
execute if score #m2 dv.clock matches 0 run function canon:x/face
function canon:x/seen
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score #seen dv.tmp matches 0 run scoreboard players add @s dv.state 1
execute if score #seen dv.tmp matches 1 run scoreboard players set @s dv.state 0
execute if score @s dv.watch matches 40.. run function canon:fin/dem/grita
execute if score @s dv.state matches 60.. unless entity @a[tag=dv_wtgt,distance=..2] run function canon:x/walk
execute if score @s dv.state matches 60.. unless entity @a[tag=dv_wtgt,distance=..2] run function canon:x/walk_slow
execute if entity @a[tag=dv_wtgt,distance=..2] run function canon:fin/dem/atrapa
execute if score @s dv.timer matches 1200.. run function canon:rig/despawn
''')
    F('fin/dem/grita', 'playsound canon:diana.scream hostile @a[distance=..48] ~ ~ ~ 1 0.4\nparticle minecraft:large_smoke ~ ~1 ~ 0.4 1 0.4 0.05 40 normal\n'
      'tellraw @a[tag=dv_wtgt] {"text":"El de la cara roja gritó y se deshizo en humo. Volverá.","color":"#8b0000","italic":true}\nfunction canon:rig/despawn')
    F('fin/dem/atrapa', 'execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare\ndamage @a[tag=dv_wtgt,limit=1] 4 minecraft:mob_attack by @s\n'
      'scoreboard players add @a[tag=dv_wtgt] dv.miedo 25\nfunction canon:rig/despawn')

    # ================================================================ ZOMBIS que tiran piedritas
    c.on('second', 'execute as @e[type=zombie,tag=!dv_brain] at @s if entity @a[distance=4..12,gamemode=!creative,gamemode=!spectator] if predicate canon:azar/1en30 run function canon:fin/zpiedra')
    F('fin/zpiedra', '''
tag @a remove dv_zpt
tag @a[distance=4..12,gamemode=!creative,gamemode=!spectator,limit=1,sort=nearest] add dv_zpt
execute anchored eyes facing entity @a[tag=dv_zpt,limit=1] eyes positioned ^ ^ ^1 summon minecraft:snowball run function canon:fin/zpiedra_ini
playsound minecraft:entity.snowball.throw hostile @a[distance=..16] ~ ~ ~ 1 0.5
tag @a remove dv_zpt
''')
    F('fin/zpiedra_ini', '''
data merge entity @s {Item:{id:"minecraft:cobblestone",Count:1b},Tags:["dv_zpiedra"]}
execute positioned 0.0 0.0 0.0 run summon minecraft:marker ^ ^0.12 ^0.95 {Tags:["dv_zvec"]}
data modify entity @s Motion set from entity @e[type=marker,tag=dv_zvec,limit=1] Pos
kill @e[type=marker,tag=dv_zvec]
''')
    c.on('tick', 'execute as @e[type=snowball,tag=dv_zpiedra] at @s if entity @a[distance=..1.3,gamemode=!creative,gamemode=!spectator] run function canon:fin/zpiedra_pega')
    F('fin/zpiedra_pega', 'damage @p[gamemode=!creative,gamemode=!spectator] 1 minecraft:generic\nplaysound minecraft:block.stone.hit hostile @a[distance=..8] ~ ~ ~ 1 1\nkill @s')

    # ================================================================ CARTAS bajo la puerta (al amanecer)
    for i, (de, txt, _) in enumerate(CARTAS):
        page = json.dumps(['', {'text': f'Carta de {de}\n\n', 'bold': True, 'color': 'dark_red'}, {'text': txt, 'color': 'black'}], ensure_ascii=False)
        c.json(f'data/canon/loot_tables/fin/carta{i}.json', loot_item('written_book', '{title:"Carta de ' + de + '",author:"' + de + '",generation:3,pages:[\'' +
                                                                       page.replace('\\', '\\\\').replace("'", "\\'") + '\']}'))
    gen = [i for i, x in enumerate(CARTAS) if not x[2]]
    c.pick('fin/carta/normal', [f'loot give @s loot canon:fin/carta{i}' for i in gen])
    c.patch('rel/racha/amanecer', lambda s: s if 'fin/carta' in s else s.rstrip('\n') + '\nexecute as @a[gamemode=!spectator] at @s if predicate canon:azar/1en4 run function canon:fin/carta/dar\n')
    F('fin/carta/dar', 'function canon:fin/carta/normal\n'
      'tellraw @s {"text":"Al amanecer, alguien deslizó una carta debajo de tu puerta.","color":"#e8c9a8","italic":true}\nplaysound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8')

    # ================================================================ LIBRO GUÍA (al entrar) + botón de ayuda
    pages = ','.join("'" + json.dumps({'text': t, 'color': 'black'}, ensure_ascii=False).replace('\\', '\\\\').replace("'", "\\'") + "'" for t in GUIA)
    c.json('data/canon/loot_tables/fin/guia.json', loot_item('written_book', '{title:"Guía de Canon Event",author:"El Narrador",generation:0,pages:[' + pages + ']}'))
    c.on('player', 'execute unless entity @s[tag=dv_guia] run function canon:fin/guia')
    F('fin/guia', 'tag @s add dv_guia\nloot give @s loot canon:fin/guia\ntellraw @s {"text":"Te dejaron un libro: «Guía de Canon Event». Léelo.","color":"#d77a8a","italic":true}')
    F('admin/fin/guia', 'loot give @s loot canon:fin/guia')
    c.admin('/function canon:admin/fin/guia', 'Otra copia de la Guía de Canon Event')

    # ================================================================ admin
    for nm, body, desc in [('fantasma', 'function canon:fin/fant/aparecer', 'Un fantasma cruza la pared'),
                           ('demonio', 'function canon:fin/dem/aparecer', 'El demonio a lo lejos'),
                           ('carta', 'function canon:fin/carta/dar', 'Una carta bajo la puerta')]:
        F(f'admin/fin/{nm}', body)
        c.admin(f'/function canon:admin/fin/{nm}', desc)
