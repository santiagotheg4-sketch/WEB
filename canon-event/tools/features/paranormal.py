"""Paranormal en el mundo normal + ideas para que nadie se aburra.
Ítems: Ouija, Kit de velas, Espejo, Radio de espíritus, Medidor EMF, Muñeca maldita, Caja de música, Sal,
Agua bendita, Libro de invocación, Grabadora. Poltergeist en tu casa. Diana roba e imita a tus amigos.
Nicolás tapa la salida. El de la cara roja te sigue. El Imitador. Regalos de Juli. Tienda de Dani.
Retos y bromas de Kevin. Tesoros de Luna. Misiones diarias. Logros. El Narrador.
"""
from PIL import Image, ImageDraw
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon import skins as SK
from canon.ctx import item_nbt, loot_item

ITEMS = [  # id, nombre, color, lore, cmd, receta (shapeless), icono(colores)
    ('ouija', 'Tablero Ouija', '#d9b88a', ['Clic derecho: pregúntale a los espíritus.', 'Siempre despídete.'], ['oak_planks', 'oak_planks', 'ink_sac', 'bone', 'phantom_membrane'], ((150, 100, 50), (40, 25, 15))),
    ('velas', 'Kit de ritual (velas)', '#f0e0b0', ['Clic derecho: haces un círculo de velas.', 'Algo vendrá al centro.'], ['candle', 'candle', 'candle', 'bone_meal', 'phantom_membrane'], ((240, 230, 200), (255, 120, 40))),
    ('espejo', 'Espejo de mano', '#c8d8e8', ['De noche, úsalo tres veces seguidas.', 'No lo hagas.'], ['glass_pane', 'iron_ingot', 'gold_nugget', 'phantom_membrane'], ((200, 220, 235), (120, 110, 90))),
    ('radio_esp', 'Radio de espíritus', '#8fb36a', ['Clic derecho: barre las frecuencias.', 'Entre la estática, alguien contesta.'], ['iron_ingot', 'redstone', 'copper_ingot', 'phantom_membrane'], ((80, 90, 60), (200, 60, 40))),
    ('emf', 'Medidor de energía (EMF)', '#e0d040', ['Tenlo en la mano: pita cuando algo está cerca.'], ['iron_ingot', 'redstone', 'gold_ingot', 'glowstone_dust', 'phantom_membrane'], ((60, 60, 60), (240, 220, 60))),
    ('muneca', 'Muñeca maldita', '#d8a0b0', ['Clic derecho: la dejas en el suelo.', 'Golpéala para guardarla. Si puedes.'], ['white_wool', 'string', 'spider_eye', 'phantom_membrane'], ((230, 200, 210), (40, 20, 20))),
    ('caja_musica', 'Caja de música', '#c9a46a', ['Clic derecho: suena una melodía vieja.', 'En la oscuridad, alguien baila.'], ['note_block', 'gold_nugget', 'phantom_membrane'], ((150, 100, 60), (230, 200, 120))),
    ('sal', 'Saco de sal', '#f4f4f4', ['Clic derecho: haces un círculo de sal por 5 minutos.', 'Lo que acecha no lo cruza.'], ['bone_meal', 'bone_meal', 'paper', 'phantom_membrane'], ((240, 240, 240), (200, 200, 200))),
    ('agua_bendita', 'Agua bendita', '#a0c8f0', ['Clic derecho: la lanzas adelante.', 'Quema a lo que no está vivo.'], ['glass_bottle', 'gold_nugget', 'ghast_tear', 'phantom_membrane'], ((150, 190, 240), (230, 240, 255))),
    ('libro_inv', 'Libro de invocación', '#8b2a2a', ['Clic derecho: llamas a alguien.', 'Puede que venga. Puede que venga otra cosa.'], ['book', 'ender_pearl', 'soul_sand', 'phantom_membrane'], ((110, 30, 30), (200, 170, 90))),
    ('grabadora', 'Grabadora vieja', '#9a9a9a', ['Clic derecho de noche: empieza a grabar.', 'De día: escucha lo que pasó mientras dormías.'], ['iron_ingot', 'redstone', 'string', 'phantom_membrane'], ((80, 80, 80), (30, 30, 30))),
]
BASE_CMD = 7311100
NARR = dict(skin='#bfb6ae', hair='#1a1a1a', hair_style='short', eyes='#d0d0d0', top='#2a2a30', top_style='hoodie', pants='#222226',
            shoes='#151515', lips='#5a5a5a', extras=['dark_circles'])
FRAG = ['Antes de Valle Quieto había un pueblo con otro nombre. Lo borraron con un deseo.',
        'El Hueso no concede deseos. Los presta. Y cobra intereses.',
        'Diana pidió no ser olvidada. Juan pidió olvidarla. Los dos deseos se cumplieron a medias.',
        'La abuela Esmeralda encontró el Hueso en el bosque, debajo de un árbol que no estaba ahí ayer.',
        'Juli no está dormida. Está esperando. No es lo mismo.',
        'Kevin volvió de las catacumbas con una sonrisa que no era suya. Bueno, casi suya.',
        'Mariana bailaba con Felipe. Él dejó de bailar. Ella no.',
        'Nicolás no odia a nadie. Solo quiere que alguien baje a buscarlo.',
        'El Mirón no hace daño. Solo mira lo que va a pasar. Por eso da miedo.',
        'En el Más Allá hay una puerta para cada persona. La tuya cambia de lugar cuando mientes.',
        'Luna ladra a lo que tú no ves. Hazle caso.',
        'Esta historia no termina. Solo cambia de dueño.']
FRAG2 = ['Juan pidió olvidar a Diana. El Hueso le cobró también el camino a casa. Lo encontraron en el río.',
         'Valery encontró la última astilla del Hueso. Pidió que Juan nunca recordara. Todavía no sabe que fue ella quien lo dejó perdido.',
         'La Abuela Esmeralda tuvo tres nietos más. Se fueron al bosque a buscar el Hueso. Todavía se ríen allá, de día.',
         'De noche, la abuela duerme. Lo que camina con su cara es lo que el Hueso dejó en su casa hace cuarenta años.',
         'Felipe se cayó al lago la noche de la fiesta. Mariana lo busca en todas partes menos en el agua.',
         'Diana escribió trece páginas. La última dice cómo terminar esto. Alguien las arrancó y las regó por el mundo.',
         'El de la cara roja no tiene nombre. Diana le dio el suyo. Y su cuerpo.',
         'Don Severo le vendió el Ouija a la muchacha pálida. Desde entonces no duerme. Por eso vende de día.',
         'Los Sin Rostro son la gente que Valle Quieto olvidó. Te miran porque quieren que alguien los recuerde.',
         'El Alto no camina. Cuando dejas de mirarlo, ya está más cerca. Kevin lo sabe. Por eso hace fiestas: para no estar solo.',
         'Juli duerme desde la noche del deseo. Si alguien termina esta historia, se despierta.',
         'Yo no soy parte de la historia. Yo solo la cuento. Por ahora.']


def icon(path, c1, c2):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 3, 13, 13], 2, fill=c1 + (255,), outline=tuple(max(0, v - 60) for v in c1) + (255,))
    d.rectangle([5, 6, 10, 10], fill=c2 + (255,))
    d.point([(4, 4), (11, 12)], fill=(255, 255, 255, 180))
    im.save(path)


def build(c):
    shim.use(c)
    c.config('paranormal', 'Actividad paranormal, misiones y logros', 1)
    for o in ('dv.ouija', 'dv.invoca', 'dv.tienda'):
        c.objective(o, 'trigger')
    c.objective('dv.mision', 'trigger')
    c.patch('camara/disparar', lambda s: s if 'dv.mfot' in s else s.rstrip('\n') + '\nscoreboard players add @s dv.mfot 1\n')
    for o in ('dv.espejo', 'dv.mfot', 'dv.grab', 'dv.durm', 'dv.demsig', 'dv.mis', 'dv.misp', 'dv.misd', 'dv.mcdp'):
        c.objective(o)
    c.objective('dv.mzk', 'minecraft.killed:minecraft.zombie')
    c.objective('dv.mfs', 'minecraft.custom:minecraft.fish_caught')
    c.objective('dv.mwk', 'minecraft.custom:minecraft.walk_one_cm')
    c.objective('dv.mpie', 'minecraft.mined:minecraft.stone')
    for n in (2, 3, 10, 20):
        c.const(n)
    # ----------------------------------------------------------- ítems
    for i, (iid, nom, col, lore, ing, (c1, c2)) in enumerate(ITEMS):
        cmd = BASE_CMD + i
        icon(c.path(f'assets/canon/textures/item/p_{iid}.png'), c1, c2)
        c.json(f'assets/canon/models/item/p_{iid}.json', {'parent': 'minecraft:item/handheld_rod', 'textures': {'layer0': f'canon:item/p_{iid}'}})
        c.item_model('carrot_on_a_stick', cmd, f'canon:item/p_{iid}')
        c.json(f'data/canon/loot_tables/para/{iid}.json', loot_item('carrot_on_a_stick', item_nbt(iid, nom, col, lore, cmd, 'Unbreakable:1b')))
        c.json(f'data/canon/recipes/p_{iid}.json', {'type': 'minecraft:crafting_shapeless', 'category': 'misc',
                                                   'ingredients': [{'item': 'minecraft:' + x} for x in ing], 'result': {'item': 'minecraft:knowledge_book', 'count': 1}})
        c.json(f'data/canon/advancements/para/receta_{iid}.json', {'criteria': {'c': {'trigger': 'minecraft:recipe_crafted', 'conditions': {
            'recipe_id': f'canon:p_{iid}'}}}, 'rewards': {'function': f'canon:para/craft/{iid}'}})
        F(f'para/craft/{iid}', f'clear @s minecraft:knowledge_book 1\nloot give @s loot canon:para/{iid}\nadvancement revoke @s only canon:para/receta_{iid}')
        if iid != 'emf':
            c.use_item(iid, f'para/{iid}/usar', cooldown=True)
    F('para/recetas', '\n'.join(f'recipe give @s canon:p_{x[0]}' for x in ITEMS) + '\ntag @s add dv_precetas')
    c.json('data/canon/predicates/mano/emf.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {
        'mainhand': {'items': ['minecraft:carrot_on_a_stick'], 'nbt': '{canon:{id:"emf"}}'}}}})
    c.on('player', '''
execute unless entity @s[tag=dv_precetas] run function canon:para/recetas
scoreboard players enable @s dv.ouija
scoreboard players enable @s dv.invoca
scoreboard players enable @s dv.tienda
scoreboard players enable @s dv.mision
execute if score @s dv.ouija matches 1.. run function canon:para/ouija/responder
execute if score @s dv.invoca matches 1.. run function canon:para/libro_inv/invocar
execute if score @s dv.tienda matches 1.. run function canon:para/tienda/comprar
execute if score @s dv.mision matches 1.. run function canon:para/mision/ver
execute if score #m10 dv.clock matches 0 if predicate canon:mano/emf run function canon:para/emf/medir
execute if data entity @s SleepingX run scoreboard players set @s dv.durm 1
execute if score @s dv.durm matches 1 unless data entity @s SleepingX run function canon:para/despertar
execute if score @s dv.dzz matches 100 if score #diana dv.cfg matches 1 if predicate canon:azar/1en6 run function canon:para/diana_roba
''')
    # Ouija
    F('para/ouija/usar', '''
scoreboard players set @s dv.cool 60
playsound minecraft:block.wood.place player @s ~ ~ ~ 0.6 0.6
''' + menu('@s', 'La plancheta tiembla bajo tus dedos...', '#d9b88a', [
        ('¿Hay alguien aquí?', '/trigger dv.ouija set 1'), ('¿Quién eres?', '/trigger dv.ouija set 2'), ('¿Qué quieres?', '/trigger dv.ouija set 3'),
        ('¿Dónde está Juan?', '/trigger dv.ouija set 4'), ('¿Voy a morir?', '/trigger dv.ouija set 5'), ('Adiós', '/trigger dv.ouija set 6')]))
    resp = {1: ['S Í', 'S Í . A T R Á S', 'N O . E S T O Y . S O L A'], 2: ['D I A N A', 'U N . A M I G O', 'T U . A B U E L A . N O'],
            3: ['Q U E . M E . R E C U E R D E S', 'T U . C A R A', 'J U G A R'], 4: ['B A J O . T U . C A M A', 'Y A . N O . E S . J U A N', 'B A N A'],
            5: ['T O D A V Í A . N O', 'H O Y', 'P R E G U N T A . O T R A . V E Z']}
    lines = ['scoreboard players operation #oq dv.tmp = @s dv.ouija', 'scoreboard players set @s dv.ouija 0',
             'playsound canon:miron.estatica ambient @s ~ ~ ~ 0.5 0.6', 'scoreboard players add @s dv.miedo 6']
    for q, ans in resp.items():
        c.pick(f'para/ouija/r{q}', ['tellraw @s ' + jt('La plancheta se mueve sola: ' + a, '#c94a4a', True) for a in ans])
        lines.append(f'execute if score #oq dv.tmp matches {q} run function canon:para/ouija/r{q}')
    lines += ['execute if score #oq dv.tmp matches 6 run tellraw @s {"text":"La plancheta va despacio hasta ADIÓS. Esta vez se fue.","color":"#d9b88a","italic":true}',
              'execute if score #oq dv.tmp matches 1..5 if predicate canon:azar/1en4 run function canon:para/ouija/algo']
    F('para/ouija/responder', '\n'.join(lines))
    F('para/ouija/algo', 'scoreboard players set @s dv.acd 0\nfunction canon:acecho/esquina\ntellraw @s {"text":"Ahora algo te está mirando. Lo llamaste.","color":"#c94a4a","italic":true}')
    # Kit de velas
    F('para/velas/usar', '''
scoreboard players set @s dv.cool 200
clear @s minecraft:carrot_on_a_stick{canon:{id:"velas"}} 1
setblock ~2 ~ ~ minecraft:candle[lit=true,candles=3] keep
setblock ~-2 ~ ~ minecraft:candle[lit=true,candles=3] keep
setblock ~ ~ ~2 minecraft:candle[lit=true,candles=3] keep
setblock ~ ~ ~-2 minecraft:candle[lit=true,candles=3] keep
summon minecraft:marker ~ ~ ~ {Tags:["dv_ritual","dv_ritual_new"]}
scoreboard players operation @e[type=marker,tag=dv_ritual_new] dv.pid = @s dv.pid
tag @e[type=marker,tag=dv_ritual_new] remove dv_ritual_new
tellraw @s {"text":"Prendes las velas en círculo. Las llamas se inclinan hacia el centro.","color":"#f0e0b0","italic":true}
playsound minecraft:item.flintandsteel.use player @s ~ ~ ~ 1 0.8
''')
    c.on('tick', 'execute as @e[type=marker,tag=dv_ritual] at @s run function canon:para/velas/tick')
    F('para/velas/tick', '''
scoreboard players add @s dv.timer 1
execute if score @s dv.timer matches 20 run particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.3 0.6 0.3 0.01 20 normal
execute if score @s dv.timer matches 60 run function canon:para/velas/viene
execute if score @s dv.timer matches 61.. run kill @s
''')
    c.pick('para/velas/viene', [
        'function canon:masalla/fantasma1\nloot spawn ~ ~1 ~ loot canon:items/petalo\ntellraw @a[distance=..12] {"text":"Un alma amable aparece en el centro y deja un pétalo.","color":"#c8d4dc","italic":true}',
        'function canon:masalla/fantasma2\ntellraw @a[distance=..12] {"text":"Un alma aparece en el centro. Te mira. Parece perdida.","color":"#c8d4dc","italic":true}',
        'scoreboard players operation #pid dv.tmp = @s dv.pid\nscoreboard players set #quien dv.tmp 1\nfunction canon:acecho/aparecer\nfill ~-2 ~ ~-2 ~2 ~ ~2 minecraft:candle[lit=false,candles=3] replace minecraft:candle[lit=true,candles=3]\nplaysound canon:diana.scream hostile @a[distance=..16] ~ ~ ~ 1 1\neffect give @a[distance=..12] minecraft:darkness 5 0 true\ntellraw @a[distance=..12] {"text":"Las velas se apagan de golpe. No era un alma amable.","color":"#c94a4a","italic":true}',
    ])
    # Espejo
    F('para/espejo/usar', '''
scoreboard players set @s dv.cool 10
scoreboard players add @s dv.espejo 1
playsound minecraft:block.glass.hit player @s ~ ~ ~ 0.6 1.4
execute if score @s dv.espejo matches 1 run title @s actionbar {"text":"Dices su nombre una vez...","color":"#c8d8e8","italic":true}
execute if score @s dv.espejo matches 2 run title @s actionbar {"text":"Dices su nombre dos veces...","color":"#c8d8e8","italic":true}
execute if score @s dv.espejo matches 3.. if predicate canon:de_noche run function canon:para/espejo/sale
execute if score @s dv.espejo matches 3.. unless predicate canon:de_noche run title @s actionbar {"text":"En el espejo solo estás tú. Es de día.","color":"#c8d8e8","italic":true}
execute if score @s dv.espejo matches 3.. run scoreboard players set @s dv.espejo 0
''')
    c.on('second', 'execute if score #m200 dv.clock matches 0..19 run scoreboard players set @a[scores={dv.espejo=1..}] dv.espejo 0')
    F('para/espejo/sale', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #quien dv.tmp 1
execute positioned ^ ^ ^-1.6 run function canon:acecho/aparecer
function canon:x/jumpscare
playsound canon:diana.jumpscare master @s ~ ~ ~ 1 1
scoreboard players add @s dv.miedo 30
tellraw @s {"text":"Dijiste su nombre tres veces. En el espejo, detrás de ti, alguien sonríe.","color":"#c94a4a","italic":true}
''')
    # Radio de espíritus
    F('para/radio_esp/usar', '''
scoreboard players set @s dv.cool 40
playsound canon:items.radio_static player @s ~ ~ ~ 1 1
tag @s add dv_fk
function canon:para/radio_esp/voz
tag @s remove dv_fk
execute if predicate canon:azar/1en5 run function canon:para/ouija/algo
''')
    c.pick('para/radio_esp/voz', ['tellraw @s ' + jt('Entre la estática: «' + t + '»', '#8fb36a', True) for t in [
        'Detrás... detrás de ti.', 'No apagues la luz.', 'Juli pregunta por Santi.', 'Me llamo... Esme... ralda.', 'Ya casi llego.',
        'Kevin, no le creas a Kevin.', 'Felipe, vuelve.', 'Aquí abajo hace frío.', 'Uno. Tres. Uno. Uno.', 'Te vi dormir.']]
        + ['tellraw @s ["",{"text":"Entre la estática, la voz de ","color":"#8fb36a","italic":true},{"selector":"@a[tag=!dv_fk,limit=1,sort=random]","color":"#8fb36a"},{"text":": «Ayúdame. No es mi cuerpo.»","color":"#8fb36a","italic":true}]'])
    # EMF
    F('para/emf/medir', '''
scoreboard players set #emf dv.tmp 1
execute if entity @e[tag=dv_horror,distance=..32] run scoreboard players set #emf dv.tmp 2
execute if entity @e[type=zombie,tag=dv_diana,distance=..32] run scoreboard players set #emf dv.tmp 2
execute if entity @e[tag=dv_fantasma,distance=..32] run scoreboard players set #emf dv.tmp 2
execute if entity @e[tag=dv_horror,distance=..20] run scoreboard players set #emf dv.tmp 3
execute if entity @e[tag=dv_fantasma,distance=..20] run scoreboard players set #emf dv.tmp 3
execute if entity @e[type=zombie,tag=dv_diana,distance=..20] run scoreboard players set #emf dv.tmp 3
execute if entity @e[tag=dv_horror,distance=..12] run scoreboard players set #emf dv.tmp 4
execute if entity @e[type=zombie,tag=dv_diana,distance=..12] run scoreboard players set #emf dv.tmp 4
execute if entity @e[tag=dv_horror,distance=..6] run scoreboard players set #emf dv.tmp 5
execute if entity @e[type=zombie,tag=dv_diana,distance=..6] run scoreboard players set #emf dv.tmp 5
execute if score #emf dv.tmp matches 1 run title @s actionbar {"text":"EMF ▮▯▯▯▯","color":"green"}
execute if score #emf dv.tmp matches 2 run title @s actionbar {"text":"EMF ▮▮▯▯▯","color":"yellow"}
execute if score #emf dv.tmp matches 3 run title @s actionbar {"text":"EMF ▮▮▮▯▯","color":"gold"}
execute if score #emf dv.tmp matches 4 run title @s actionbar {"text":"EMF ▮▮▮▮▯","color":"red"}
execute if score #emf dv.tmp matches 5 run title @s actionbar {"text":"EMF ▮▮▮▮▮  ESTÁ AQUÍ","color":"dark_red","bold":true}
execute if score #emf dv.tmp matches 2 run playsound minecraft:block.note_block.pling player @s ~ ~ ~ 0.3 0.8
execute if score #emf dv.tmp matches 3 run playsound minecraft:block.note_block.pling player @s ~ ~ ~ 0.4 1.1
execute if score #emf dv.tmp matches 4 run playsound minecraft:block.note_block.pling player @s ~ ~ ~ 0.5 1.5
execute if score #emf dv.tmp matches 5 run playsound minecraft:block.note_block.pling player @s ~ ~ ~ 0.7 2
''')
    # Muñeca maldita
    F('para/muneca/usar', '''
scoreboard players set @s dv.cool 20
clear @s minecraft:carrot_on_a_stick{canon:{id:"muneca"}} 1
execute positioned ^ ^ ^1.5 align xyz positioned ~0.5 ~ ~0.5 run function canon:para/muneca/poner
''')
    F('para/muneca/poner', '''
summon minecraft:item_display ~ ~ ~ {Tags:["dv_muneca","dv_mun_new"],item_display:"none",view_range:1.0f,item:{id:"minecraft:leather_horse_armor",Count:1b,tag:{CustomModelData:7320077}},transformation:{translation:[0f,0.5f,0f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:interaction ~ ~ ~ {Tags:["dv_munclick","dv_click","dv_npc_click","dv_mun_new"],width:0.7f,height:0.9f,response:1b}
scoreboard players operation @e[tag=dv_mun_new] dv.id = #next dv.id
scoreboard players add #next dv.id 1
tag @e[tag=dv_mun_new] remove dv_mun_new
''')
    c.click('dv_munclick', 'para/muneca/clic')
    c.attack('dv_munclick', 'para/muneca/recoger')
    c.pick('para/muneca/clic', ['tellraw @a[tag=dv_talker] ' + jt('La muñeca: «' + t + '»', '#d8a0b0', True) for t in
                                ['Juguemos.', 'Ya sé dónde duermes.', 'Me moví mientras parpadeabas.', 'No me dejes sola.']])
    F('para/muneca/recoger', '''
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=item_display,tag=dv_muneca] if score @s dv.id = #id dv.tmp run kill @s
loot give @a[tag=dv_talker] loot canon:para/muneca
kill @s
''')
    c.on('second', 'execute if predicate canon:de_noche as @e[type=item_display,tag=dv_muneca] at @s if entity @a[distance=..20] if predicate canon:azar/1en45 run function canon:para/muneca/moverse')
    F('para/muneca/moverse', '''
scoreboard players operation #id dv.tmp = @s dv.id
tag @s add dv_mun_mv
tag @a remove dv_lookers
tag @a[distance=..20] add dv_lookers
function canon:x/seen
tag @a remove dv_lookers
execute if score #seen dv.tmp matches 0 at @a[distance=..20,limit=1,sort=nearest] positioned ^ ^ ^-2 run function canon:para/muneca/destino
tag @s remove dv_mun_mv
''')
    F('para/muneca/destino', '''
scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 as @e[type=item_display,tag=dv_mun_mv] at @e[type=marker,tag=dv_spot,limit=1] run tp @s ~ ~ ~ facing entity @p feet
execute if score #ok dv.tmp matches 1 as @e[type=interaction,tag=dv_munclick] if score @s dv.id = #id dv.tmp at @e[type=marker,tag=dv_spot,limit=1] run tp @s ~ ~ ~
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run playsound canon:devota.giggle hostile @a[distance=..12] ~ ~ ~ 0.6 1.3
kill @e[type=marker,tag=dv_spot]
''')
    # Caja de música
    F('para/caja_musica/usar', '''
scoreboard players set @s dv.cool 240
playsound canon:fx.music_box_end record @a[distance=..20] ~ ~ ~ 1 1
execute if predicate canon:oscuro run function canon:para/caja_musica/baila
execute if predicate canon:de_noche run function canon:para/caja_musica/baila
''')
    F('para/caja_musica/baila', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #quien dv.tmp 1
execute positioned ^1.6 ^ ^1.2 run function canon:acecho/aparecer
tellraw @s {"text":"Con la música, alguien a tu lado empieza a bailar. Despacio. Torcido.","color":"#c94a4a","italic":true}
scoreboard players add @s dv.miedo 15
''')
    # Sal
    F('para/sal/usar', '''
scoreboard players set @s dv.cool 100
clear @s minecraft:carrot_on_a_stick{canon:{id:"sal"}} 1
summon minecraft:marker ~ ~ ~ {Tags:["dv_sal"]}
tellraw @s {"text":"Haces un círculo de sal. Por un rato, aquí nada entra.","color":"#f4f4f4","italic":true}
''')
    c.on('second', '''
execute as @e[type=marker,tag=dv_sal] at @s run function canon:para/sal/second
''')
    F('para/sal/second', '''
scoreboard players add @s dv.timer 1
particle minecraft:white_ash ~ ~0.1 ~ 2.5 0 2.5 0 40 normal
execute as @e[tag=dv_horror,distance=..5] at @s run function canon:camara/espanta
execute if score @s dv.timer matches 300.. run kill @s
''')
    # Agua bendita
    F('para/agua_bendita/usar', '''
scoreboard players set @s dv.cool 30
clear @s minecraft:carrot_on_a_stick{canon:{id:"agua_bendita"}} 1
playsound minecraft:entity.splash_potion.throw player @a[distance=..16] ~ ~ ~ 1 1
scoreboard players set #ab dv.tmp 0
execute anchored eyes positioned ^ ^ ^1 run function canon:para/agua_bendita/rayo
''')
    F('para/agua_bendita/rayo', '''
scoreboard players add #ab dv.tmp 1
execute if entity @e[tag=dv_horror,distance=..1.6] run scoreboard players set #ab dv.tmp 99
execute if entity @e[type=zombie,tag=dv_jefe,distance=..2.6] run scoreboard players set #ab dv.tmp 99
execute if entity @e[type=#canon:hostiles,distance=..1.6] run scoreboard players set #ab dv.tmp 99
execute unless block ~ ~ ~ #canon:pasable run scoreboard players set #ab dv.tmp 99
execute if score #ab dv.tmp matches 12.. run function canon:para/agua_bendita/salpica
execute if score #ab dv.tmp matches ..11 positioned ^ ^ ^0.8 run function canon:para/agua_bendita/rayo
''')
    F('para/agua_bendita/salpica', '''
particle minecraft:splash ~ ~ ~ 1 1 1 0.2 60 normal
particle minecraft:end_rod ~ ~ ~ 0.6 0.6 0.6 0.05 15 normal
playsound minecraft:entity.splash_potion.break player @a[distance=..16] ~ ~ ~ 1 1
execute as @e[tag=dv_horror,distance=..3] at @s run function canon:camara/espanta
execute as @e[type=zombie,tag=dv_jefe,distance=..4] run function canon:rel/jefe/agua
execute as @e[type=#canon:hostiles,distance=..3,limit=4] run damage @s 8 minecraft:magic
''')
    # Libro de invocación
    F('para/libro_inv/usar', 'scoreboard players set @s dv.cool 20\n' + menu('@s', 'LIBRO DE INVOCACIÓN: ¿a quién llamas?', '#8b2a2a', [
        ('Diana', '/trigger dv.invoca set 1'), ('Abuela Esmeralda', '/trigger dv.invoca set 2'), ('Un alma', '/trigger dv.invoca set 3'),
        ('Kevin', '/trigger dv.invoca set 4'), ('El Narrador', '/trigger dv.invoca set 5'), ('Terminar esto (13 páginas)', '/trigger dv.invoca set 6')]))
    F('para/libro_inv/invocar', '''
scoreboard players operation #iv dv.tmp = @s dv.invoca
scoreboard players set @s dv.invoca 0
execute if score @s dv.cool matches 1.. run tellraw @s {"text":"El libro todavía está caliente. Espera.","color":"gray","italic":true}
execute unless score @s dv.cool matches 1.. if entity @s[predicate=canon:mano/libro_inv] run function canon:para/libro_inv/llamar
''')
    F('para/libro_inv/llamar', '''
scoreboard players set @s dv.cool 1200
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #dstate dv.tmp 0
playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.6
particle minecraft:soul ~ ~1 ~ 1 1 1 0.02 30 normal
execute if score #iv dv.tmp matches 1 positioned ^ ^ ^5 run function canon:diana2/humana/summon
execute if score #iv dv.tmp matches 2 positioned ^ ^ ^5 run function canon:abuela/summon
execute if score #iv dv.tmp matches 3 positioned ^ ^ ^5 run function canon:masalla/fantasma1
execute if score #iv dv.tmp matches 4 positioned ^ ^ ^5 run function canon:kevin/summon
execute if score #iv dv.tmp matches 5 positioned ^ ^ ^5 run function canon:para/narrador/summon
execute if score #iv dv.tmp matches 6 run function canon:rel/jefe/invocar
execute if predicate canon:azar/1en4 run function canon:para/ouija/algo
''')
    # Grabadora
    F('para/grabadora/usar', '''
scoreboard players set @s dv.cool 40
execute store result score #gd dv.tmp run time query day
execute unless score @s dv.grab matches 1.. if predicate canon:de_noche run function canon:para/grabadora/grabar
execute if score @s dv.grab matches 1.. unless score @s dv.grab = #gd dv.tmp run function canon:para/grabadora/escuchar
execute if score @s dv.grab matches 1.. if score @s dv.grab = #gd dv.tmp run tellraw @s {"text":"Está grabando. Escúchala mañana.","color":"gray","italic":true}
execute unless score @s dv.grab matches 1.. unless predicate canon:de_noche run tellraw @s {"text":"Mejor graba de noche.","color":"gray","italic":true}
''')
    F('para/grabadora/grabar', 'scoreboard players operation @s dv.grab = #gd dv.tmp\nscoreboard players add @s dv.grab 0\nexecute if score @s dv.grab matches 0 run scoreboard players set @s dv.grab 1\n'
      'playsound minecraft:block.lever.click player @s ~ ~ ~ 1 1.6\ntellraw @s {"text":"Clic. La grabadora empieza a girar.","color":"#9a9a9a","italic":true}')
    c.pick('para/grabadora/escuchar', [f'tellraw @s {jt("La grabación: " + t, "#9a9a9a", True)}\nplaysound {s} hostile @s ~ ~ ~ 0.8 1\nscoreboard players set @s dv.grab 0' for t, s in [
        ('a las 3:11 se oye tu respiración... y otra respiración, más cerca del micrófono.', 'canon:diana.breath'),
        ('pasos que suben la escalera. Se detienen al lado de tu cama. Se quedan ahí una hora.', 'canon:diana.step'),
        ('una voz de mujer canta muy bajito. Dice tu nombre al final.', 'canon:devota.hum'),
        ('alguien golpea la ventana tres veces. Tú respondes dormido: «Ya voy».', 'canon:diana.knock'),
        ('una risa de niño. Luego, una voz: «Aquí abajo hace frío».', 'canon:nicolas.risa'),
        ('estática. Solo estática. Y al final, muy claro: «Te encontré».', 'canon:miron.estatica')]])
    # ----------------------------------------------------------- poltergeist en tu casa
    c.on('second', '''
execute if score #paranormal dv.cfg matches 1 as @a[gamemode=!spectator,scores={dv.home=1}] at @s if predicate canon:de_noche if predicate canon:azar/1en180 run function canon:para/polter
''')
    c.pick('para/polter', [
        'playsound minecraft:block.wooden_door.open block @s ^3 ^ ^-3 1 0.9\nplaysound minecraft:block.wooden_door.close block @s ^3 ^ ^-3 1 0.8\ntellraw @s {"text":"Una puerta se abrió y se cerró sola.","color":"gray","italic":true}',
        'execute as @e[type=painting,distance=..12,limit=1,sort=random] at @s run function canon:para/cuadro_cae',
        'playsound minecraft:block.chest.open block @s ^-3 ^ ^2 1 0.8\nplaysound minecraft:block.chest.close block @s ^-3 ^ ^2 1 0.8',
        'function canon:para/cartel_te_vi',
        'playsound minecraft:block.chain.fall block @s ^2 ^1 ^-2 1 0.6\nplaysound minecraft:entity.item.pickup block @s ^-2 ^ ^ 0.7 0.5',
        'playsound minecraft:block.glass.break block @s ^5 ^1 ^-4 0.7 0.6\ntellraw @s {"text":"Algo de vidrio se rompió en otro cuarto. No hay nada roto.","color":"gray","italic":true}',
        'function canon:rel/polter/puerta', 'function canon:rel/polter/trampilla', 'function canon:rel/polter/antorcha',
        'function canon:rel/polter/cofre', 'function canon:rel/polter/mueble',
    ])
    F('para/cuadro_cae', 'summon minecraft:item ~ ~ ~ {Item:{id:"minecraft:painting",Count:1b}}\nplaysound minecraft:entity.painting.break block @a[distance=..16] ~ ~ ~ 1 0.8\nkill @s')
    F('para/cartel_te_vi', '''
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-3 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run setblock ~ ~ ~ minecraft:dark_oak_sign[rotation=0]{front_text:{messages:['{"text":"TE VI","color":"dark_red"}','{"text":"dormir","color":"dark_red"}','{"text":"","color":"black"}','{"text":"","color":"black"}']}} keep
kill @e[type=marker,tag=dv_spot]
''')
    # ----------------------------------------------------------- Diana roba e imita
    c.pick('para/diana_roba', [f'''data remove storage canon:tmp robo
data modify storage canon:tmp robo set from entity @s Inventory[{{Slot:{k}b}}]
execute if data storage canon:tmp robo run function canon:para/diana_roba{k}''' for k in range(9)])
    for k in range(9):
        F(f'para/diana_roba{k}', f'''
item replace entity @s hotbar.{k} with minecraft:air
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-9 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run summon minecraft:item ~ ~0.5 ~ {{Tags:["dv_robado"],Item:{{id:"minecraft:stone",Count:1b}},PickupDelay:0s}}
execute unless score #ok dv.tmp matches 1 run summon minecraft:item ~ ~1 ~ {{Tags:["dv_robado"],Item:{{id:"minecraft:stone",Count:1b}},PickupDelay:0s}}
kill @e[type=marker,tag=dv_spot]
execute as @e[type=item,tag=dv_robado] run data modify entity @s Item set from storage canon:tmp robo
execute as @e[type=item,tag=dv_robado] run data remove entity @s Item.Slot
tag @e[type=item,tag=dv_robado] remove dv_robado
tellraw @s {{"text":"Mientras dormías, alguien hurgó en tus cosas. Te falta algo. Huele a tierra mojada.","color":"#c94a4a","italic":true}}
''')
    c.on('second', '''
execute if score #diana dv.cfg matches 1 as @a[gamemode=!spectator] at @s if predicate canon:de_noche if predicate canon:azar/1en1800 run function canon:para/voz_amigo
''')
    F('para/voz_amigo', '''
tag @s add dv_fk
execute if entity @a[tag=!dv_fk] run function canon:para/voz_amigo2
execute unless entity @a[tag=!dv_fk] run tellraw @s ["",{"text":"<Juli> ","color":"white"},{"text":"ven, estoy afuera. no me dejes aquí sola","color":"white"}]
tag @s remove dv_fk
''')
    c.pick('para/voz_amigo2', ['tellraw @s ["",{"text":"<"},{"selector":"@a[tag=!dv_fk,limit=1,sort=random]"},{"text":"> ' + t + '"}]' for t in [
        'ven rápido, encontré algo en la cueva de aquí cerca', 'oye abre la puerta, soy yo', 'no mires atrás', 'estoy detrás de ti jaja',
        'ya vengo, no te muevas de ahí']])
    # ----------------------------------------------------------- Nicolás tapa la salida
    c.on('second', '''
execute if score #nicolas dv.cfg matches 1 as @a[gamemode=!spectator,gamemode=!creative,predicate=canon:en_superficie] at @s if entity @s[y=-64,dy=104] if predicate canon:azar/1en900 run function canon:para/nico_tapa
execute as @e[type=marker,tag=dv_tapa] at @s run function canon:para/nico_tapa_tick
''')
    F('para/nico_tapa', '''
execute rotated ~ 0 positioned ^ ^ ^-3 run fill ^-1 ^ ^ ^1 ^2 ^ minecraft:cobblestone replace minecraft:air
execute rotated ~ 0 positioned ^ ^ ^-3 run summon minecraft:marker ~ ~ ~ {Tags:["dv_tapa","dv_tapa_new"]}
execute rotated ~ 0 as @e[type=marker,tag=dv_tapa_new] run tp @s ~ ~ ~ ~ 0
tag @e[type=marker,tag=dv_tapa_new] remove dv_tapa_new
playsound canon:mina.derrumbe hostile @s ^ ^ ^-3 1 0.9
playsound canon:nicolas.risa hostile @s ^ ^ ^-5 1 0.8
tellraw @s {"text":"Nicolás tapó el túnel detrás de ti. Se ríe al otro lado. ¡Pica!","color":"#8a8a96","italic":true}
''')
    F('para/nico_tapa_tick', '''
scoreboard players add @s dv.timer 1
execute if score @s dv.timer matches 30.. rotated as @s run fill ^-1 ^ ^ ^1 ^2 ^ minecraft:air replace minecraft:cobblestone
execute if score @s dv.timer matches 30.. run kill @s
''')
    # ----------------------------------------------------------- El de la cara roja te sigue
    c.patch('masalla/volver', lambda s: s if 'dv.demsig' in s else s.rstrip('\n') + '\nscoreboard players set @s dv.demsig 600\n')
    F('para/rig_demonio', rig_summon(['dv_asomo', 'dv_horror'], 'El de la cara roja', '#8b0000') + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_asomo,distance=..2,limit=1,sort=nearest] at @s run function canon:para/rig_demonio_init')
    F('para/rig_demonio_init', f'function canon:rig/init_common\n{set_cmd("body", 7321040)}\n{head(7321046)}\nscoreboard players operation @s dv.target = #pid dv.tmp\nscoreboard players set @s dv.watch 0')
    c.on('second', '''
scoreboard players remove @a[scores={dv.demsig=1..}] dv.demsig 1
execute as @a[scores={dv.demsig=1..},predicate=canon:en_superficie] at @s if predicate canon:de_noche if predicate canon:azar/1en80 run function canon:para/demonio_sigue
''')
    F('para/demonio_sigue', '''
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-9 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:para/rig_demonio
kill @e[type=marker,tag=dv_spot]
tellraw @s {"text":"Volviste del Más Allá... pero no volviste solo.","color":"#8b0000","italic":true}
''')
    # ----------------------------------------------------------- El Imitador
    c.json('data/canon/tags/entity_types/imitables.json', {'values': ['minecraft:cow', 'minecraft:sheep', 'minecraft:pig', 'minecraft:chicken']})
    c.on('second', 'execute if score #paranormal dv.cfg matches 1 if predicate canon:de_noche as @a[gamemode=!spectator,gamemode=!creative] at @s as @e[type=#canon:imitables,distance=..5,limit=1] at @s if predicate canon:azar/1en300 run function canon:para/imitador')
    F('para/imitador', '''
summon minecraft:zombie ~ ~ ~ {CustomName:'{"text":"El Imitador","color":"#8b0000"}',Tags:["dv_zinit","dv_zvar","dv_imitador"],CanPickUpLoot:0b,Attributes:[{Name:"generic.movement_speed",Base:0.36d},{Name:"generic.max_health",Base:30d},{Name:"generic.attack_damage",Base:6d}],Health:30f,ArmorItems:[{},{},{},{id:"minecraft:carved_pumpkin",Count:1b}],ArmorDropChances:[0f,0f,0f,0f]}
particle minecraft:large_smoke ~ ~0.8 ~ 0.4 0.5 0.4 0.03 30 normal
playsound minecraft:entity.ravager.roar hostile @a[distance=..24] ~ ~ ~ 0.8 1.4
tellraw @a[distance=..16] {"text":"El animal se dobla, se estira... no era un animal.","color":"#c94a4a","italic":true}
tp @s ~ -300 ~
kill @s
''')
    # ----------------------------------------------------------- Juli: regalos al despertar
    F('para/despertar', '''
scoreboard players set @s dv.durm 0
execute if predicate canon:de_dia if score #juli dv.cfg matches 1 if predicate canon:azar/1en4 run function canon:para/juli_regalo
''')
    c.pick('para/juli_regalo', [
        'loot give @s loot canon:items/petalo\ntellraw @s {"text":"Al despertar hay un pétalo rosado en tu almohada. Huele a Juli.","color":"#f2a7c3","italic":true}',
        'give @s minecraft:pink_tulip\ntellraw @s {"text":"Al despertar hay un tulipán en tu cama. Nadie entró. Nadie.","color":"#f2a7c3","italic":true}',
        'loot give @s loot canon:extras/chocolate\ntellraw @s {"text":"Al despertar hay un chocolate caliente al lado de la cama. Todavía humea.","color":"#f2a7c3","italic":true}'])
    # ----------------------------------------------------------- Dani: tienda
    c.patch('dani/clic', lambda s: s if 'dv.dani set 8' in s else s.rstrip('\n') + '\n' +
            menu('@a[tag=dv_talker]', '', '#9fc3a8', [('¿Qué vendes, Dani?', '/trigger dv.dani set 8')]) + '\n')
    c.patch('dani/responde', lambda s: s if 'para/tienda/abrir' in s else s.rstrip('\n') + '\nexecute if score #dac dv.tmp matches 8 run function canon:para/tienda/abrir\n')
    F('para/tienda/abrir', say('Dani', '#9fc3a8', '#e3f1e6', '¿Cómo estás? ¿Comiste? Vendo comida casera, una esmeralda cada cosa. Y te la regalo si te veo muy flaco. Jaja.', 140) + '\n' +
      menu('@a[tag=dv_datalk]', 'TIENDA DE DANI (1 esmeralda)', '#9fc3a8', [('Arepa', '/trigger dv.tienda set 1'), ('Empanada', '/trigger dv.tienda set 2'),
                                                                        ('Chocolate', '/trigger dv.tienda set 3'), ('Café', '/trigger dv.tienda set 4'),
                                                                        ('Buñuelo', '/trigger dv.tienda set 5')]))
    tienda = ['scoreboard players operation #tv dv.tmp = @s dv.tienda', 'scoreboard players set @s dv.tienda 0',
              'execute store result score #esm dv.tmp run clear @s minecraft:emerald 0',
              'execute unless entity @e[type=zombie,tag=dv_dani,distance=..12] run scoreboard players set #esm dv.tmp -1',
              'execute if score #esm dv.tmp matches 0 run tellraw @s {"text":"Dani: No tienes esmeraldas, pero bueno... la próxima me pagas.","color":"#e3f1e6","italic":true}',
              'execute if score #esm dv.tmp matches 1.. run clear @s minecraft:emerald 1']
    for k, food in enumerate(['arepa', 'empanada', 'chocolate', 'cafe', 'bunuelo'], 1):
        tienda.append(f'execute if score #esm dv.tmp matches 0.. if score #tv dv.tmp matches {k} run loot give @s loot canon:extras/{food}')
    tienda.append('execute if score #esm dv.tmp matches 0.. run playsound minecraft:entity.villager.yes neutral @s ~ ~ ~ 0.6 1.3')
    F('para/tienda/comprar', '\n'.join(tienda))
    # ----------------------------------------------------------- Kevin: retos y bromas
    c.patch('kevin/clicked', lambda s: s if 'dv.kv set 7' in s else s.rstrip('\n') + '\nexecute unless score #kev dv.dev matches 1.. run ' +
            menu('@a[tag=dv_talker]', '', '#ffb347', [('Reto', '/trigger dv.kv set 7')]) + '\n')
    c.patch('kevin/c/run', lambda s: s if 'para/kevin/reto' in s else s.rstrip('\n') + '\nexecute if score #kc dv.tmp matches 7 run function canon:para/kevin/reto\n')
    F('para/kevin/reto', '''
kill @e[type=marker,tag=dv_meta]
scoreboard players set #ok dv.tmp 0
execute at @a[tag=dv_ktalk,limit=1] positioned ^ ^ ^18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["dv_meta","dv_meta_new"]}
kill @e[type=marker,tag=dv_spot]
scoreboard players operation @e[type=marker,tag=dv_meta_new] dv.pid = @a[tag=dv_ktalk,limit=1] dv.pid
tag @e[type=marker,tag=dv_meta_new] remove dv_meta_new
''' + say('Kevin', '#ffb347', '#ffd27a', '¡Reto! Llega a la luz verde en 10 segundos. Si pierdes, me debes una arepa. ¡Ya!', 80, '@a[distance=..20]'))
    c.on('tick', 'execute as @e[type=marker,tag=dv_meta] at @s run function canon:para/kevin/meta')
    F('para/kevin/meta', '''
scoreboard players add @s dv.timer 1
particle minecraft:happy_villager ~ ~1 ~ 0.2 1.5 0.2 0 6 force
scoreboard players operation #pid dv.tmp = @s dv.pid
scoreboard players set #gano dv.tmp 0
execute as @a[distance=..2] if score @s dv.pid = #pid dv.tmp run scoreboard players set #gano dv.tmp 1
execute if score #gano dv.tmp matches 1 as @a[distance=..2] if score @s dv.pid = #pid dv.tmp run function canon:para/kevin/gana
execute if score #gano dv.tmp matches 1 run kill @s
execute if score @s dv.timer matches 200.. run tellraw @a[distance=..40] {"text":"Kevin: ¡Perdiste! Jajaja. Me debes una arepa.","color":"#ffb347","italic":true}
execute if score @s dv.timer matches 200.. run kill @s
''')
    F('para/kevin/gana', 'loot give @s loot canon:items/billete\nloot give @s loot canon:items/billete\nplaysound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1.2\n'
      'tellraw @s {"text":"Kevin: ¡Uy! Ganaste. Tome, unos billetes. No se los gaste en Mariana.","color":"#ffb347","italic":true}')
    c.on('second', 'execute as @e[type=zombie,tag=dv_kevin,scores={dv.mode=0}] at @s if entity @a[distance=..10] if predicate canon:azar/1en240 run function canon:para/kevin/broma')
    F('para/kevin/broma', '''
execute as @a[distance=..10,limit=1,sort=nearest] at @s run tp @e[type=zombie,tag=dv_kevin,limit=1,sort=nearest] ^ ^ ^-1.6
execute as @a[distance=..10,limit=1,sort=nearest] run title @s times 0 15 10
execute as @a[distance=..10,limit=1,sort=nearest] run title @s title {"text":"¡BU!","color":"#ffb347","bold":true}
playsound canon:kevin.laugh neutral @a[distance=..16] ~ ~ ~ 1 1
playsound canon:kevin.hey neutral @a[distance=..16] ~ ~ ~ 1 1.3
scoreboard players add @a[distance=..10,limit=1,sort=nearest] dv.miedo 8
''')
    # ----------------------------------------------------------- Luna: tesoros
    c.on('tick', 'execute as @e[type=wolf,tag=dv_luna,scores={dv.lpose=21,dv.ltime=5}] at @s if predicate canon:azar/1en3 run function canon:para/luna_tesoro')
    c.pick('para/luna_tesoro', [f'loot spawn ~ ~0.5 ~ loot {t}\ntellraw @a[distance=..16] {jt("Luna desenterró algo y te lo trae moviendo la cola.", "#ffd27a", True)}' for t in
                                ['canon:items/billete', 'canon:items/petalo', 'canon:items/carta', 'canon:items/mechon', 'canon:extras/arepa']])
    # ----------------------------------------------------------- misiones diarias
    c.on('second', 'execute if score #paranormal dv.cfg matches 1 as @a[gamemode=!spectator] run function canon:para/mision/second')
    MIS = [(1, 'Mata 10 zombies', 'dv.mzk', 10), (2, 'Pica 64 bloques de piedra', 'dv.mpie', 64), (3, 'Camina 1000 bloques', 'dv.mwk', 100000),
           (4, 'Pesca 3 peces', 'dv.mfs', 3), (5, 'Saca 3 fotos con la cámara instantánea', 'dv.mfot', 3)]
    F('para/mision/second', '''
execute store result score #md dv.tmp run time query day
execute unless score @s dv.misd = #md dv.tmp run function canon:para/mision/nueva
execute if score @s dv.mis matches 1..5 run function canon:para/mision/revisar
''')
    nueva = ['scoreboard players operation @s dv.misd = #md dv.tmp', 'scoreboard players set @s dv.misp 0'] + \
            [f'scoreboard players set @s {o} 0' for _, _, o, _ in MIS] + ['function canon:para/mision/elegir',
                                                                          'function canon:para/mision/ver']
    F('para/mision/nueva', '\n'.join(nueva))
    c.pick('para/mision/elegir', [f'scoreboard players set @s dv.mis {k}' for k, *_ in MIS])
    rev = []
    ver = ['scoreboard players set @s dv.mision 0']
    for k, txt_, obj, meta in MIS:
        rev.append(f'execute if score @s dv.mis matches {k} if score @s {obj} matches {meta}.. run function canon:para/mision/cumplida')
        ver.append(f'execute if score @s dv.mis matches {k} run tellraw @s ["",{jt("☾ Misión del día: ", "#d77a8a")},{jt(txt_, "white")}]')
    ver.append('execute if score @s dv.mis matches 0 run tellraw @s {"text":"☾ Ya cumpliste la misión de hoy. Mañana hay otra.","color":"gray","italic":true}')
    F('para/mision/revisar', '\n'.join(rev))
    F('para/mision/ver', '\n'.join(ver))
    c.pick('para/mision/premio', [f'loot give @s loot {t}' for t in ['canon:extras/chocolate', 'canon:extras/arepa', 'canon:para/sal',
                                                                     'canon:para/agua_bendita', 'canon:camara/pelicula', 'canon:extras/crucifijo']])
    F('para/mision/cumplida', '''
scoreboard players set @s dv.mis 0
function canon:para/mision/premio
loot give @s loot canon:items/billete
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1
tellraw @a ["",{"text":"☾ ","color":"#d77a8a"},{"selector":"@s","color":"gold"},{"text":" cumplió su misión del día.","color":"gray"}]
advancement grant @s only canon:logros/mision
''')
    c.admin('/trigger dv.mision set 1', 'Ver tu misión del día (cualquiera)')
    # ----------------------------------------------------------- logros
    LOG = [('raiz', None, 'Canon Event', 'Lo que tiene que pasar, va a pasar.', 'minecraft:bone', 'task'),
           ('susto', 'raiz', 'Primer susto', 'Algo te gritó en la cara.', 'minecraft:carved_pumpkin', 'task'),
           ('foto', 'raiz', 'Fotógrafo paranormal', 'Saca una foto con la cámara instantánea.', 'minecraft:paper', 'task'),
           ('masalla', 'raiz', 'Ida y vuelta', 'Vuelve del Más Allá por la puerta correcta.', 'minecraft:soul_lantern', 'goal'),
           ('miedo', 'raiz', 'No estás solo', 'Llega al 100 de miedo.', 'minecraft:redstone', 'task'),
           ('mariana', 'raiz', 'Nunca me vuelvas a hablar', 'Hazla enojar.', 'minecraft:poppy', 'task'),
           ('abuela', 'raiz', 'Sopita de la abuela', 'Acepta la sopa de la Abuela Esmeralda.', 'minecraft:mushroom_stew', 'task'),
           ('ouija', 'raiz', 'Hay alguien aquí', 'Usa el tablero Ouija.', 'minecraft:oak_planks', 'task'),
           ('visita', 'raiz', 'Te encontré', 'Sobrevive a la visita nocturna de Diana.', 'minecraft:wither_rose', 'challenge'),
           ('mision', 'raiz', 'Cumplidor', 'Cumple una misión del día.', 'minecraft:emerald', 'task'),
           ('tala', 'raiz', 'Tala total', 'Tumba un árbol entero de un golpe.', 'minecraft:iron_axe', 'task')]
    for lid, parent, tit, desc, ic, frame in LOG:
        adv = {'display': {'icon': {'item': ic}, 'title': {'text': tit, 'color': '#d77a8a'}, 'description': {'text': desc},
                           'frame': frame, 'show_toast': True, 'announce_to_chat': lid != 'raiz', 'hidden': False},
               'criteria': {'c': {'trigger': 'minecraft:impossible'}}}
        if parent:
            adv['parent'] = f'canon:logros/{parent}'
        else:
            adv['display']['background'] = 'minecraft:textures/block/blackstone.png'
            adv['criteria'] = {'c': {'trigger': 'minecraft:tick'}}
        c.json(f'data/canon/advancements/logros/{lid}.json', adv)
    grants = [('x/jumpscare', 'advancement grant @s only canon:logros/susto'), ('camara/disparar', 'advancement grant @s only canon:logros/foto'),
              ('masalla/volver', 'advancement grant @s only canon:logros/masalla'), ('para/ouija/usar', 'advancement grant @s only canon:logros/ouija'),
              ('mari2/enojo', 'advancement grant @a[tag=dv_talker] only canon:logros/mariana'),
              ('abuela/sopa', 'advancement grant @a[tag=dv_atalk] only canon:logros/abuela'),
              ('diana2/visita/fin', 'advancement grant @s only canon:logros/visita'), ('herr/taladora/romper', 'advancement grant @s only canon:logros/tala')]
    for path, line in grants:
        c.patch(path, lambda s, line=line: s if line in s else s.rstrip('\n') + '\n' + line + '\n')
    c.on('second', 'advancement grant @a[scores={dv.miedo=100..}] only canon:logros/miedo')
    # ----------------------------------------------------------- El Narrador
    nb, nh = SK.build_character('narrador', NARR, c.out, ('idle', 'walk_a', 'walk_b', 'reach'), [('neutral', 'flat'), ('ojos', 'glow')])
    shim.models(nb + nh, 7321060)
    K = shim.CMD
    F('para/narrador/summon', rig_summon(['dv_narrador'], 'El Narrador', '#9a9ab0') + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_narrador,distance=..2,limit=1,sort=nearest] at @s run function canon:para/narrador/init')
    F('para/narrador/init', f'''
function canon:rig/init_common
{set_cmd('body', K['narrador_idle'])}
{head(K['narrador_cabeza_neutral'])}
scoreboard players set @s dv.say -1
function canon:x/add_bubble
''')
    c.npc('dv_narrador', 'para/narrador/tick')
    c.pick('para/narrador/fa', [say('El Narrador', '#9a9ab0', '#e0e0ea', t, 200, '@a[distance=..24]') for t in FRAG])
    c.pick('para/narrador/fb', [say('El Narrador', '#9a9ab0', '#e0e0ea', t, 200, '@a[distance=..24]') for t in FRAG2])
    c.pick('para/narrador/fragmento', ['function canon:para/narrador/fa', 'function canon:para/narrador/fb'])
    F('para/narrador/tick', f'''
function canon:x/links_follow
scoreboard players remove @s[scores={{dv.say=1..}}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
tag @a[distance=..40,limit=1,sort=nearest] add dv_wtgt
execute if score #m4 dv.clock matches 0 run function canon:x/face
tag @a remove dv_wtgt
execute if score @s dv.timer matches 30 run function canon:para/narrador/fragmento
execute if score @s dv.timer matches 150 run {head(K['narrador_cabeza_ojos']).splitlines()[0]}
execute if score @s dv.timer matches 240.. run function canon:acecho/se_va
execute unless entity @a[distance=..64] run function canon:rig/despawn
''')
    c.on('second', 'execute if score #paranormal dv.cfg matches 1 unless entity @e[type=zombie,tag=dv_narrador] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:azar/1en2400 positioned ^ ^ ^12 run function canon:para/narrador/aparecer')
    F('para/narrador/aparecer', '''
scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:para/narrador/summon
kill @e[type=marker,tag=dv_spot]
''')
    F('admin/para/kit', '\n'.join(f'loot give @s loot canon:para/{x[0]}' for x in ITEMS))
    F('admin/para/narrador', 'execute positioned ^ ^ ^4 run function canon:para/narrador/summon')
    c.admin('/function canon:admin/para/kit', 'Todos los objetos paranormales')
    c.admin('/function canon:admin/para/narrador', 'Traer al Narrador')
