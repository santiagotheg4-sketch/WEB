"""Canon Event 6: arreglos (volver del sueño, cámara), páginas del diario de Diana, jefe final,
Don Severo (tienda paranormal), cuaderno, poltergeist de verdad, muñeca que vuelve, fotos en marcos,
casa de la Abuela Esmeralda y sus nietos, Mariana baila en tu ventana, Felipe y el final de Mariana,
el Mirón que se acerca, los Sin Rostro, el jardín secreto de Juli, Luna caza vacas/ovejas/pollos (y le teme a todo lo demás), noches anunciadas,
muertes distintas y rachas de supervivencia.
"""
from PIL import Image, ImageDraw
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon import skins as SK
from canon.ctx import item_nbt, loot_item
from features.personajes import MARI

PAG_CMD, CUAD_CMD, FOTO_CMD = 7311120, 7311121, 7312012
SEV, FEL = '#b9915a', '#8fa6c9'
SEVERO = dict(skin='#c9a284', hair='#9a9a9a', hair_style='short', eyes='#2a2a2a', brows='#888888', top='#6a4a2a', top_style='cardigan',
              pants='#3a3530', shoes='#2a2018', extras=['shawl', 'cap'], shawl='#8a5a2a', cap='#4a3a2a')
FELIPE = dict(skin='#d8c8bc', hair='#3a2a1e', hair_style='messy', eyes='#3a5a7a', top='#3b4a5e', top_style='jacket', top2='#d8d8d8',
              pants='#2a2f3a', shoes='#1a1a1a', extras=['dark_circles'])
NIETO = dict(skin='#e0b896', hair='#4a2e1a', hair_style='messy', eyes='#2a1a12', top='#c8a83a', top_style='tshirt', pants='#4a5a7a',
             pants_style='shorts', shoes='#5a3a2a', extras=['freckles'])
SINR = dict(skin='#cfc6bd', hair='#2a2a2a', hair_style='short', eyes='#cfc6bd', brows='#cfc6bd', lips='#cfc6bd', top='#3a3a40',
            top_style='long', pants='#2a2a30', shoes='#151515')

PAGINAS = [
    'Hoy conocí a Juan. Me prestó un lápiz y ni me miró. Lo guardé. Todavía huele a él.',
    'Juan se ríe con todos menos conmigo. Bana dice que no me haga ilusiones. Bana no entiende nada.',
    'En el bosque, debajo de un árbol que ayer no estaba, encontré un hueso blanco y tibio. Una viejita me miraba desde lejos.',
    'Dicen que el Hueso concede un deseo si lo partes pensando en alguien. Lo tengo debajo de la almohada. Late.',
    'Lo partí. Pedí que Juan me quisiera para siempre. Que no pudiera estar sin mí. Ni un minuto.',
    'Funcionó. Juan me escribe todo el día. Me espera afuera de la casa. Me mira dormir por la ventana. Era lo que quería, ¿no?',
    'Juan ya no come si no estoy. Dice que le duele la cabeza cuando me alejo. Su mamá lloró hoy en la puerta.',
    'Intenté deshacerlo. Pegué el hueso con cinta. No sirve. Juan se arrancó un mechón de pelo para dármelo.',
    'Juan pidió su propio deseo con lo que quedaba del Hueso: olvidarme. Ahora me mira y no sabe quién soy.',
    'Juan ya no me mira. Mira a través de mí, como si yo fuera una ventana sucia. Le sonríe a cualquiera menos a mí.',
    'Si él no me recuerda, voy a hacer que todos me recuerden. Mi cara en cada esquina. Mi nombre en cada radio.',
    'Algo con la cara roja me habla desde el otro lado. Dice que si le doy mi cuerpo, nunca me van a olvidar. Le dije que sí.',
    'Para terminar esto: de noche, con las trece páginas, abre el Libro de invocación y llama al de la cara roja. '
    'La sal, el agua bendita, la cruz de la abuela y el flash lo lastiman. Péguenle todos juntos.',
]
DESC = [  # clave, nombre, tags de entidad, texto del cuaderno
    ('juli', 'Juli', ['zombie,tag=dv_juli'], 'Duerme en algún lado y sueña con una casa blanca.'),
    ('dani', 'Dani', ['zombie,tag=dv_dani'], 'La hermana de Juli. Vende comida y pregunta si comiste.'),
    ('kevin', 'Kevin', ['zombie,tag=dv_kevin'], 'Llega, se queda y se va. Nunca dice a dónde.'),
    ('luna', 'Luna', ['wolf,tag=dv_luna'], 'Ladra a lo que tú no ves. Hazle caso.'),
    ('dhum', 'Diana (de día)', ['zombie,tag=dv_dhum'], 'Pálida, con ojeras. Pregunta por Juan.'),
    ('zunga', 'Diana (de noche)', ['zombie,tag=dv_as_zunga', 'zombie,tag=dv_zunga'], 'Se tuerce. Se arrastra. Sonríe demasiado.'),
    ('mariana', 'Mariana', ['zombie,tag=dv_mari2', 'zombie,tag=dv_mbaile'], 'Busca a Felipe. No le hables mucho.'),
    ('felipe', 'Felipe', ['zombie,tag=dv_felipe'], 'El ex de Mariana. Está demasiado pálido. Demasiado frío.'),
    ('abuela', 'Abuela Esmeralda', ['zombie,tag=dv_abuela'], 'La abuela de Santi. De día es ella. De noche, no.'),
    ('nietos', 'Los nietos', ['zombie,tag=dv_nieto'], 'Tomasito, Lucía y Pablito. Brillan un poquito.'),
    ('nicolas', 'Nicolás', ['zombie,tag=dv_nicolas', 'zombie,tag=dv_as_nicolas', 'zombie,tag=dv_as_nicolas2'], 'Vive en las cuevas. Se ríe.'),
    ('miron', 'El Mirón', ['zombie,tag=dv_miron', 'zombie,tag=dv_miracerca', 'zombie,tag=dv_as_miron'], 'Solo mira. Cada vez más cerca.'),
    ('sinrostro', 'Los Sin Rostro', ['zombie,tag=dv_sinrostro'], 'No tienen cara, pero te miran.'),
    ('imitador', 'El Imitador', ['zombie,tag=dv_imitador'], 'Se disfraza de animal.'),
    ('fantasma', 'Las almas', ['zombie,tag=dv_fantasma'], 'Perdidas. Algunas son amables.'),
    ('demonio', 'El de la cara roja', ['zombie,tag=dv_demonio', 'zombie,tag=dv_jefe'], 'Te caza en el Más Allá. Y a veces te sigue.'),
    ('narrador', 'El Narrador', ['zombie,tag=dv_narrador'], 'Sabe toda la historia. Cuenta pedacitos.'),
    ('severo', 'Don Severo', ['zombie,tag=dv_severo'], 'Vende cosas para lo que no se ve.'),
]
TIENDA = [('sal', 'Sal', 1), ('muneca', 'Muñeca', 1), ('agua_bendita', 'Agua bendita', 2), ('velas', 'Velas', 2), ('espejo', 'Espejo', 2),
          ('caja_musica', 'Caja de música', 3), ('grabadora', 'Grabadora', 3), ('radio_esp', 'Radio', 3), ('emf', 'EMF', 3),
          ('ouija', 'Ouija', 3), ('libro_inv', 'Libro de invocación', 5), ('pagina', 'Página del diario', 4)]
WOODS = ['oak', 'spruce', 'birch', 'jungle', 'acacia', 'dark_oak', 'mangrove', 'cherry', 'bamboo', 'crimson', 'warped']
BILL = 'minecraft:paper{canon:{id:"billete"}}'


def icon(path, c1, c2, lines=False):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([3, 2, 12, 14], fill=c1 + (255,), outline=tuple(max(0, v - 70) for v in c1) + (255,))
    if lines:
        for y in range(5, 13, 2):
            d.line([5, y, 10, y], fill=c2 + (255,))
    else:
        d.rectangle([5, 4, 10, 8], fill=c2 + (255,))
    im.save(path)


def build(c):
    shim.use(c)
    for o in ('dv.fel', 'dv.severo', 'dv.despertar'):
        c.objective(o, 'trigger')
    for o in ('dv.nietos', 'dv.luci', 'dv.racha', 'dv.rmuerte', 'dv.jvida', 'dv.jstun'):
        c.objective(o)
    c.objective('dv.muerte', 'deathCount')
    for n in (2, 12, 24, 75):
        c.const(n)
    c.json('data/canon/tags/entity_types/presas.json', {'values': [f'minecraft:{x}' for x in (
        'zombie', 'husk', 'drowned', 'skeleton', 'stray', 'spider', 'cave_spider', 'zombie_villager', 'pillager', 'vindicator', 'witch', 'silverfish')]})

    # ================================================================ ARREGLO: volver del sueño
    # El tp de regreso usaba la posición y la dimensión de quien llamaba la función: te mandaba al mundo normal
    # y en el mismo tick te devolvía al sueño (pantalla de carga infinita). Ahora cada paso es relativo al jugador.
    for ax in ('x', 'y', 'z'):
        for sg in ('pos', 'neg'):
            c.patch(f'util/tp_{ax}_{sg}', lambda s: s.replace(' run tp @s ~', ' at @s run tp @s ~'))
    c.patch('util/tp_return_known', lambda s: s.replace('\ntp @s ~0.5 ~ ~0.5', '\nexecute at @s run tp @s ~0.5 ~ ~0.5'))
    # la cámara se fija desde los ojos (antes desde los pies: quedaba mirando por encima de la cabeza)
    c.patch('juli/scene/look', lambda s: s if 'anchored eyes' in s else s.replace('tp @s ~ ~ ~ facing', 'execute anchored eyes run tp @s ~ ~ ~ facing'))
    c.patch('diana/par/tick', lambda s: s if 'anchored eyes run tp @s ~ ~ ~ facing' in s else
            s.replace('run tp @s ~ ~ ~ facing entity @e[type=marker,tag=dv_dl_me', 'anchored eyes run tp @s ~ ~ ~ facing entity @e[type=marker,tag=dv_dl_me'))
    despierta = 'tellraw @s ["",{"text":"[ Despertar ya ]","color":"#f2a7c3","bold":true,"clickEvent":{"action":"run_command","value":"/trigger dv.despertar set 1"}}]'
    for f in ('sueno/arrived', 'casa/enter'):
        c.patch(f, lambda s: s if 'dv.despertar' in s else s.rstrip('\n') + '\n' + despierta + '\n')
    c.on('player', '''
scoreboard players enable @s dv.despertar
execute if score @s dv.despertar matches 1.. run function canon:rel/despertar
scoreboard players enable @s dv.fel
scoreboard players enable @s dv.severo
execute if score @s dv.fel matches 1.. run function canon:rel/felipe/eleccion
execute if score @s dv.severo matches 1.. run function canon:rel/severo/comprar
execute if score @s dv.muerte matches 1.. run function canon:rel/muerte
execute unless entity @s[tag=dv_cuad] run function canon:rel/cuaderno/dar
''')
    F('rel/despertar', '''
scoreboard players set @s dv.despertar 0
execute if predicate canon:en_sueno run function canon:sueno/wake
execute if dimension canon:sueno_blanco run function canon:casa/wake
''')

    # ================================================================ modelos nuevos
    def char(prefix, cfg, poses, exprs, start):
        b, h = SK.build_character(prefix, cfg, c.out, poses, exprs)
        shim.models(b + h, start)
    char('severo', SEVERO, ('idle', 'walk_a', 'walk_b', 'offer'), [('sonrisa', 'smile'), ('raro', 'creepy')], 7321070)
    char('felipe', FELIPE, ('idle', 'walk_a', 'walk_b', 'reach', 'dance_a', 'dance_b'), [('triste', 'sad'), ('sonrisa', 'soft')], 7321080)
    char('nieto', NIETO, ('idle', 'walk_a', 'walk_b', 'arms_up'), [('sonrisa', 'smile'), ('triste', 'sad')], 7321090)
    char('sinrostro', SINR, ('idle', 'point'), [('liso', 'nada')], 7321100)
    char('mariana3', MARI, ('dance_a', 'dance_b', 'arms_up', 'twist'), [('creepy', 'creepy')], 7321110)
    K = shim.CMD

    def rig(prefix, tag, name, color, body, hd, tags=(), scale=1.0, click=None, bubble=True, h=1.9):
        F(f'{prefix}/summon', rig_summon([tag, *tags], name, color, head=hd is not None, scale=scale) + '\n'
          f'execute as @e[type=zombie,tag=dv_new,tag={tag},distance=..2,limit=1,sort=nearest] at @s run function canon:{prefix}/init')
        link = ''
        if click:
            link = (f'summon minecraft:interaction ~ ~ ~ {{Tags:["dv_link","dv_click","dv_npc_click","dv_xclick","{click}","dv_new_link"],'
                    f'width:{0.8 * scale:.2f}f,height:{h * scale:.2f}f,response:1b}}\n'
                    'scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id\ntag @e[tag=dv_new_link] remove dv_new_link\n')
        F(f'{prefix}/init', 'function canon:rig/init_common\n' + set_cmd('body', body) + '\n' + (head(hd) + '\n' if hd else '') +
          'scoreboard players operation @s dv.target = #pid dv.tmp\nscoreboard players set @s dv.say -1\nscoreboard players set @s dv.state 0\n'
          'scoreboard players set @s dv.timer 0\nscoreboard players set @s dv.mode 0\n' + link + ('function canon:x/add_bubble' if bubble else ''))

    HEAD = '''function canon:x/links_follow
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
tag @a remove dv_wtgt
scoreboard players operation #tgt dv.tmp = @s dv.target
execute as @a[distance=..64] if score @s dv.pid = #tgt dv.tmp run tag @s add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run tag @a[distance=..40,gamemode=!spectator,limit=1,sort=nearest] add dv_wtgt
'''

    def tick(prefix, tag, body):
        c.npc(tag, f'{prefix}/tick')
        F(f'{prefix}/tick', HEAD + f'execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn\n'
          f'execute if entity @a[tag=dv_wtgt] run function canon:{prefix}/piensa\ntag @a remove dv_wtgt')
        F(f'{prefix}/piensa', body)

    def spot(fn, pos='~ ~ ~'):
        return (f'scoreboard players set #ok dv.tmp 0\nexecute positioned {pos} run function canon:util/spot_search\n'
                f'execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:{fn}\nkill @e[type=marker,tag=dv_spot]')
    WALKF = '''scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
'''

    # ================================================================ PÁGINAS DEL DIARIO DE DIANA + CUADERNO
    icon(c.path('assets/canon/textures/item/r_pagina.png'), (232, 218, 190), (120, 100, 90), True)
    icon(c.path('assets/canon/textures/item/r_cuaderno.png'), (110, 70, 40), (232, 218, 190))
    for iid, cmd in (('pagina', PAG_CMD), ('cuaderno', CUAD_CMD)):
        c.json(f'assets/canon/models/item/r_{iid}.json', {'parent': 'minecraft:item/handheld_rod', 'textures': {'layer0': f'canon:item/r_{iid}'}})
        c.item_model('carrot_on_a_stick', cmd, f'canon:item/r_{iid}')
    for n in range(1, 14):
        c.json(f'data/canon/loot_tables/rel/pag/p{n}.json', loot_item('carrot_on_a_stick', item_nbt(
            'pagina', f'Diario de Diana — página {n}/13', '#e8c9a8', ['Clic derecho para leerla.'], PAG_CMD, f'pag:{n}')))
    c.json('data/canon/loot_tables/rel/cuaderno.json', loot_item('carrot_on_a_stick', item_nbt(
        'cuaderno', 'Cuaderno de investigación', '#c9a46a', ['Clic derecho: todo lo que has descubierto.'], CUAD_CMD)))
    c.json('data/canon/loot_tables/rel/foto_vieja.json', loot_item('paper', item_nbt(
        'foto_vieja', 'Foto vieja', '#ece8de', ['Tres niños frente a la casa de la abuela.', 'Uno no tiene cara.'], FOTO_CMD)))
    c.json('data/canon/loot_tables/rel/hueso.json', loot_item('bone', item_nbt(
        'hueso', 'Hueso de los Deseos (apagado)', 'gold', ['Ya no late.', 'Lo lograron.'], None, 'Enchantments:[{id:"minecraft:unbreaking",lvl:1s}]')))
    c.use_item('pagina', 'rel/pag/leer', cooldown=True)
    c.use_item('cuaderno', 'rel/cuaderno/ver', cooldown=True)
    leer = ['scoreboard players set @s dv.cool 10', 'execute store result score #pg dv.tmp run data get entity @s SelectedItem.tag.pag',
            'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1']
    for n, t in enumerate(PAGINAS, 1):
        F(f'rel/pag/t{n}', f'tellraw @s ["",{jt(f"— Diario de Diana, página {n} —", "#c94a4a", bold=True)},{jt(chr(10) + t, "#e8c9a8", True)}]\ntag @s add dv_pag{n}')
        leer.append(f'execute if score #pg dv.tmp matches {n} run function canon:rel/pag/t{n}')
    leer.append('function canon:rel/pag/contar')
    F('rel/pag/leer', '\n'.join(leer))
    F('rel/pag/contar', 'scoreboard players set #pc dv.tmp 0\n' + '\n'.join(f'execute if entity @s[tag=dv_pag{n}] run scoreboard players add #pc dv.tmp 1' for n in range(1, 14)) +
      '\ntitle @s actionbar ["",{"text":"Páginas del diario: ","color":"#e8c9a8"},{"score":{"name":"#pc","objective":"dv.tmp"},"color":"white"},{"text":"/13","color":"#e8c9a8"}]'
      '\nexecute if score #pc dv.tmp matches 13 unless entity @s[tag=dv_pagtodas] run function canon:rel/pag/completo')
    F('rel/pag/completo', '''
tag @s add dv_pagtodas
advancement grant @s only canon:logros/paginas
tellraw @a ["",{"text":"☾ ","color":"#c94a4a"},{"selector":"@s","color":"gold"},{"text":" juntó las 13 páginas del diario de Diana. La última dice cómo terminar esto.","color":"#c94a4a","italic":true}]
execute unless score #jefe_ganado dv.dev matches 1 unless score #an_ev dv.dev matches 20 run function canon:rel/noches/demonio
''')
    sig = ['scoreboard players set #pn dv.tmp 0'] + [f'execute if score #pn dv.tmp matches 0 unless entity @s[tag=dv_pag{n}] run scoreboard players set #pn dv.tmp {n}' for n in range(1, 14)]
    F('rel/pag/siguiente', '\n'.join(sig))
    F('rel/pag/dar', 'function canon:rel/pag/siguiente\n' + '\n'.join(
        f'execute if score #pn dv.tmp matches {n} run loot give @s loot canon:rel/pag/p{n}\nexecute if score #pn dv.tmp matches {n} run tag @s add dv_pag{n}' for n in range(1, 14)) +
      '\nexecute if score #pn dv.tmp matches 0 run loot give @s loot canon:items/billete')
    F('rel/pag/dar_aviso', 'function canon:rel/pag/dar\ntellraw @s {"text":"Te dieron una página arrancada de un diario. La letra es de Diana.","color":"#e8c9a8","italic":true}')
    F('rel/pag/suelo', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nfunction canon:rel/pag/siguiente\n' + spot('rel/pag/suelo2', '^ ^ ^10'))
    F('rel/pag/suelo2', '\n'.join(f'execute if score #pn dv.tmp matches {n} run loot spawn ~ ~0.5 ~ loot canon:rel/pag/p{n}' for n in range(1, 14)) +
      '\nexecute as @e[type=item,distance=..1.5] run data merge entity @s {Glowing:1b}\nparticle minecraft:enchant ~ ~1 ~ 0.3 0.5 0.3 0.5 40 normal')
    c.on('second', 'execute if score #paranormal dv.cfg matches 1 as @a[gamemode=!spectator,predicate=canon:en_superficie] at @s if predicate canon:de_noche if predicate canon:azar/1en1500 run function canon:rel/pag/suelo')
    for path in ('para/narrador/fragmento', 'para/mision/cumplida'):
        c.patch(path, lambda s: s if 'rel/pag/dar_aviso' in s else s.rstrip('\n') +
                '\nexecute if predicate canon:azar/1en2 as @p[distance=..24] run function canon:rel/pag/dar_aviso\n')
    c.patch('para/luna_tesoro', lambda s: s if 'rel/pag' in s else s.rstrip('\n') + '\nexecute if predicate canon:azar/1en4 as @p[distance=..16] run function canon:rel/pag/dar_aviso\n')
    # cuaderno
    F('rel/cuaderno/dar', 'tag @s add dv_cuad\nloot give @s loot canon:rel/cuaderno')
    ver = ['scoreboard players set @s dv.cool 20', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.9',
           'tellraw @s {"text":"\\n☾ CUADERNO DE INVESTIGACIÓN","color":"#c9a46a","bold":true}']
    grants = []
    for key, nom, sels, txt in DESC:
        c.json(f'data/canon/advancements/cuaderno/{key}.json', {'parent': 'canon:logros/raiz', 'display': {
            'icon': {'item': 'minecraft:writable_book'}, 'title': {'text': 'Cuaderno: ' + nom, 'color': '#c9a46a'}, 'description': {'text': txt},
            'frame': 'task', 'show_toast': True, 'announce_to_chat': False, 'hidden': True}, 'criteria': {'c': {'trigger': 'minecraft:impossible'}}})
        ver.append(f'execute if entity @s[advancements={{canon:cuaderno/{key}=true}}] run tellraw @s ["",{jt(" ✔ " + nom + ": ", "#e8c9a8")},{jt(txt, "gray", True)}]')
        ver.append(f'execute unless entity @s[advancements={{canon:cuaderno/{key}=true}}] run tellraw @s {jt(" • ???", "dark_gray")}')
        for sel in sels:
            grants.append(f'execute as @e[type={sel}] at @s run advancement grant @a[distance=..12] only canon:cuaderno/{key}')
    ver.append('function canon:rel/pag/contar')
    F('rel/cuaderno/ver', '\n'.join(ver))
    F('rel/cuaderno/descubrir', '\n'.join(grants))
    c.on('second', 'execute if score #m4 dv.clock matches 0..19 run function canon:rel/cuaderno/descubrir')
    c.json('data/canon/recipes/r_cuaderno.json', {'type': 'minecraft:crafting_shapeless', 'category': 'misc', 'ingredients': [
        {'item': 'minecraft:book'}, {'item': 'minecraft:feather'}, {'item': 'minecraft:ink_sac'}], 'result': {'item': 'minecraft:knowledge_book', 'count': 1}})
    c.json('data/canon/advancements/rel/receta_cuaderno.json', {'criteria': {'c': {'trigger': 'minecraft:recipe_crafted', 'conditions': {
        'recipe_id': 'canon:r_cuaderno'}}}, 'rewards': {'function': 'canon:rel/cuaderno/craft'}})
    F('rel/cuaderno/craft', 'clear @s minecraft:knowledge_book 1\nloot give @s loot canon:rel/cuaderno\nadvancement revoke @s only canon:rel/receta_cuaderno')

    # ================================================================ LOGROS NUEVOS
    for lid, tit, desc, ic, frame in [('paginas', 'El diario completo', 'Junta las 13 páginas del diario de Diana.', 'minecraft:paper', 'goal'),
                                      ('jefe', 'Lo que tenía que pasar', 'Derrota al de la cara roja.', 'minecraft:bone', 'challenge'),
                                      ('felipe', 'La última canción', 'Lleva a Felipe con Mariana.', 'minecraft:music_disc_11', 'goal'),
                                      ('nietos', 'Ya pueden descansar', 'Encuentra a los tres nietos de la abuela.', 'minecraft:candle', 'goal'),
                                      ('jardin', 'Lugar secreto', 'Atrapa las cinco luciérnagas del jardín de Juli.', 'minecraft:pink_tulip', 'task'),
                                      ('racha', 'Diez noches', 'Sobrevive 10 noches seguidas sin morir.', 'minecraft:clock', 'challenge')]:
        c.json(f'data/canon/advancements/logros/{lid}.json', {'parent': 'canon:logros/raiz', 'display': {
            'icon': {'item': ic}, 'title': {'text': tit, 'color': '#d77a8a'}, 'description': {'text': desc}, 'frame': frame,
            'show_toast': True, 'announce_to_chat': True, 'hidden': False}, 'criteria': {'c': {'trigger': 'minecraft:impossible'}}})

    # ================================================================ JEFE FINAL: el de la cara roja
    c.on('load', 'bossbar add canon:jefe {"text":"El de la cara roja","color":"dark_red"}\nbossbar set canon:jefe color red\nbossbar set canon:jefe style notched_10')
    rig('rel/jefe', 'dv_jefe', 'El de la cara roja', '#8b0000', 7321040, 7321046, scale=1.6, click='dv_jefe_click', h=2.0)
    c.patch('rel/jefe/init', lambda s: s.rstrip('\n') + '''
execute store result score #np dv.tmp if entity @a[distance=..96,gamemode=!spectator]
scoreboard players operation @s dv.jvida = #np dv.tmp
scoreboard players operation @s dv.jvida *= #75 dv.math
scoreboard players add @s dv.jvida 150
scoreboard players operation #jmax dv.dev = @s dv.jvida
scoreboard players operation #jmitad dv.dev = @s dv.jvida
scoreboard players operation #jmitad dv.dev /= #2 dv.math
execute store result bossbar canon:jefe max run scoreboard players get #jmax dv.dev
scoreboard players set @s dv.jstun 0
''')
    c.brain_click('dv_jefe_click', 'zombie', 'dv_jefe', 'rel/jefe/clic', 'rel/jefe/golpe')
    c.frames('dv_jefe', 'rel/jefe/frames')
    F('rel/jefe/frames', '''scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 4
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 5
execute if score @s dv.cool matches 22.. run scoreboard players set #frame dv.tmp 3''')
    js = lambda t: say('El de la cara roja', '#8b0000', '#ffb0b0', t, 80, '@a[distance=..40]')
    c.npc('dv_jefe', 'rel/jefe/tick')
    F('rel/jefe/tick', '''function canon:x/links_follow
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
scoreboard players remove @s[scores={dv.jstun=1..}] dv.jstun 1
scoreboard players remove @s[scores={dv.cool=1..}] dv.cool 1
tag @a remove dv_wtgt
tag @a[distance=..64,gamemode=!spectator,gamemode=!creative,limit=1,sort=nearest] add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run scoreboard players add @s dv.watch 1
execute if entity @a[tag=dv_wtgt] run scoreboard players set @s dv.watch 0
execute if entity @a[tag=dv_wtgt] run function canon:rel/jefe/piensa
tag @a remove dv_wtgt
execute if score @s dv.watch matches 1200.. run function canon:rel/jefe/se_va''')
    F('rel/jefe/piensa', '''
execute if score #m2 dv.clock matches 0 run function canon:x/face
execute if score @s dv.jstun matches 1.. run particle minecraft:electric_spark ~ ~2.8 ~ 0.4 0.3 0.4 0 3 normal
execute unless score @s dv.jstun matches 1.. unless entity @a[tag=dv_wtgt,distance=..2.4] run function canon:x/walk
execute unless score @s dv.jstun matches 1.. if entity @s[tag=dv_jfuria] unless entity @a[tag=dv_wtgt,distance=..2.4] run function canon:x/walk_slow
execute unless score @s dv.jstun matches 1.. if entity @a[tag=dv_wtgt,distance=..2.8] unless score @s dv.cool matches 1.. run function canon:rel/jefe/ataca
execute if score @s dv.timer matches 400.. run function canon:rel/jefe/especial
''')
    F('rel/jefe/ataca', '''
scoreboard players set @s dv.cool 30
damage @a[tag=dv_wtgt,limit=1] 7 minecraft:mob_attack by @s
playsound minecraft:entity.ravager.attack hostile @a[distance=..16] ~ ~ ~ 1 0.7
scoreboard players add @a[tag=dv_wtgt] dv.miedo 5
''')
    F('rel/jefe/especial', 'scoreboard players set @s dv.timer 0\nfunction canon:rel/jefe/esp')
    c.pick('rel/jefe/esp', [
        js('¡NADIE ME VA A OLVIDAR!') + '\nplaysound canon:diana.scream hostile @a[distance=..32] ~ ~ ~ 1 0.5\neffect give @a[distance=..24] minecraft:darkness 5 0 true',
        js('Vengan, mis muertos.') + '\nsummon minecraft:zombie ~2 ~ ~ {Tags:["dv_zinit"]}\nsummon minecraft:zombie ~-2 ~ ~ {Tags:["dv_zinit"]}\nsummon minecraft:zombie ~ ~ ~2 {Tags:["dv_zinit"]}\nparticle minecraft:soul ~ ~1 ~ 2 0.5 2 0.02 40 normal',
        'execute at @a[tag=dv_wtgt,limit=1] rotated ~ 0 positioned ^ ^ ^-3 run function canon:rel/jefe/detras',
        js('Diana me dio su cuerpo. Ustedes me van a dar el suyo.') + '\neffect give @a[distance=..20] minecraft:slowness 4 1 true',
    ])
    F('rel/jefe/detras', '''
scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 as @e[type=zombie,tag=dv_jefe,limit=1,sort=nearest] run tp @s @e[type=marker,tag=dv_spot,limit=1]
kill @e[type=marker,tag=dv_spot]
title @a[tag=dv_wtgt] times 0 20 10
title @a[tag=dv_wtgt] title {"text":"DETRÁS DE TI","color":"dark_red","bold":true}
playsound canon:diana.jumpscare hostile @a[tag=dv_wtgt] ~ ~ ~ 0.8 0.6
''')
    F('rel/jefe/clic', 'tellraw @a[tag=dv_talker] {"text":"Golpéalo. Solo le duelen las cosas benditas: agua bendita, sal, la cruz de la abuela y el flash de la cámara.","color":"gray","italic":true}')
    F('rel/jefe/golpe', 'scoreboard players set #dmg dv.tmp 4\nexecute if entity @a[tag=dv_talker,predicate=canon:mano/crucifijo] run scoreboard players set #dmg dv.tmp 12\nfunction canon:rel/jefe/dano')
    for nm, dmg, stun in (('agua', 25, 40), ('cruz', 15, 60), ('flash', 6, 50), ('sal', 3, 25)):
        F(f'rel/jefe/{nm}', f'scoreboard players set #dmg dv.tmp {dmg}\nscoreboard players set @s dv.jstun {stun}\nfunction canon:rel/jefe/dano')
    c.patch('camara/disparar', lambda s: s if 'rel/jefe/flash' in s else s.rstrip('\n') + '\nexecute as @e[type=zombie,tag=dv_jefe,distance=..20] at @s run function canon:rel/jefe/flash\n')
    c.patch('extras/cruz', lambda s: s if 'rel/jefe/cruz' in s else s.rstrip('\n') + '\nexecute as @e[type=zombie,tag=dv_jefe,distance=..10] at @s run function canon:rel/jefe/cruz\n')
    F('rel/jefe/dano', '''
scoreboard players operation @s dv.jvida -= #dmg dv.tmp
particle minecraft:damage_indicator ~ ~2.5 ~ 0.4 0.4 0.4 0.1 6 normal
playsound minecraft:entity.ravager.hurt hostile @a[distance=..24] ~ ~ ~ 1 0.6
execute if score @s dv.jvida <= #jmitad dv.dev unless entity @s[tag=dv_jfuria] run function canon:rel/jefe/furia
execute if score @s dv.jvida matches ..0 run function canon:rel/jefe/muerte
''')
    F('rel/jefe/furia', 'tag @s add dv_jfuria\n' + head(7321047) + '\ntitle @a[distance=..48] times 5 40 10\ntitle @a[distance=..48] title {"text":"¡ESTÁ FURIOSO!","color":"dark_red","bold":true}\n'
      + js('¿Creen que pueden olvidarla? ¡YO SOY ELLA AHORA!'))
    F('rel/jefe/muerte', '''
particle minecraft:soul_fire_flame ~ ~1.5 ~ 1 2 1 0.1 200 force
particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1 force
playsound minecraft:entity.wither.death hostile @a[distance=..64] ~ ~ ~ 1 0.8
title @a[distance=..96] times 20 100 40
title @a[distance=..96] subtitle {"text":"Diana por fin puede descansar.","color":"#f2a7c3","italic":true}
title @a[distance=..96] title {"text":"LO LOGRARON","color":"gold","bold":true}
tellraw @a {"text":"☾ El de la cara roja volvió al Más Allá. El Hueso de los Deseos dejó de latir.","color":"gold","italic":true}
loot give @a[distance=..96] loot canon:rel/hueso
advancement grant @a[distance=..96] only canon:logros/jefe
scoreboard players set #jefe_ganado dv.dev 1
scoreboard players set @a dv.demsig 0
bossbar set canon:jefe players
schedule function canon:rel/jefe/epilogo 200t
function canon:rig/despawn
''')
    F('rel/jefe/epilogo', '''
tellraw @a ["",{"text":"Juli: ","color":"#f2a7c3","bold":true},{"text":"Santi... ya me puedo despertar. Nos vemos del otro lado. Gracias por no dejar de buscarme.","color":"#fde3ee","italic":true}]
tellraw @a ["",{"text":"Diana: ","color":"#c94a4a","bold":true},{"text":"Juan... no tienes que recordarme. Solo no me odies. Adiós.","color":"#e8c9a8","italic":true}]
playsound canon:juli.chime ambient @a ~ ~ ~ 1 1
''')
    F('rel/jefe/se_va', 'tellraw @a[distance=..128] {"text":"El de la cara roja se cansó de esperar. Volverá.","color":"#8b0000","italic":true}\nbossbar set canon:jefe players\nfunction canon:rig/despawn')
    c.on('second', '''
execute as @e[type=zombie,tag=dv_jefe,limit=1] at @s run bossbar set canon:jefe players @a[distance=..96]
execute as @e[type=zombie,tag=dv_jefe,limit=1] store result bossbar canon:jefe value run scoreboard players get @s dv.jvida
execute unless entity @e[type=zombie,tag=dv_jefe] run bossbar set canon:jefe players
execute as @e[type=marker,tag=dv_sal] at @s as @e[type=zombie,tag=dv_jefe,distance=..5] at @s run function canon:rel/jefe/sal
''')
    F('rel/jefe/invocar', '''
execute unless entity @s[tag=dv_pagtodas] run tellraw @s {"text":"El libro no responde. Te faltan páginas del diario de Diana.","color":"gray","italic":true}
execute if entity @s[tag=dv_pagtodas] unless predicate canon:de_noche run tellraw @s {"text":"Solo se le puede llamar de noche.","color":"gray","italic":true}
execute if entity @s[tag=dv_pagtodas] if predicate canon:de_noche if entity @e[type=zombie,tag=dv_jefe] run tellraw @s {"text":"Ya está aquí.","color":"#8b0000","italic":true}
execute if entity @s[tag=dv_pagtodas] if predicate canon:de_noche unless entity @e[type=zombie,tag=dv_jefe] run function canon:rel/jefe/forzar
''')
    F('rel/jefe/forzar', 'scoreboard players operation #pid dv.tmp = @s dv.pid\n' + spot('rel/jefe/llega', '^ ^ ^12'))
    F('rel/jefe/llega', '''
function canon:rel/jefe/summon
particle minecraft:large_smoke ~ ~1 ~ 1 2 1 0.05 120 force
playsound minecraft:entity.wither.spawn hostile @a[distance=..96] ~ ~ ~ 1 0.6
title @a[distance=..96] times 10 60 20
title @a[distance=..96] subtitle {"text":"Agua bendita, sal, la cruz de la abuela y el flash. Todos juntos.","color":"gray","italic":true}
title @a[distance=..96] title {"text":"EL DE LA CARA ROJA","color":"dark_red","bold":true}
''')
    F('rel/jefe/noche', '''
execute as @a[gamemode=!spectator,gamemode=!creative,predicate=canon:en_superficie,limit=1,sort=random] at @s run function canon:rel/jefe/forzar
execute unless entity @e[type=zombie,tag=dv_jefe] run scoreboard players set #an_ev dv.dev 20
''')

    # ================================================================ NOCHES ANUNCIADAS
    NOCHES = {1: 'la Luna de Sangre', 3: 'la Noche de Diana', 6: 'la Noche del Mirón', 12: 'el Gran Apagón', 20: 'la Noche del Demonio'}
    c.on('second', '''
execute store result score #hd dv.tmp run time query daytime
execute store result score #hday dv.tmp run time query day
execute if score #hd dv.tmp matches 1000..1100 unless score #an_dia dv.dev = #hday dv.tmp run function canon:rel/noches/manana
execute if score #an_ev dv.dev matches 1.. if score #an_falta dv.dev matches ..0 if score #hd dv.tmp matches 12500..12600 run function canon:rel/noches/empieza
execute if score #hd dv.tmp matches 0..40 unless score #racha_dia dv.dev = #hday dv.tmp run function canon:rel/racha/amanecer
''')
    F('rel/noches/manana', '''
scoreboard players operation #an_dia dv.dev = #hday dv.tmp
execute if score #an_ev dv.dev matches 1.. if score #an_falta dv.dev matches 1.. run scoreboard players remove #an_falta dv.dev 1
execute if score #an_ev dv.dev matches 1.. run function canon:rel/noches/anuncio
execute if score #an_ev dv.dev matches 1.. if score #an_falta dv.dev matches ..0 run scoreboard players operation #dir_day dv.dev = #hday dv.tmp
execute unless score #an_ev dv.dev matches 1.. if score #hday dv.tmp matches 2.. if score #paranormal dv.cfg matches 1 if predicate canon:azar/1en3 run function canon:rel/noches/planear
''')
    c.pick('rel/noches/elegir', [f'scoreboard players set #an_ev dv.dev {k}' for k in (1, 3, 6, 12)])
    F('rel/noches/planear', 'function canon:rel/noches/elegir\nscoreboard players set #an_falta dv.dev 3\nfunction canon:rel/noches/anuncio')
    F('rel/noches/demonio', 'scoreboard players set #an_ev dv.dev 20\nscoreboard players set #an_falta dv.dev 3\nfunction canon:rel/noches/anuncio')
    an = []
    for k, nom in NOCHES.items():
        an.append(f'execute if score #an_ev dv.dev matches {k} if score #an_falta dv.dev matches 1.. run tellraw @a ["",{jt("☾ Faltan ", "#d77a8a")},'
                  f'{{"score":{{"name":"#an_falta","objective":"dv.dev"}},"color":"white","bold":true}},{jt(" días para " + nom + ".", "#d77a8a")}]')
        an.append(f'execute if score #an_ev dv.dev matches {k} if score #an_falta dv.dev matches ..0 run title @a subtitle {jt(nom.upper(), "#c94a4a", bold=True)}')
    an += ['execute if score #an_falta dv.dev matches ..0 run title @a title {"text":"ESTA NOCHE","color":"#d77a8a"}',
           'playsound minecraft:block.bell.use ambient @a ~ ~ ~ 0.5 0.6']
    F('rel/noches/anuncio', '\n'.join(an))
    F('rel/noches/empieza', '''
scoreboard players operation #ane dv.tmp = #an_ev dv.dev
scoreboard players set #an_ev dv.dev 0
execute if score #ane dv.tmp matches 20 run function canon:rel/jefe/noche
execute unless score #ane dv.tmp matches 20 if score #canon_ev dv.dev matches 0 run function canon:rel/noches/director
''')
    F('rel/noches/director', 'scoreboard players operation #pick dv.tmp = #ane dv.tmp\nfunction canon:director/empezar')

    # ================================================================ MUERTES DISTINTAS + RACHAS
    MU = {0: ('TE MORISTE', 'Alguien lo anotó en su diario.', ' murió. Algo lo vio todo desde lejos.'),
          1: ('TE LLEVÓ', 'Al Más Allá.', ' fue arrastrado al Más Allá por el de la cara roja.'),
          2: ('TE ENCONTRÉ', 'Diana sonríe.', ' fue arrastrado debajo de la cama por Diana.'),
          3: ('QUÉ NIETO TAN RICO', 'La abuela de noche no es la abuela.', ' recibió la última sopita de la Abuela Esmeralda.'),
          4: ('QUÉDATE CONMIGO', 'Nicolás ya no está solo.', ' se quedó con Nicolás en la mina.'),
          5: ('NO MIRASTE', 'El de la cara roja corre cuando no lo miras.', ' fue cazado en el Más Allá.'),
          6: ('NO HABÍA LUZ', 'La oscuridad muerde.', ' fue mordido por la oscuridad. Debió llevar una antorcha.'),
          7: ('NO LAS MIRASTE', 'Se acercan cuando no las miras.', ' fue envuelto por las arañas.'),
          8: ('TE ALCANZARON', 'Los muertos de Valle Quieto tienen hambre.', ' fue devorado por los muertos de Valle Quieto.'),
          9: ('AHORA SOY TÚ', '¿Cuál es el de verdad?', ' fue imitado por el Imitador. Ahora hay dos.')}
    F('rel/muerte', '''
scoreboard players set @s dv.muerte 0
scoreboard players set @s dv.racha 0
scoreboard players set @s dv.rmuerte 1
scoreboard players set #mk dv.tmp 0
execute if entity @e[type=zombie,tag=!dv_brain,distance=..6] run scoreboard players set #mk dv.tmp 8
execute if entity @e[type=#canon:aranas,distance=..6] run scoreboard players set #mk dv.tmp 7
execute if score #mk dv.tmp matches 0 if predicate canon:oscuro run scoreboard players set #mk dv.tmp 6
execute if entity @e[type=zombie,tag=dv_demonio,distance=..20] run scoreboard players set #mk dv.tmp 5
execute if entity @e[type=zombie,tag=dv_nicolas,distance=..16] run scoreboard players set #mk dv.tmp 4
execute if entity @e[type=zombie,tag=dv_as_nicolas,distance=..16] run scoreboard players set #mk dv.tmp 4
execute if entity @e[type=zombie,tag=dv_abuela,distance=..10] run scoreboard players set #mk dv.tmp 3
execute if entity @e[type=zombie,tag=dv_zunga,distance=..16] run scoreboard players set #mk dv.tmp 2
execute if entity @e[type=zombie,tag=dv_as_zunga,distance=..16] run scoreboard players set #mk dv.tmp 2
execute if entity @e[type=zombie,tag=dv_imitador,distance=..8] run scoreboard players set #mk dv.tmp 9
execute if entity @e[type=zombie,tag=dv_jefe,distance=..24] run scoreboard players set #mk dv.tmp 1
title @s times 5 80 20
''' + '\n'.join(f'execute if score #mk dv.tmp matches {k} run function canon:rel/muerte/m{k}' for k in MU))
    c.json('data/canon/tags/entity_types/aranas.json', {'values': ['minecraft:spider', 'minecraft:cave_spider']})
    for k, (t, sub, msg) in MU.items():
        F(f'rel/muerte/m{k}', f'title @s subtitle {jt(sub, "gray", True)}\ntitle @s title {jt(t, "dark_red", bold=True)}\n'
          f'tellraw @a ["",{jt("☠ ", "dark_red")},{{"selector":"@s","color":"#e8c9a8"}},{jt(msg, "#c94a4a", True)}]\nplaysound canon:fx.stinger master @s ~ ~ ~ 0.8 0.6')
    F('rel/racha/amanecer', '''
scoreboard players operation #racha_dia dv.dev = #hday dv.tmp
execute as @a[gamemode=!spectator] unless score @s dv.rmuerte matches 1 run function canon:rel/racha/sube
scoreboard players set @a dv.rmuerte 0
''')
    F('rel/racha/sube', '''
scoreboard players add @s dv.racha 1
title @s actionbar ["",{"text":"☀ Sobreviviste la noche. Racha: ","color":"#ffd27a"},{"score":{"name":"@s","objective":"dv.racha"},"color":"white","bold":true}]
execute if score @s dv.racha matches 3 run function canon:rel/racha/p3
execute if score @s dv.racha matches 5 run function canon:rel/racha/p5
execute if score @s dv.racha matches 7 run function canon:rel/racha/p7
execute if score @s dv.racha matches 10 run function canon:rel/racha/p10
''')
    rmsg = lambda n: f'tellraw @a ["",{jt("☀ ", "#ffd27a")},{{"selector":"@s","color":"gold"}},{jt(f" lleva {n} noches seguidas sin morir. Las noches se ponen más difíciles.", "gray", True)}]'
    F('rel/racha/p3', rmsg(3) + '\nloot give @s loot canon:para/sal\nloot give @s loot canon:para/agua_bendita')
    F('rel/racha/p5', rmsg(5) + '\nloot give @s loot canon:extras/crucifijo\nfunction canon:rel/pag/dar_aviso')
    F('rel/racha/p7', rmsg(7) + '\nloot give @s loot canon:para/caja_musica\nloot give @s loot canon:items/billete\nloot give @s loot canon:items/billete\nloot give @s loot canon:items/billete')
    F('rel/racha/p10', rmsg(10) + '\ngive @s minecraft:diamond 3\nadvancement grant @s only canon:logros/racha')
    c.on('second', '''
execute as @a[scores={dv.racha=3..}] at @s if predicate canon:de_noche run effect give @e[type=zombie,tag=!dv_brain,distance=..32] minecraft:speed 3 0 true
execute as @a[scores={dv.racha=6..}] at @s if predicate canon:de_noche run effect give @e[type=zombie,tag=!dv_brain,distance=..32] minecraft:strength 3 0 true
''')

    # ================================================================ DON SEVERO (tienda paranormal)
    rig('rel/sev', 'dv_severo', 'Don Severo', SEV, K['severo_idle'], K['severo_cabeza_sonrisa'], ['dv_humano'], click='dv_sev_click')
    c.brain_click('dv_sev_click', 'zombie', 'dv_severo', 'rel/sev/clic', 'rel/sev/golpe')
    c.frames('dv_severo', 'rel/sev/frames')
    F('rel/sev/frames', 'execute if entity @a[distance=..5] run scoreboard players set #frame dv.tmp 3')
    ss = lambda t, ticks=120: say('Don Severo', SEV, '#f3e6cc', t, ticks)
    c.on('second', '''
execute if score #paranormal dv.cfg matches 1 unless entity @e[type=zombie,tag=dv_severo] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:de_dia if predicate canon:azar/1en2400 run function canon:rel/sev/aparecer
execute if score #paranormal dv.cfg matches 1 unless entity @e[type=zombie,tag=dv_severo] as @a[gamemode=!spectator,predicate=canon:en_pueblo,limit=1,sort=random] at @s if predicate canon:azar/1en700 run function canon:rel/sev/aparecer
''')
    F('rel/sev/aparecer', 'scoreboard players operation #pid dv.tmp = @s dv.pid\n' + spot('rel/sev/summon', '^ ^ ^9'))
    tick('rel/sev', 'dv_severo', '''
execute if score #m4 dv.clock matches 0 run function canon:x/face
execute if score @s dv.timer matches 20 run function canon:rel/sev/hola
execute if score @s dv.timer matches 6000.. run function canon:rel/sev/se_va
''')
    c.pick('rel/sev/hola', [ss(t) for t in [
        'Buenas, joven. Cosas para lo que no se ve. Barato. Pague con billetes.',
        'Sal, agua bendita, velas... Lo que necesite para dormir tranquilo. O para no dormir.',
        'Yo le vendí el Ouija a la muchacha pálida. No me mire así. Yo no sabía.']])
    F('rel/sev/se_va', ss('Me voy. Lo que no compró hoy, mañana le va a hacer falta.', 80) + '\nfunction canon:rig/despawn')
    F('rel/sev/golpe', head(K['severo_cabeza_raro']) + '\n' + ss('Con el vendedor no, joven. Con el vendedor nunca.', 80))
    F('rel/sev/clic', 'execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0\n' +
      menu('@a[tag=dv_talker]', 'DON SEVERO — cosas para lo que no se ve (precio en billetes)', SEV,
           [(f'{nom} ({p})', f'/trigger dv.severo set {k}') for k, (_, nom, p) in enumerate(TIENDA, 1)]))
    comp = ['scoreboard players operation #sv dv.tmp = @s dv.severo', 'scoreboard players set @s dv.severo 0',
            'execute unless entity @e[type=zombie,tag=dv_severo,distance=..12] run scoreboard players set #sv dv.tmp 0',
            f'execute store result score #bill dv.tmp run clear @s {BILL} 0']
    for k, (iid, nom, p) in enumerate(TIENDA, 1):
        give = 'function canon:rel/pag/dar' if iid == 'pagina' else f'loot give @s loot canon:para/{iid}'
        F(f'rel/sev/v{k}', f'clear @s {BILL} {p}\n{give}\nplaysound minecraft:entity.villager.yes neutral @s ~ ~ ~ 0.7 0.7\n'
          f'tellraw @s {jt("Don Severo: Buena compra. Úselo con respeto.", "#f3e6cc", True)}')
        comp.append(f'execute if score #sv dv.tmp matches {k} if score #bill dv.tmp matches {p}.. run function canon:rel/sev/v{k}')
        comp.append(f'execute if score #sv dv.tmp matches {k} unless score #bill dv.tmp matches {p}.. run tellraw @s {jt(f"Don Severo: Le faltan billetes, joven. Eso cuesta {p}.", "#f3e6cc", True)}')
    F('rel/severo/comprar', '\n'.join(comp))

    # ================================================================ POLTERGEIST DE VERDAD
    def scan(name, conds, tag):
        ls = []
        for dx in range(-6, 7):
            for dy in range(-1, 3):
                for dz in range(-6, 7):
                    for cond in conds:
                        ls.append(f'execute positioned ~{dx} ~{dy} ~{dz} if block ~ ~ ~ {cond} run summon minecraft:marker ~ ~ ~ {{Tags:["{tag}"]}}')
        F(f'rel/polter/scan_{name}', '\n'.join(ls))
    scan('puerta', ['#minecraft:wooden_doors[half=lower]'], 'dv_ppu')
    scan('antorcha', ['minecraft:torch', 'minecraft:wall_torch'], 'dv_pan')
    scan('cofre', ['minecraft:chest', 'minecraft:barrel'], 'dv_pco')
    scan('trampilla', ['#minecraft:wooden_trapdoors'], 'dv_ptr')
    F('rel/polter/trampilla', 'function canon:rel/polter/scan_trampilla\nexecute as @e[type=marker,tag=dv_ptr,limit=1,sort=random] at @s run function canon:rel/polter/tramp_tog\nkill @e[type=marker,tag=dv_ptr]')
    tt = ['scoreboard players set #dop dv.tmp 0', 'execute if block ~ ~ ~ #minecraft:wooden_trapdoors[open=false] run scoreboard players set #dop dv.tmp 1']
    for w in WOODS:
        tt.append(f'execute if block ~ ~ ~ minecraft:{w}_trapdoor run function canon:rel/polter/tramp_{w}')
        ls = []
        for f in ('north', 'south', 'east', 'west'):
            for hf in ('top', 'bottom'):
                st = f'facing={f},half={hf}'
                ls.append(f'execute if score #dop dv.tmp matches 1 if block ~ ~ ~ minecraft:{w}_trapdoor[{st},open=false] run setblock ~ ~ ~ minecraft:{w}_trapdoor[{st},open=true]')
                ls.append(f'execute if score #dop dv.tmp matches 0 if block ~ ~ ~ minecraft:{w}_trapdoor[{st},open=true] run setblock ~ ~ ~ minecraft:{w}_trapdoor[{st},open=false]')
        F(f'rel/polter/tramp_{w}', '\n'.join(ls))
    tt.append('playsound minecraft:block.wooden_trapdoor.open block @a[distance=..16] ~ ~ ~ 1 0.7')
    F('rel/polter/tramp_tog', '\n'.join(tt))
    for nm, tg, fn in (('puerta', 'dv_ppu', 'puerta_tog'), ('antorcha', 'dv_pan', 'antorcha_off'), ('cofre', 'dv_pco', 'cofre_escupe')):
        F(f'rel/polter/{nm}', f'function canon:rel/polter/scan_{nm}\nexecute as @e[type=marker,tag={tg},limit=1,sort=random] at @s run function canon:rel/polter/{fn}\nkill @e[type=marker,tag={tg}]')
    tog = ['scoreboard players set #dop dv.tmp 0', 'execute if block ~ ~ ~ #minecraft:wooden_doors[open=false] run scoreboard players set #dop dv.tmp 1']
    for w in WOODS:
        tog.append(f'execute if block ~ ~ ~ minecraft:{w}_door run function canon:rel/polter/door_{w}')
        ls = []
        for f in ('north', 'south', 'east', 'west'):
            for hg in ('left', 'right'):
                st = f'half=lower,facing={f},hinge={hg}'
                ls.append(f'execute if score #dop dv.tmp matches 1 if block ~ ~ ~ minecraft:{w}_door[{st},open=false] run setblock ~ ~ ~ minecraft:{w}_door[{st},open=true]')
                ls.append(f'execute if score #dop dv.tmp matches 0 if block ~ ~ ~ minecraft:{w}_door[{st},open=true] run setblock ~ ~ ~ minecraft:{w}_door[{st},open=false]')
        F(f'rel/polter/door_{w}', '\n'.join(ls))
    tog += ['execute if score #dop dv.tmp matches 1 run playsound minecraft:block.wooden_door.open block @a[distance=..16] ~ ~ ~ 1 0.8',
            'execute if score #dop dv.tmp matches 0 run playsound minecraft:block.wooden_door.close block @a[distance=..16] ~ ~ ~ 1 0.8',
            'tellraw @a[distance=..12] {"text":"Una puerta se movió sola.","color":"gray","italic":true}']
    F('rel/polter/puerta_tog', '\n'.join(tog))
    F('rel/polter/antorcha_off', '''
setblock ~ ~ ~ minecraft:air destroy
particle minecraft:smoke ~ ~0.5 ~ 0.1 0.2 0.1 0.01 15 normal
playsound minecraft:block.fire.extinguish block @a[distance=..16] ~ ~ ~ 0.8 1.2
tellraw @a[distance=..16] {"text":"Una antorcha se apagó sola y cayó al suelo.","color":"gray","italic":true}
''')
    F('rel/polter/cofre_escupe', 'data remove storage canon:tmp cof\ndata modify storage canon:tmp cof set from block ~ ~ ~ Items[-1]\n'
      'execute if data storage canon:tmp cof run function canon:rel/polter/cofre_saca')
    F('rel/polter/cofre_saca', '''
data remove block ~ ~ ~ Items[-1]
summon minecraft:item ~ ~1.1 ~ {Tags:["dv_pcit"],Item:{id:"minecraft:stone",Count:1b},PickupDelay:20s,Motion:[0.0d,0.35d,0.15d]}
execute as @e[type=item,tag=dv_pcit] run data modify entity @s Item set from storage canon:tmp cof
execute as @e[type=item,tag=dv_pcit] run data remove entity @s Item.Slot
tag @e[type=item,tag=dv_pcit] remove dv_pcit
playsound minecraft:block.chest.open block @a[distance=..16] ~ ~ ~ 1 0.7
playsound minecraft:block.chest.close block @a[distance=..16] ~ ~ ~ 1 0.6
tellraw @a[distance=..16] {"text":"Un cofre se abrió solo y escupió algo.","color":"gray","italic":true}
''')
    c.pick('rel/polter/mueble', [
        'execute as @e[type=item_display,tag=dv_mueble,distance=..14,limit=1,sort=random] at @s run tp @s ~ ~ ~ ~90 ~\nplaysound minecraft:block.wood.hit block @s ^ ^ ^-3 1 0.5\n'
        'tellraw @s {"text":"Algo se arrastró en el cuarto. Un mueble está girado.","color":"gray","italic":true}',
        'execute as @e[type=item_frame,distance=..14,limit=1,sort=random] run function canon:rel/polter/marco',
        'execute as @e[type=armor_stand,distance=..14,limit=1,sort=random] at @s facing entity @p eyes run tp @s ~ ~ ~ ~ 0\nplaysound minecraft:entity.armor_stand.hit block @s ^ ^ ^-3 1 0.6\n'
        'tellraw @s {"text":"Un soporte de armadura ahora te está mirando.","color":"gray","italic":true}'])
    F('rel/polter/marco', 'execute store result score #r dv.tmp run data get entity @s ItemRotation\nscoreboard players add #r dv.tmp 2\n'
      'scoreboard players operation #r dv.tmp %= #8 dv.math\nexecute store result entity @s ItemRotation byte 1 run scoreboard players get #r dv.tmp\n'
      'execute at @s run playsound minecraft:entity.item_frame.rotate_item block @a[distance=..16] ~ ~ ~ 1 0.6')
    c.const(8)

    # ================================================================ MUÑECA QUE VUELVE + FOTOS EN MARCOS
    c.on('second', '''
execute as @e[type=item] if data entity @s Item.tag.canon{id:"muneca"} run function canon:rel/muneca
execute if predicate canon:de_noche as @e[type=item_frame] if data entity @s Item.tag.canon{id:"foto"} at @s if entity @a[distance=..14] if predicate canon:azar/1en240 run function canon:rel/foto_marco
execute if predicate canon:de_noche as @e[type=item_frame] if data entity @s Item.tag.canon{id:"foto_vieja"} at @s if entity @a[distance=..14] if predicate canon:azar/1en240 run function canon:rel/foto_nieto
''')
    F('rel/muneca', 'scoreboard players add @s dv.timer 1\nexecute if score @s dv.timer matches 30.. at @s if entity @a[distance=..64] run function canon:rel/muneca2')
    F('rel/muneca2', 'loot give @p[gamemode=!spectator] loot canon:para/muneca\n'
      'tellraw @p[gamemode=!spectator] {"text":"Algo pesado apareció en tu bolsillo. La muñeca volvió. Siempre vuelve.","color":"#d8a0b0","italic":true}\nkill @s')
    F('rel/foto_marco', 'scoreboard players operation #pid dv.tmp = @p dv.pid\nfunction canon:acecho/elegir_quien\n' + spot('rel/foto_sale', '^ ^ ^2'))
    F('rel/foto_sale', 'function canon:acecho/aparecer\nplaysound minecraft:block.glass.hit hostile @a[distance=..16] ~ ~ ~ 0.8 0.6\n'
      'tellraw @a[distance=..14] {"text":"La persona de la foto ya no está en la foto. Está en el cuarto.","color":"#c94a4a","italic":true}')
    F('rel/foto_nieto', 'scoreboard players operation #pid dv.tmp = @p dv.pid\n' + spot('rel/nieto/fantasma', '^ ^ ^2'))

    # ================================================================ ABUELA: casa y nietos
    AB = lambda t, sel='@a[tag=dv_atalk]': say('Abuela Esmeralda', '#c9a27a', '#f6ead8', t, 140, sel)
    F('rel/abuela/casa', '''
execute if score #abucasa dv.build matches 1 run function canon:rel/abuela/casa_dice
execute unless score #abucasa dv.build matches 1 if dimension minecraft:overworld run function canon:rel/abuela/casa_nueva
''')
    F('rel/abuela/casa_dice', AB('Mi casita está aquí cerca. Vaya cuando quiera, mijo. La puerta nunca tiene seguro. Aunque debería.') +
      '\ntellraw @a[tag=dv_atalk] ["",{"text":"(La casa de la abuela está en ","color":"gray","italic":true},{"score":{"name":"#abx","objective":"dv.build"},"color":"white"},{"text":" ","color":"gray"},'
      '{"score":{"name":"#aby","objective":"dv.build"},"color":"white"},{"text":" ","color":"gray"},{"score":{"name":"#abz","objective":"dv.build"},"color":"white"},{"text":")","color":"gray","italic":true}]')
    F('rel/abuela/casa_nueva', 'scoreboard players set #ok dv.tmp 0\nexecute at @a[tag=dv_atalk,limit=1] rotated ~ 0 positioned ^ ^ ^22 run function canon:util/spot_search\n'
      'execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:rel/abuela/construir\nkill @e[type=marker,tag=dv_spot]\n'
      'execute if score #abucasa dv.build matches 1 run function canon:rel/abuela/casa_dice')
    diario = ['Diario de Esmeralda. Si estás leyendo esto, ya entraste a mi casa. Bienvenido, mijo.',
              'Hace cuarenta años encontré el Hueso. Pedí que mi esposo volviera del monte. Volvió sin voz.',
              'Mis nietos Tomasito, Lucía y Pablito, los primos de Santi, se fueron al bosque a buscar el Hueso. No volvieron. A veces los oigo reír.',
              'De noche, algo se pone mi cara y sale a buscar nietos nuevos. Yo me quedo dormida. Si toca tu puerta, no le abras.']
    pages = ','.join("'" + jt(t, '#3a2a1a').replace("'", '') + "'" for t in diario)
    foto = '{id:"minecraft:paper",Count:1b,tag:' + item_nbt('foto_vieja', 'Foto vieja', '#ece8de', ['Tres niños frente a la casa de la abuela.'], FOTO_CMD) + '}'
    F('rel/abuela/construir', f'''
scoreboard players set #abucasa dv.build 1
execute store result score #abx dv.build run data get entity @e[type=marker,tag=dv_spot,limit=1] Pos[0]
execute store result score #aby dv.build run data get entity @e[type=marker,tag=dv_spot,limit=1] Pos[1]
execute store result score #abz dv.build run data get entity @e[type=marker,tag=dv_spot,limit=1] Pos[2]
fill ~-6 ~-4 ~-6 ~6 ~-1 ~6 minecraft:cobblestone
fill ~-6 ~ ~-6 ~6 ~7 ~6 minecraft:air
fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 minecraft:dark_oak_planks
fill ~-4 ~ ~-4 ~4 ~3 ~-4 minecraft:spruce_planks
fill ~-4 ~ ~4 ~4 ~3 ~4 minecraft:spruce_planks
fill ~-4 ~ ~-4 ~-4 ~3 ~4 minecraft:spruce_planks
fill ~4 ~ ~-4 ~4 ~3 ~4 minecraft:spruce_planks
fill ~-4 ~ ~-4 ~-4 ~3 ~-4 minecraft:stripped_spruce_log
fill ~4 ~ ~-4 ~4 ~3 ~-4 minecraft:stripped_spruce_log
fill ~-4 ~ ~4 ~-4 ~3 ~4 minecraft:stripped_spruce_log
fill ~4 ~ ~4 ~4 ~3 ~4 minecraft:stripped_spruce_log
fill ~-4 ~4 ~-4 ~4 ~4 ~4 minecraft:dark_oak_planks
fill ~-5 ~5 ~-5 ~5 ~5 ~5 minecraft:dark_oak_slab
fill ~-3 ~6 ~-3 ~3 ~6 ~3 minecraft:dark_oak_slab
setblock ~-4 ~1 ~-1 minecraft:glass
setblock ~-4 ~1 ~1 minecraft:glass
setblock ~4 ~1 ~-1 minecraft:glass
setblock ~4 ~1 ~1 minecraft:glass
setblock ~-2 ~1 ~-4 minecraft:glass
setblock ~2 ~1 ~-4 minecraft:glass
setblock ~-2 ~1 ~4 minecraft:glass
setblock ~2 ~1 ~4 minecraft:glass
setblock ~ ~ ~4 minecraft:air
setblock ~ ~1 ~4 minecraft:air
setblock ~ ~ ~4 minecraft:spruce_door[half=lower,facing=north]
setblock ~ ~1 ~4 minecraft:spruce_door[half=upper,facing=north]
fill ~-2 ~ ~-1 ~2 ~ ~1 minecraft:red_carpet
setblock ~-3 ~ ~-2 minecraft:red_bed[part=foot,facing=north]
setblock ~-3 ~ ~-3 minecraft:red_bed[part=head,facing=north]
setblock ~3 ~ ~-3 minecraft:lectern[facing=south,has_book=true]{{Book:{{id:"minecraft:written_book",Count:1b,tag:{{title:"Diario de Esmeralda",author:"Esmeralda",pages:[{pages}]}}}}}}
setblock ~3 ~ ~2 minecraft:chest[facing=west]{{LootTable:"canon:rel/abu_cofre"}}
setblock ~-2 ~ ~2 minecraft:spruce_stairs[facing=south]
setblock ~ ~ ~ minecraft:oak_fence
setblock ~ ~1 ~ minecraft:candle[lit=true,candles=3]
setblock ~ ~3 ~ minecraft:lantern[hanging=true]
setblock ~-3 ~ ~3 minecraft:potted_red_tulip
setblock ~1 ~ ~5 minecraft:potted_red_tulip
setblock ~-1 ~ ~5 minecraft:oak_sign[rotation=0]{{front_text:{{messages:['{{"text":"Casa de la"}}','{{"text":"Abuela Esmeralda"}}','{{"text":"No abrir"}}','{{"text":"de noche"}}']}}}}
summon minecraft:item_frame ~-1 ~1 ~-3 {{Facing:3b,Item:{foto}}}
summon minecraft:item_frame ~1 ~1 ~-3 {{Facing:3b,Item:{foto}}}
''')
    c.json('data/canon/loot_tables/rel/abu_cofre.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'name': 'canon:rel/foto_vieja'}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'name': 'canon:rel/pag/p7'}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'name': 'canon:extras/crucifijo'}]},
        {'rolls': 2, 'entries': [{'type': 'minecraft:loot_table', 'name': 'canon:items/billete'}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:candle', 'functions': [{'function': 'minecraft:set_count', 'count': 3}]}]}]})
    F('rel/abuela/nietos', 'execute as @a[tag=dv_atalk,limit=1] run function canon:rel/nietos/pedir')
    NM = ['Tomasito', 'Lucía', 'Pablito']
    F('rel/nietos/pedir', f'''
execute if score @s dv.nietos matches 1..3 run tellraw @s {jt("Abuela Esmeralda: ¿Ya los encontró, mijo? Siga la risa. Brillan un poquito, como luciérnagas.", "#f6ead8", True)}
execute if score @s dv.nietos matches 4 run function canon:rel/nietos/premio
execute if score @s dv.nietos matches 5.. run tellraw @s {jt("Abuela Esmeralda: Ya están conmigo, mijo. Gracias. Ya nadie los busca de noche.", "#f6ead8", True)}
execute unless score @s dv.nietos matches 1.. run function canon:rel/nietos/empezar
''')
    F('rel/nietos/empezar', 'scoreboard players set @s dv.nietos 1\ntellraw @s ' + jt(
        'Abuela Esmeralda: Se llaman Tomasito, Lucía y Pablito. Se perdieron jugando en el bosque. Si de día oye una risa de niño, sígala. '
        'Brillan un poquito, como luciérnagas. Tráigamelos, mijo.', '#f6ead8', True))
    F('rel/nietos/premio', '''
scoreboard players set @s dv.nietos 5
tellraw @s {"text":"Abuela Esmeralda: Gracias, mijo. Ahora sí descansan. ¿Sabe por qué brillaban? Porque ya no están vivos. Pero ya no están solos.","color":"#f6ead8","italic":true}
loot give @s loot canon:items/billete
loot give @s loot canon:items/billete
loot give @s loot canon:items/billete
loot give @s loot canon:extras/crucifijo
function canon:rel/pag/dar_aviso
advancement grant @s only canon:logros/nietos
''')
    c.on('second', 'execute as @a[scores={dv.nietos=1..3},predicate=canon:en_superficie] at @s if predicate canon:de_dia unless entity @e[type=zombie,tag=dv_nieto,distance=..120] if predicate canon:azar/1en60 run function canon:rel/nietos/aparecer')
    c.pick('rel/nietos/aparecer', [f'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute rotated {a} 0 positioned ^ ^ ^40 run function canon:rel/nietos/spot' for a in (0, 60, 120, 180, 240, 300)])
    F('rel/nietos/spot', spot('rel/nieto/vivo') + '\ntellraw @s {"text":"Oyes la risa de un niño a lo lejos...","color":"#ffe3a0","italic":true}\nplaysound canon:devota.giggle ambient @s ~ ~ ~ 0.6 1.7')
    rig('rel/nieto', 'dv_nieto', 'Nieto', '#ffe3a0', K['nieto_idle'], K['nieto_cabeza_sonrisa'], scale=0.7)
    F('rel/nieto/vivo', 'function canon:rel/nieto/summon\nexecute as @e[type=zombie,tag=dv_nieto,distance=..2,limit=1,sort=nearest] on passengers run data merge entity @s {Glowing:1b,glow_color_override:16774000}')
    F('rel/nieto/fantasma', 'function canon:rel/nieto/summon\nexecute as @e[type=zombie,tag=dv_nieto,distance=..2,limit=1,sort=nearest] run function canon:rel/nieto/hacer_fantasma\n'
      'tellraw @a[distance=..14] {"text":"Uno de los niños de la foto está parado en el cuarto. No tiene cara.","color":"#c94a4a","italic":true}')
    F('rel/nieto/hacer_fantasma', 'tag @s add dv_asomo\ntag @s add dv_horror\nscoreboard players set @s dv.watch 0\n' + head(K['nieto_cabeza_triste']))
    tick('rel/nieto', 'dv_nieto', f'''
execute if entity @s[tag=dv_asomo] run scoreboard players set @s dv.timer 0
execute if entity @s[tag=dv_asomo] run function canon:acecho/piensa
execute if entity @s[tag=!dv_asomo] if score #m4 dv.clock matches 0 run function canon:x/face
execute if entity @s[tag=!dv_asomo] if score @s dv.timer matches 200 run playsound canon:devota.giggle ambient @a[distance=..48] ~ ~ ~ 0.8 1.7
execute if entity @s[tag=!dv_asomo] if score @s dv.state matches 0 if entity @a[tag=dv_wtgt,distance=..4] run function canon:rel/nieto/encontrado
execute if entity @s[tag=!dv_asomo] if score @s dv.timer matches 4800.. run function canon:rig/despawn
execute if score @s dv.state matches 1 if score @s dv.mode matches 60.. run function canon:rel/nieto/se_va
execute if score @s dv.state matches 1 run scoreboard players add @s dv.mode 1
''')
    F('rel/nieto/encontrado', 'scoreboard players set @s dv.state 1\nscoreboard players set @s dv.mode 0\n' +
      '\n'.join(f'execute if score @a[tag=dv_wtgt,limit=1] dv.nietos matches {i + 1} run tellraw @a[tag=dv_wtgt] {jt(f"{n}: ¡Me encontraste! Dile a mi abuela que la quiero... pero que no salga de noche. La de la noche no es ella.", "#ffe3a0", True)}'
                for i, n in enumerate(NM)) + '''
scoreboard players add @a[tag=dv_wtgt,scores={dv.nietos=1..3}] dv.nietos 1
loot give @a[tag=dv_wtgt] loot canon:items/petalo
execute as @a[tag=dv_wtgt,scores={dv.nietos=4}] run tellraw @s {"text":"Ya encontraste a los tres. Vuelve con la Abuela Esmeralda (de día) y pregúntale por sus nietos.","color":"gray","italic":true}
''' + set_cmd('body', K['nieto_arms_up']))
    F('rel/nieto/se_va', 'particle minecraft:glow ~ ~0.8 ~ 0.3 0.6 0.3 0 30 normal\nfunction canon:rig/despawn')

    # ================================================================ MARIANA: baile en tu ventana + Felipe
    rig('rel/mbaile', 'dv_mbaile', 'Mariana', '#b07ab8', K['mariana3_dance_a'], 7321007, ['dv_horror'], bubble=False)
    c.frames('dv_mbaile', 'rel/mbaile/frames')
    F('rel/mbaile/frames', 'scoreboard players operation #c dv.tmp = @s dv.anim\nscoreboard players operation #c dv.tmp %= #24 dv.math\n'
      'execute if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 1\nexecute if score #c dv.tmp matches 12..17 run scoreboard players set #frame dv.tmp 2\n'
      'execute if score #c dv.tmp matches 18..23 run scoreboard players set #frame dv.tmp 3')
    tick('rel/mbaile', 'dv_mbaile', '''
execute if score #m2 dv.clock matches 0 run function canon:x/face
execute if score @s dv.timer matches 1 run playsound canon:fx.music_box_end hostile @a[distance=..24] ~ ~ ~ 0.8 0.8
execute if score @s dv.timer matches 1 run tellraw @a[tag=dv_wtgt] {"text":"Afuera de tu ventana, Mariana baila. Sola. Despacio. Mirándote.","color":"#b07ab8","italic":true}
execute if entity @a[tag=dv_wtgt,distance=..4] run function canon:rel/mbaile/fin
execute if score @s dv.timer matches 400.. run function canon:rel/mbaile/fin
''')
    F('rel/mbaile/fin', 'playsound canon:devota.giggle hostile @a[distance=..16] ~ ~ ~ 0.8 0.8\nparticle minecraft:ash ~ ~1 ~ 0.4 0.9 0.4 0 30 normal\nfunction canon:rig/despawn')
    c.on('second', '''
execute if score #mariana2 dv.cfg matches 1 unless score #felipe_fin dv.dev matches 1 unless entity @e[type=zombie,tag=dv_mbaile] as @a[gamemode=!spectator,scores={dv.home=1}] at @s if predicate canon:de_noche if predicate canon:azar/1en900 run function canon:rel/mbaile/buscar
execute if score #mariana2 dv.cfg matches 1 unless score #felipe_fin dv.dev matches 1 unless entity @e[type=zombie,tag=dv_mbaile] as @a[gamemode=!spectator,tag=dv_mari_odio,scores={dv.home=1}] at @s if predicate canon:de_noche if predicate canon:azar/1en300 run function canon:rel/mbaile/buscar
execute if score #felipe_fin dv.dev matches 1 run scoreboard players set #ma_cd dv.dev 99999
''')
    F('rel/mbaile/buscar', 'scoreboard players set #vf dv.tmp 0\nscoreboard players operation #pid dv.tmp = @s dv.pid\n' + '\n'.join(
        f'execute if score #vf dv.tmp matches 0 anchored eyes rotated ~{a} 0 positioned ^ ^ ^1 run function canon:rel/mbaile/ray0' for a in (0, 45, -45, 90, -90, 135, -135, 180)))
    F('rel/mbaile/ray0', 'scoreboard players set #vs dv.tmp 0\nfunction canon:rel/mbaile/ray')
    F('rel/mbaile/ray', '''scoreboard players add #vs dv.tmp 1
execute if block ~ ~ ~ #canon:vidrio positioned ^ ^ ^2.5 if block ~ ~ ~ #canon:pasable positioned ~ ~-1.5 ~ run function canon:rel/mbaile/poner
execute if score #vf dv.tmp matches 0 if score #vs dv.tmp matches ..12 if block ~ ~ ~ #canon:pasable positioned ^ ^ ^1 run function canon:rel/mbaile/ray''')
    F('rel/mbaile/poner', 'scoreboard players set #vf dv.tmp 1\nfunction canon:rel/mbaile/summon\nexecute as @e[type=zombie,tag=dv_mbaile,distance=..2] at @s run function canon:diana/ground')
    # Felipe
    rig('rel/fel', 'dv_felipe', 'Felipe', FEL, K['felipe_idle'], K['felipe_cabeza_triste'], ['dv_humano'], click='dv_fel_click')
    rig('rel/mfin', 'dv_mfin', 'Mariana', '#b07ab8', K['mariana2_idle'], K['mariana2_cabeza_neutral'], ['dv_humano'])
    c.brain_click('dv_fel_click', 'zombie', 'dv_felipe', 'rel/fel/clic', 'rel/fel/clic')
    c.frames('dv_felipe', 'rel/fel/frames')
    F('rel/fel/frames', WALKF + 'execute if score @s dv.state matches 2 if score @s dv.timer matches 380.. if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 4\n'
      'execute if score @s dv.state matches 2 if score @s dv.timer matches 380.. if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 5')
    c.frames('dv_mfin', 'rel/mfin/frames')
    F('rel/mfin/frames', 'execute if score @s dv.mode matches 1 run function canon:rel/mbaile/frames')
    c.npc('dv_mfin', 'rel/mfin/tick')
    F('rel/mfin/tick', 'function canon:x/links_follow\nscoreboard players remove @s[scores={dv.say=1..}] dv.say 1\nexecute if score @s dv.say matches 0 run function canon:x/bubble_clear\n'
      'execute unless entity @e[type=zombie,tag=dv_felipe,distance=..12] run function canon:rig/despawn')
    fs = lambda t: say('Felipe', FEL, '#e0e8f4', t, 140, '@a[distance=..24]')
    ms = lambda t: 'execute as @e[type=zombie,tag=dv_mfin,limit=1,sort=nearest] at @s run function canon:rel/mfin/' + t
    for k, t in enumerate(['¿Felipe? ¿Eres tú? ¿Dónde estabas?', 'Te busqué en todas partes. Le grité a gente que no tenía la culpa. Les dejé carteles a todos.',
                           'Está bien. La última. Y después me dejas de doler.'], 1):
        F(f'rel/mfin/l{k}', say('Mariana', '#b07ab8', '#f0dcf4', t, 140, '@a[distance=..24]'))
    F('rel/mfin/baila', set_cmd('body', K['mariana3_dance_a']) + '\nscoreboard players set @s dv.mode 1\n' + head(K['mariana2_cabeza_neutral']))
    c.on('second', 'execute if score #mariana2 dv.cfg matches 1 unless score #felipe_fin dv.dev matches 1 unless entity @e[type=zombie,tag=dv_felipe] as @a[advancements={canon:cuaderno/mariana=true},gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:de_dia if predicate canon:azar/1en1500 run function canon:rel/fel/aparecer')
    F('rel/fel/aparecer', 'scoreboard players operation #pid dv.tmp = @s dv.pid\n' + spot('rel/fel/summon', '^ ^ ^14'))
    tick('rel/fel', 'dv_felipe', f'''
execute if score @s dv.state matches 0..1 if score #m4 dv.clock matches 0 run function canon:x/face
execute if score @s dv.state matches 0 if score @s dv.timer matches 20 run function canon:rel/fel/hola
execute if score @s dv.state matches 0 if score @s dv.timer matches 3600.. run function canon:rel/fel/se_va
execute if score @s dv.state matches 1 unless entity @a[tag=dv_wtgt,distance=..3] run function canon:x/walk
execute if score @s dv.state matches 1 if entity @a[tag=dv_wtgt] unless entity @a[tag=dv_wtgt,distance=..24] at @a[tag=dv_wtgt,limit=1] run tp @s ^ ^ ^-2
execute if score @s dv.state matches 1 if score @s dv.timer matches 300 unless entity @e[type=zombie,tag=dv_mari2] at @a[tag=dv_wtgt,limit=1] rotated ~ 0 positioned ^ ^ ^14 run function canon:rel/fel/llamar_mari
execute if score @s dv.state matches 1 if entity @e[type=zombie,tag=dv_mari2,distance=..10] run function canon:rel/fel/escena
execute if score @s dv.state matches 1 if score @s dv.timer matches 12000.. run function canon:rel/fel/se_va
execute if score @s dv.state matches 2 run function canon:rel/fel/escena_tick
''')
    F('rel/fel/hola', fs('¿Usted conoce a Mariana? Dígame que sí. Necesito... necesito despedirme.'))
    F('rel/fel/se_va', fs('Si la ve, no le diga que estoy frío.') + '\nfunction canon:rig/despawn')
    F('rel/fel/clic', 'execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0\n' + menu('@a[tag=dv_talker]', 'FELIPE', FEL, [
        ('¿Eres Felipe? Mariana te busca', '/trigger dv.fel set 1'), ('¿Qué te pasó?', '/trigger dv.fel set 2'),
        ('Ven conmigo, vamos a buscarla', '/trigger dv.fel set 3'), ('Adiós', '/trigger dv.fel set 4')]))
    F('rel/felipe/eleccion', '''
tag @s add dv_ftalk
scoreboard players operation #fc dv.tmp = @s dv.fel
scoreboard players set @s dv.fel 0
execute as @e[type=zombie,tag=dv_felipe,distance=..14,limit=1,sort=nearest] at @s run function canon:rel/fel/responde
tag @s remove dv_ftalk
''')
    F('rel/fel/r1', fs('¿Mariana? Le dije que volvía en una hora. Eso fue hace mucho. Mucho. ¿Todavía baila sola?'))
    F('rel/fel/r2', fs('Me caí al lago la noche de la fiesta. Nadie me buscó en el agua. Ella me busca en todas partes menos ahí.'))
    F('rel/fel/r3', fs('¿Me lleva con ella? Sí. Quiero despedirme bien. Vamos, yo lo sigo.') + '\nscoreboard players set @s dv.state 1\nscoreboard players set @s dv.timer 0\n'
      'scoreboard players operation @s dv.target = @a[tag=dv_ftalk,limit=1] dv.pid')
    F('rel/fel/responde', '\n'.join(f'execute if score #fc dv.tmp matches {k} run function canon:rel/fel/r{k}' for k in (1, 2, 3)) +
      '\nexecute if score #fc dv.tmp matches 4 run function canon:rel/fel/se_va')
    F('rel/fel/llamar_mari', 'scoreboard players operation #pid dv.tmp = @a[tag=dv_wtgt,limit=1] dv.pid\n' + spot('mari2/summon') + '\n' +
      'execute as @e[type=zombie,tag=dv_felipe] at @s run function canon:rel/fel/la_vi')
    F('rel/fel/la_vi', fs('Ahí está. La reconocería en cualquier parte. Lleva el vestido de esa noche.'))
    F('rel/fel/escena', '''
scoreboard players set @s dv.state 2
scoreboard players set @s dv.timer 0
execute as @e[type=zombie,tag=dv_mari2] at @s run function canon:rig/despawn
execute positioned ^ ^ ^2.5 run function canon:rel/mfin/summon
execute as @e[type=zombie,tag=dv_mfin,limit=1,sort=nearest] at @s facing entity @e[type=zombie,tag=dv_felipe,limit=1,sort=nearest] feet run tp @s ~ ~ ~ ~ 0
''')
    F('rel/fel/escena_tick', f'''
execute if score @s dv.timer matches 20 run {ms('l1')}
execute if score @s dv.timer matches 110 run function canon:rel/fel/e1
execute if score @s dv.timer matches 200 run {ms('l2')}
execute if score @s dv.timer matches 300 run function canon:rel/fel/e2
execute if score @s dv.timer matches 370 run {ms('l3')}
execute if score @s dv.timer matches 380 run function canon:rel/fel/baila
execute if score @s dv.timer matches 380.. if score #m10 dv.clock matches 0 run particle minecraft:cherry_leaves ~ ~1.5 ~ 1.5 1 1.5 0 10 normal
execute if score @s dv.timer matches 600 run function canon:rel/fel/fin
''')
    F('rel/fel/e1', fs('Perdóname. Te dije que volvía en una hora.'))
    F('rel/fel/e2', head(K['felipe_cabeza_sonrisa']) + '\n' + fs('Ya no tienes que buscar más. Ven. Bailemos la última canción.'))
    F('rel/fel/baila', set_cmd('body', K['felipe_dance_a']) + '\nplaysound canon:fx.music_box_end record @a[distance=..32] ~ ~ ~ 1 1\n' + ms('baila'))
    F('rel/fel/fin', '''
particle minecraft:end_rod ~ ~1.2 ~ 1 1 1 0.05 80 normal
title @a[distance=..48] times 20 80 30
title @a[distance=..48] subtitle {"text":"Por fin dejaron de buscarse.","color":"#f0dcf4","italic":true}
title @a[distance=..48] title {"text":"Mariana y Felipe","color":"#b07ab8"}
tellraw @a {"text":"☾ Mariana encontró a Felipe. Ya no va a volver a dejar carteles.","color":"gray","italic":true}
scoreboard players set #felipe_fin dv.dev 1
tag @a remove dv_mari_odio
advancement grant @a[distance=..48] only canon:logros/felipe
execute as @p[distance=..48] run function canon:rel/pag/dar_aviso
execute as @e[type=zombie,tag=dv_mfin] at @s run function canon:rig/despawn
function canon:rig/despawn
''')

    # ================================================================ EL MIRÓN QUE SE ACERCA + LOS SIN ROSTRO
    rig('rel/miron', 'dv_miracerca', 'El Mirón', '#555555', 7320142, None, ['dv_horror'], scale=1.3, bubble=False)
    c.on('second', '''
execute if score #miron dv.cfg matches 1 unless entity @e[type=zombie,tag=dv_miracerca] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:de_noche if predicate canon:azar/1en1500 run function canon:rel/miron/aparecer
execute if score #paranormal dv.cfg matches 1 unless entity @e[type=zombie,tag=dv_sinrostro] as @a[gamemode=!spectator,predicate=canon:en_pueblo,limit=1,sort=random] at @s if predicate canon:azar/1en500 run function canon:rel/sinr/grupo
execute if score #paranormal dv.cfg matches 1 unless entity @e[type=zombie,tag=dv_sinrostro] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:de_noche if predicate canon:azar/1en3000 run function canon:rel/sinr/grupo
''')
    F('rel/miron/aparecer', 'scoreboard players operation #pid dv.tmp = @s dv.pid\n' + spot('rel/miron/summon', '^ ^ ^34'))
    tick('rel/miron', 'dv_miracerca', '''
tag @a remove dv_lookers
tag @a[tag=dv_wtgt] add dv_lookers
execute if score #m2 dv.clock matches 0 run function canon:x/face
function canon:x/seen
tag @a remove dv_lookers
execute if score #seen dv.tmp matches 1 run scoreboard players set @s dv.state 1
execute if score #seen dv.tmp matches 0 if score @s dv.state matches 1 run function canon:rel/miron/acerca
execute if score @s dv.timer matches 3600.. run function canon:rig/despawn
''')
    F('rel/miron/acerca', 'scoreboard players set @s dv.state 0\nscoreboard players add @s dv.mode 1\n'
      'execute if score @s dv.mode matches 4.. run function canon:rel/miron/final\nexecute if score @s dv.mode matches ..3 run function canon:rel/miron/mover')
    F('rel/miron/mover', 'scoreboard players set #ok dv.tmp 0\n' + '\n'.join(
        f'execute if score @s dv.mode matches {m} at @a[tag=dv_wtgt,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^{d} run function canon:util/spot_search'
        for m, d in ((1, 24), (2, 14), (3, 7))) + '''
execute if score #ok dv.tmp matches 1 run tp @s @e[type=marker,tag=dv_spot,limit=1]
kill @e[type=marker,tag=dv_spot]
playsound canon:miron.estatica hostile @a[tag=dv_wtgt] ~ ~ ~ 0.5 0.5
''')
    F('rel/miron/final', '''
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
scoreboard players add @a[tag=dv_wtgt] dv.miedo 30
tellraw @a[tag=dv_wtgt] {"text":"Cada vez que lo mirabas, se acercaba. Ya no necesita acercarse más.","color":"#c94a4a","italic":true}
function canon:rig/despawn
''')
    rig('rel/sinr', 'dv_sinrostro', '???', '#555555', K['sinrostro_idle'], K['sinrostro_cabeza_liso'], ['dv_horror'], bubble=False)
    c.frames('dv_sinrostro', 'rel/sinr/frames')
    F('rel/sinr/frames', 'execute if score @s dv.state matches 1 run scoreboard players set #frame dv.tmp 1')
    F('rel/sinr/grupo', 'scoreboard players operation #pid dv.tmp = @s dv.pid\n' + '\n'.join(
        f'execute rotated ~ 0 positioned ^{x} ^ ^{z} run function canon:rel/sinr/uno' for x, z in ((-4, 20), (0, 22), (4, 20), (-2, 25), (2, 25))) +
      '\ntellraw @s {"text":"Hay gente parada a lo lejos, mirándote. No tienen cara.","color":"#c94a4a","italic":true}')
    F('rel/sinr/uno', spot('rel/sinr/summon') + '\nexecute as @e[type=zombie,tag=dv_sinrostro,tag=!dv_sr_ok] run function canon:rel/sinr/pose')
    c.pick('rel/sinr/pose', ['tag @s add dv_sr_ok', 'tag @s add dv_sr_ok', 'tag @s add dv_sr_ok\nscoreboard players set @s dv.state 1'])
    tick('rel/sinr', 'dv_sinrostro', '''
tag @a remove dv_lookers
tag @a[tag=dv_wtgt] add dv_lookers
execute if score #m4 dv.clock matches 0 run function canon:x/face
function canon:x/seen
tag @a remove dv_lookers
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score #seen dv.tmp matches 0 if score @s dv.watch matches 40.. run function canon:rel/sinr/paso
execute if entity @a[tag=dv_wtgt,distance=..8] run function canon:rel/sinr/se_van
execute if score @s dv.timer matches 1200.. run function canon:rig/despawn
''')
    F('rel/sinr/paso', 'scoreboard players set @s dv.watch 0\nexecute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^3 run tp @s ~ ~ ~\n'
      'execute at @s run function canon:diana/ground\nplaysound canon:diana.step hostile @a[tag=dv_wtgt] ~ ~ ~ 0.4 0.7')
    F('rel/sinr/se_van', 'execute as @e[type=zombie,tag=dv_sinrostro] at @s run particle minecraft:ash ~ ~1 ~ 0.3 0.8 0.3 0 20 normal\n'
      'execute as @e[type=zombie,tag=dv_sinrostro] at @s run function canon:rig/despawn')

    # ================================================================ JARDÍN SECRETO DE JULI (en El Sueño de la casa blanca)
    c.on('load', 'execute in canon:sueno_blanco run forceload add 33 33 47 47\nexecute unless score #jardin dv.build matches 1 run schedule function canon:rel/jardin/try 40t')
    F('rel/jardin/try', 'execute in canon:sueno_blanco if loaded 40 110 40 run function canon:rel/jardin/construir\n'
      'execute unless score #jardin dv.build matches 1 run schedule function canon:rel/jardin/try 40t')
    flores = [(34, 37, 'pink_tulip'), (35, 40, 'allium'), (38, 44, 'azure_bluet'), (41, 46, 'oxeye_daisy'), (46, 44, 'lily_of_the_valley'),
              (44, 34, 'cornflower'), (39, 39, 'pink_tulip'), (42, 38, 'allium'), (46, 35, 'pink_tulip'), (34, 46, 'lily_of_the_valley')]
    F('rel/jardin/construir', '\n'.join([
        'fill 33 109 33 47 109 47 minecraft:grass_block', 'fill 34 108 34 46 108 46 minecraft:dirt', 'fill 36 107 36 44 107 44 minecraft:dirt',
        'fill 38 106 38 42 106 42 minecraft:stone', 'fill 33 110 33 47 118 47 minecraft:air', 'fill 35 109 44 37 109 46 minecraft:water',
        'fill 43 110 43 43 114 43 minecraft:cherry_log', 'fill 41 114 41 45 116 45 minecraft:cherry_leaves[persistent=true] keep',
        'fill 42 117 42 44 117 44 minecraft:cherry_leaves[persistent=true]', 'fill 36 110 36 36 113 36 minecraft:oak_fence',
        'fill 38 110 36 38 113 36 minecraft:oak_fence', 'fill 36 114 36 38 114 36 minecraft:oak_slab', 'setblock 37 113 36 minecraft:chain',
        'setblock 37 112 36 minecraft:chain', 'setblock 37 111 36 minecraft:oak_slab', 'fill 34 110 33 39 110 33 minecraft:birch_fence',
        'fill 41 110 33 46 110 33 minecraft:birch_fence', 'setblock 40 110 33 minecraft:birch_fence_gate[facing=south]',
        'setblock 33 110 33 minecraft:lantern', 'setblock 47 110 33 minecraft:lantern', 'setblock 33 110 47 minecraft:lantern', 'setblock 47 110 47 minecraft:lantern',
        'setblock 44 110 38 minecraft:spruce_stairs[facing=east]', 'setblock 44 110 39 minecraft:spruce_stairs[facing=east]',
        """setblock 40 110 35 minecraft:birch_sign[rotation=0]{front_text:{messages:['{"text":"Lugar secreto"}','{"text":"de Juli"}','{"text":"No le digas"}','{"text":"a nadie"}']}}""",
        'summon minecraft:interaction 40.5 110 33.5 {Tags:["dv_jsalida","dv_click","dv_npc_click"],width:1.2f,height:1.6f,response:1b}',
        'scoreboard players set #jardin dv.build 1'] + [f'setblock {x} 110 {z} minecraft:{f}' for x, z, f in flores]))
    LUCI = [(34.5, 110.4, 34.5), (46.5, 110.4, 46.5), (37.5, 111.9, 36.5), (45.5, 110.4, 40.5), (43.5, 112.5, 42.5)]
    F('rel/jardin/lucis', '\n'.join(
        f'summon minecraft:item_display {x} {y} {z} {{Tags:["dv_luci_vis"],Glowing:1b,glow_color_override:16774000,brightness:{{sky:15,block:15}},billboard:"center",'
        f'item:{{id:"minecraft:glowstone_dust",Count:1b}},transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.4f,0.4f,0.4f],right_rotation:[0f,0f,0f,1f]}}}}\n'
        f'summon minecraft:interaction {x} {y - 0.35:.2f} {z} {{Tags:["dv_luci","dv_click","dv_npc_click"],width:0.7f,height:0.7f,response:1b}}' for x, y, z in LUCI))
    c.patch('casa/clicked', lambda s: s if 'dv.jr set 10' in s else s.rstrip('\n') + '\n' +
            menu('@a[tag=dv_talker]', '', '#f2a7c3', [('Enséñame tu lugar secreto', '/trigger dv.jr set 10')]) + '\n')
    c.patch('casa/c/run', lambda s: s if 'rel/jardin/ir' in s else s.rstrip('\n') + '\nexecute if score #jc dv.tmp matches 10 run function canon:rel/jardin/ir\n')
    jt_j = lambda t: f'tellraw @s ["",{jt("Juli: ", "#f2a7c3", bold=True)},{jt(t, "#fde3ee", True)}]'
    F('rel/jardin/ir', 'execute as @a[tag=dv_jtalk] run function canon:rel/jardin/entrar')
    F('rel/jardin/entrar', f'''
execute unless score #jardin dv.build matches 1 run {jt_j("Todavía lo estoy arreglando. Pregúntame otra vez en un ratito.")}
execute if score #jardin dv.build matches 1 in canon:sueno_blanco run function canon:rel/jardin/entrar2
''')
    F('rel/jardin/entrar2', f'''
tp @s 40.5 110 41.5 180 0
effect give @s minecraft:blindness 1 0 true
playsound canon:juli.chime ambient @s ~ ~ ~ 1 1.2
{jt_j("Este es mi lugar secreto. Ni Dani lo conoce. Aquí Diana no entra. Hay cinco luciérnagas escondidas; si las atrapas todas, te doy algo.")}
tellraw @s {{"text":"(Para volver a la casa, cruza la reja blanca del fondo.)","color":"gray","italic":true}}
execute unless entity @e[type=interaction,tag=dv_luci,x=33,y=105,z=33,dx=15,dy=15,dz=15] run function canon:rel/jardin/lucis
''')
    c.click('dv_luci', 'rel/jardin/luci')
    c.click('dv_jsalida', 'rel/jardin/salir')
    F('rel/jardin/luci', '''
kill @e[type=item_display,tag=dv_luci_vis,distance=..1.2]
scoreboard players add @a[tag=dv_talker] dv.luci 1
playsound minecraft:block.amethyst_block.chime player @a[tag=dv_talker] ~ ~ ~ 1 1.5
particle minecraft:glow ~ ~0.5 ~ 0.3 0.3 0.3 0 15 normal
tellraw @a[tag=dv_talker] ["",{"text":"Luciérnaga ","color":"#f2e27a"},{"score":{"name":"@a[tag=dv_talker,limit=1]","objective":"dv.luci"},"color":"white"},{"text":"/5","color":"#f2e27a"}]
execute as @a[tag=dv_talker,scores={dv.luci=5..}] run function canon:rel/jardin/premio
kill @s
''')
    F('rel/jardin/premio', 'scoreboard players set @s dv.luci 0\n' + jt_j('¡Las encontraste todas! Toma, son para ti. Y esto lo encontré en el piso de la casa... es de Diana, creo.') +
      '\nloot give @s loot canon:items/petalo\nloot give @s loot canon:items/petalo\nloot give @s loot canon:items/petalo\nfunction canon:rel/pag/dar\nadvancement grant @s only canon:logros/jardin')
    F('rel/jardin/salir', 'execute as @a[tag=dv_talker] in canon:sueno_blanco run tp @s 12.5 64 -5.5 0 5\ntellraw @a[tag=dv_talker] {"text":"Vuelves a la casa blanca. Huele a flores.","color":"#f2a7c3","italic":true}')
    c.on('second', '''
execute in canon:sueno_blanco as @a[x=30,y=100,z=30,dx=20,dy=30,dz=20] run effect give @s minecraft:slow_falling 3 0 true
execute in canon:sueno_blanco as @a[x=30,y=60,z=30,dx=20,dy=45,dz=20] run tp @s 40.5 110 41.5 180 0
execute in canon:sueno_blanco as @e[type=item_display,tag=dv_luci_vis] at @s run particle minecraft:glow ~ ~ ~ 0.2 0.2 0.2 0 2 normal
''')

    # ================================================================ LUNA: solo caza vacas, ovejas y pollos (el miedo lo maneja Java: LunaMiedo)
    c.json('data/canon/tags/entity_types/presas_luna.json', {'values': ['minecraft:cow', 'minecraft:sheep', 'minecraft:chicken']})
    c.on('second', 'execute as @e[type=wolf,tag=dv_luna] at @s unless entity @e[tag=dv_horror,distance=..14] if entity @e[type=#canon:presas_luna,distance=..10] if predicate canon:azar/1en120 run function canon:rel/luna/caza')
    F('rel/luna/caza', '''
data modify entity @s AngryAt set from entity @e[type=#canon:presas_luna,distance=..10,limit=1,sort=nearest] UUID
data modify entity @s AngerTime set value 200
playsound minecraft:entity.wolf.growl neutral @a[distance=..16] ~ ~ ~ 0.6 1.2
''')

    # ================================================================ admin
    adm = [('jefe', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^10 run function canon:rel/jefe/llega', 'Traer al jefe final'),
           ('paginas', '\n'.join(f'loot give @s loot canon:rel/pag/p{n}' for n in range(1, 14)), 'Las 13 páginas del diario'),
           ('severo', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^4 run function canon:rel/sev/summon', 'Traer a Don Severo'),
           ('felipe', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^4 run function canon:rel/fel/summon', 'Traer a Felipe'),
           ('miron', 'function canon:rel/miron/aparecer', 'El Mirón que se acerca'),
           ('sinrostro', 'function canon:rel/sinr/grupo', 'Los Sin Rostro'),
           ('baile', 'function canon:rel/mbaile/buscar', 'Mariana baila en tu ventana (en tu casa)'),
           ('nieto', 'scoreboard players operation #pid dv.tmp = @s dv.pid\nexecute positioned ^ ^ ^5 run function canon:rel/nieto/vivo', 'Traer a un nieto'),
           ('casa_abuela', 'scoreboard players set #abucasa dv.build 0\ntag @s add dv_atalk\nfunction canon:rel/abuela/casa_nueva\ntag @s remove dv_atalk', 'Construir la casa de la abuela adelante'),
           ('jardin', 'tag @s add dv_jtalk\nfunction canon:rel/jardin/ir\ntag @s remove dv_jtalk', 'Ir al jardín secreto de Juli'),
           ('polter', 'function canon:rel/polter/puerta\nfunction canon:rel/polter/antorcha\nfunction canon:rel/polter/cofre', 'Poltergeist ya (puerta, antorcha, cofre)'),
           ('noche', 'function canon:rel/noches/planear', 'Anunciar una noche especial')]
    for nm, body, desc in adm:
        F(f'admin/rel/{nm}', body)
        c.admin(f'/function canon:admin/rel/{nm}', desc)
