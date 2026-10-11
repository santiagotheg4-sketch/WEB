"""NPCs nuevos: 8 habitantes de Valle Quieto y 2 viajeros del mundo normal.
Cada uno con modelo propio, frases, menú de temas (trigger dv.npc), regalos y reacción a los horrores.
"""
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon import models as M

# id, nombre, color, lugar, build, hair_style, colores, escala, frases, temas[(etiqueta, respuesta, regalo_loot o None)]
NPCS = [
    ('ernesto', 'Don Ernesto', '#a8a29a', 'pueblo', 'thin', 'bald',
     dict(skin='#d9b89c', hair='#bdbdbd', pants='#2b2b2e', shoes='#1d1d1d', belt='#3a3a3a', shirt='#3b3a36', sleeve='#3b3a36'), 1.0,
     ['Mil trescientas once tumbas. Todas con flores frescas. Nadie las pone.', 'Cava despacio. La tierra de aquí devuelve cosas.',
      'Anoche una tumba estaba abierta. Hoy está cerrada otra vez.', 'Yo también pedí un deseo. Pedí no morirme nunca. Mire cómo me fue.'],
     [('¿Quién está enterrado aquí?', 'Gente que pidió un deseo. Y algunos que no. La última tumba no tiene nombre todavía. Espero que no sea la suya.', None),
      ('¿Conoce a Diana?', 'No diga ese nombre aquí. Ella viene al cementerio a leer las lápidas. Busca una que diga Juan.', None),
      ('¿Cómo salgo del pueblo?', 'Por la carretera del norte, en ese descapotable del taller. Nadie lo ha logrado en años. Pero usted tiene cara de terco.', None),
      ('¿Me regala algo?', 'Tome esta vela. Si se apaga sola, corra.', 'canon:items/linterna')]),
    ('rosa', 'Rosa la panadera', '#e8b88a', 'pueblo', 'chubby', 'bob',
     dict(skin='#e2b998', hair='#6b3b26', pants='#5a4a3a', shoes='#3a2a20', belt='#f2f2f2', shirt='#f2ece2', sleeve='#c95f4f'), 1.0,
     ['¡Pan caliente! Bueno, tibio. Bueno, de ayer.', 'Aquí nadie paga con plata. Pagan con lo que recuerdan.',
      'La muchacha del parque compra pan todos los días y nunca se lo come.', 'Mi horno se prende solo a la 1:11. Ya ni me asusto.'],
     [('¿Qué vende?', 'Pan, arepas, buñuelos y chismes. Los chismes son gratis.', None),
      ('¿Qué se dice en el pueblo?', 'Que un muchacho moreno armó una fiesta y desapareció tres días. Que la niña de la bicicleta no crece. Que el Mirón volvió.', None),
      ('¿Conoce a Mariana?', 'Mariana no habla. Baila. Si le insiste, deja de bailar. No quiera ver eso.', None),
      ('Tengo hambre', 'Tome, mijo. Y no le diga a nadie que se lo regalé.', 'canon:items/sopa')]),
    ('tomas', 'Padre Tomás', '#9a8fb0', 'pueblo', 'normal', 'short',
     dict(skin='#e0c0a8', hair='#3a3a3a', pants='#121214', shoes='#0d0d0d', belt='#121214', shirt='#141418', sleeve='#141418'), 1.0,
     ['La iglesia está abierta. Dios a veces no.', 'Rezo por los que pidieron deseos. Son muchos.', 'Las campanas suenan solas a las 13:11.'],
     [('¿Qué es el Hueso de los Deseos?', 'Una herramienta del diablo con forma de juguete. Concede todo y cobra después. Siempre cobra.', None),
      ('¿Me puede bendecir?', 'Que la luz te encuentre antes que la oscuridad. Ve con Dios. Y con linterna.', 'bendicion'),
      ('¿Por qué nadie dice el nombre de Diana?', 'Porque si lo dices completo, te escucha. Y ella nunca olvida a quien la llama.', None),
      ('Confesión', 'Yo también pedí un deseo. Pedí fe. Ahora la tengo. Y me da miedo lo que veo con ella.', None)]),
    ('ramirez', 'Policía Ramírez', '#6f8fc0', 'pueblo', 'normal', 'short',
     dict(skin='#c99a76', hair='#1f1a16', pants='#1f2b44', shoes='#111111', belt='#2a2a2a', shirt='#3a5a8a', sleeve='#3a5a8a'), 1.0,
     ['Circule, circule. Bueno, no hay a dónde circular.', 'Tengo 1.311 expedientes abiertos. Y un café frío.', 'Si ve algo raro, no me avise. Ya sé.'],
     [('Desaparecidos', 'Nicolás, catorce años, entró a la mina. Kevin, el chistoso, perdido tres días en las catacumbas. Y usted, si no se cuida.', None),
      ('¿Cómo escapo?', 'El descapotable del taller. Batería, gasolina, bujías y llaves. Las piezas están regadas por el pueblo. Revise el diario.', None),
      ('¿Ha visto algo raro?', 'Una figura flaca en las azoteas. No se mueve si la mira. Yo dejé de mirarla.', None),
      ('Necesito ayuda', 'Tome. Use eso solo si es necesario. Y no me diga para qué.', 'canon:items/balas')]),
    ('sofi', 'Sofi', '#f2a7c3', 'pueblo', 'normal', 'bob',
     dict(skin='#f0d2c0', hair='#c48a3a', pants='#f2d8e8', shoes='#e8e8e8', belt='#d07aa0', shirt='#f7b8d0', sleeve='#f7b8d0'), 0.72,
     ['¿Juegas conmigo? Nadie juega conmigo.', 'Tengo diez años. Desde hace mucho.', 'Mi bicicleta se perdió en la niebla. Ella volvió sola.'],
     [('Adivinanza', 'Tiene ojos y no ve, tiene cara y no es. Te mira de noche y nunca la ves. ¿Quién es? Jijiji.', None),
      ('¿Juegas al escondite?', 'Cuando quieras. Pero si te encuentro, te quedas aquí conmigo. Para siempre. Es broma. Creo.', None),
      ('¿Dónde están tus papás?', 'Pidieron que yo nunca creciera. Y luego se fueron. ¿Tú me vas a dejar también?', None),
      ('Toma un dulce', 'Gracias. Toma, te doy un pétalo. Me lo dio una chica que solo existe cuando duermes.', 'canon:items/petalo')]),
    ('wilson', 'Wilson el del radio', '#8fb36a', 'pueblo', 'thin', 'emo',
     dict(skin='#d8b494', hair='#5a4a3a', pants='#4a4a3a', shoes='#2a2a2a', belt='#3a3a2a', shirt='#556b2f', sleeve='#556b2f'), 1.0,
     ['¡La 13.11 FM! ¡Ahí transmiten los que se fueron!', 'Shhh. Escuche la estática. ¿Oyó su nombre?', 'Ellos nos vigilan con antenas. Y con ojos.'],
     [('El Mirón', 'Aparece antes de que pase algo. Es el que mira el Canon. Si lo ve, prepárese. Algo tiene que pasar.', None),
      ('Frecuencias', 'En la 13.11 se oye a una muchacha cantando. En la 6.6 se oye a alguien cavando. Nunca ponga la 0.0.', None),
      ('¿Qué es el Canon?', 'Lo que tiene que pasar. Usted puede cambiarlo una vez. Después el mundo se corrige. Esas cosas de afuera son correcciones.', None),
      ('Deme algo', 'Tome mi radio de repuesto. Cuanto más fuerte la estática, más cerca está.', 'canon:items/radio')]),
    ('tono', 'Toño el mecánico', '#d9a441', 'pueblo', 'chubby', 'short',
     dict(skin='#b88660', hair='#1a1a1a', pants='#3b4f6b', shoes='#2a2a2a', belt='#3b4f6b', shirt='#3b4f6b', sleeve='#6a6a6a'), 1.0,
     ['Ese descapotable es una belleza. Lástima que nadie sale vivo manejándolo.', 'Huele a gasolina. Y a algo más.', 'Le cambié las bujías al carro del alcalde. Él no tiene carro.'],
     [('El descapotable', 'Necesita batería, gasolina, bujías y las llaves. Póngaselas en el taller, súbase y maneje al norte. No pare. No mire atrás.', None),
      ('¿Dónde consigo piezas?', 'La batería la vi en una casa, la gasolina en la estación, las bujías en la tienda... y las llaves, las llaves siempre las tiene alguien que no quiere que se vaya.', None),
      ('¿Alguien escapó?', 'Uno. Hace años. Volvió al otro día. Dijo que la carretera da la vuelta.', None),
      ('Regáleme algo', 'Una linterna. Las de aquí duran poco. Como todo.', 'canon:items/linterna')]),
    ('lucia', 'Lucía la mesera', '#c94a6a', 'pueblo', 'normal', 'bob',
     dict(skin='#e8c4ae', hair='#1e1418', pants='#1b1b20', shoes='#2a1a1a', belt='#f2f2f2', shirt='#b8344e', sleeve='#b8344e'), 1.0,
     ['¿Qué le sirvo? El café es negro. Como todo aquí.', 'La rocola pone la misma canción a la 1:11.', 'Un muchacho moreno bailó aquí toda la noche. Se reía solo.'],
     [('¿Qué hay de tomar?', 'Café, aguapanela y algo que la casa no recomienda. Tome, este va por la casa.', 'canon:items/pizza'),
      ('Chismes', 'Dicen que la chica pálida pregunta por un tal Juan. Y que encontró a un muchacho que se llama Bana. Pobrecito.', None),
      ('¿Conoció a Kevin?', 'El chistoso. Se tomó algo que le dieron en una fiesta y bailó con alguien que no estaba. Volvió raro de las catacumbas.', None),
      ('¿Usted pidió un deseo?', 'Pedí que alguien se quedara conmigo. Mire cuántos clientes tengo. Ninguno se va.', None)]),
    ('aurelio', 'Don Aurelio el viajero', '#c9a23c', 'mundo', 'thin', 'short',
     dict(skin='#c8a07c', hair='#d8d8d8', pants='#5a4a32', shoes='#3a2a1a', belt='#6a4a2a', shirt='#7a6040', sleeve='#7a6040'), 1.0,
     ['Llevo caminando desde antes de que existiera este camino.', 'Vendo boletos. Bueno, los regalo. Lo caro es volver.', '¿Oyó el bus? Pasa cuando alguien lo necesita.'],
     [('Cuénteme una historia', 'Había un pueblo que no estaba en ningún mapa. Cada vez que alguien pedía un deseo, el pueblo crecía uno. Ya va en 1.311.', None),
      ('Valle Quieto', 'Un lugar en la niebla. Ahí terminan los deseos. Si va, repare el descapotable. Es la única salida.', None),
      ('¿Me da un boleto?', 'Tome. Solo ida. Usted decide si vuelve.', 'canon:items/boleto'),
      ('¿Quién es usted?', 'El que lleva a la gente. Nunca el que la trae.', None)]),
    ('marta', 'Marta la leñadora', '#7aa65a', 'mundo', 'normal', 'short',
     dict(skin='#d2a582', hair='#7a3a1a', pants='#3a4a2a', shoes='#3a2a1a', belt='#2a2a1a', shirt='#9b2f2f', sleeve='#9b2f2f'), 1.0,
     ['Corto leña de día. De noche no salgo. Nadie debería.', 'En este bosque hay un ciervo blanco. Si lo ve, no lo siga.', 'Los árboles crujen distinto cuando el Alto anda cerca.'],
     [('El bosque', 'De noche se llena de papeles pegados en los árboles. Los dejan los que grabaron al Alto. Ninguno terminó el video.', None),
      ('El Alto', 'Alto, de traje, sin cara. Si lo mira mucho, se le tira encima. Si no lo mira, se acerca. Mejor no estar en el bosque.', None),
      ('¿Me regala algo?', 'Tome mi hacha vieja. Corta lo que sea. Bueno, casi.', 'canon:items/hacha'),
      ('¿Vive sola?', 'Con mi perro. Bueno, tenía un perro. Ahora tengo un ruido que ladra.', None)]),
]

HORROR_LINES = ['¡¿Qué es eso?! ¡No lo mire!', 'Ay, Dios mío. Otra vez.', 'Métase a una casa. ¡Ya!']


def models():
    for i, (nid, nombre, color, lugar, build, hs, col, scale, *_r) in enumerate(NPCS):
        at = M.Atlas('npc_' + nid, 900 + i)
        c = dict(col)
        P = M.humanoid_parts(at, c, build)
        for n in ['idle', 'walk_a', 'walk_b', 'reach']:
            M.write_model(f'npc_{nid}_{n}', 'npc_' + nid, M.pose(P, n))
        at.save()
        ah = M.Atlas(f'npc_{nid}_cabeza', 950 + i)
        H = M.head_parts(ah, dict(skin=col['skin'], hair=col['hair']), hs)
        if nid == 'tomas':
            H['alzacuello'] = M.Part(ah, 'alzacuello', [7.2, 8.0, 4.9], [8.8, 8.6, 5.0], '#f4f4f4', faces=['north'])
        if nid == 'ramirez':
            H['gorra'] = M.Part(ah, 'gorra', [4.6, 14.0, 3.6], [11.4, 15.6, 11.4], '#1f2b44')
        if nid == 'aurelio':
            H['sombrero'] = M.Part(ah, 'sombrero', [3.4, 14.2, 3.4], [12.6, 15.0, 12.6], '#5a4028')
            H['copa'] = M.Part(ah, 'copa', [5.0, 15.0, 5.0], [11.0, 17.4, 11.0], '#5a4028')
        base = dict(iris='#2a1a12', brow=col['hair'] if col['hair'] != '#bdbdbd' else '#8a8a8a', lips='#9a5a50')
        for en, st in (('neutral', dict(base, mouth='flat')), ('sonrisa', dict(base, mouth='smile')), ('miedo', dict(base, eyes='wide', mouth='open'))):
            r = M.face_rect(ah)
            fe = M.face_element(ah, r, col['skin'], st, 'face_' + en)
            M.write_model(f'npc_{nid}_cabeza_{en}', f'npc_{nid}_cabeza', M.all_elements(H) + [fe])
        ah.save()


def build(c):
    shim.use(c)
    names = []
    for nid, *_r in NPCS:
        names += [f'npc_{nid}_{n}' for n in ['idle', 'walk_a', 'walk_b', 'reach']] + [f'npc_{nid}_cabeza_{e}' for e in ('neutral', 'sonrisa', 'miedo')]
    shim.models(names, 7320800)
    models()
    from canon import skins as SK
    HS = {'bald': 'bald', 'bob': 'bob', 'emo': 'messy', 'short': 'short'}
    EXTRA = {'tomas': ['collar_white'], 'ramirez': ['cap', 'belt'], 'rosa': ['apron'], 'aurelio': ['cap'], 'ernesto': ['dark_circles'],
             'sofi': ['blush'], 'tono': ['belt'], 'lucia': ['apron'], 'marta': ['belt'], 'wilson': ['dark_circles']}
    TOP = {'tomas': 'long', 'ramirez': 'long', 'aurelio': 'jacket', 'ernesto': 'jacket', 'wilson': 'jacket', 'marta': 'long'}
    for nid, nombre, color, lugar, build_, hs, col, scale, *_r in NPCS:
        cfg = dict(skin=col['skin'], hair=col['hair'], hair_style=HS.get(hs, 'short'), top=col['shirt'], top_style=TOP.get(nid, 'tshirt'),
                   pants=col['pants'], shoes=col['shoes'], extras=EXTRA.get(nid, []), cap=col['pants'] if nid == 'ramirez' else '#5a4028')
        if nid in ('rosa', 'lucia', 'sofi'):
            cfg['pants_style'] = 'skirt'
        SK.build_character('npc_' + nid, cfg, c.out, ('idle', 'walk_a', 'walk_b', 'reach'),
                           [('neutral', 'neutral'), ('sonrisa', 'smile'), ('miedo', 'scared')])
    K = shim.CMD
    c.config('npcs', 'NPCs nuevos (pueblo y viajeros)', 1)
    c.objective('dv.npc', 'trigger')
    for n in (12, 200):
        c.const(n)
    c.on('player', 'scoreboard players enable @s dv.npc\nexecute if score @s dv.npc matches 1.. run function canon:npc/eleccion')
    c.on('second', '''
execute if score #npcs dv.cfg matches 1 as @a[gamemode=!spectator,predicate=canon:en_pueblo,limit=1,sort=random] at @s if predicate canon:azar/1en12 run function canon:npc/pueblo_try
execute if score #npcs dv.cfg matches 1 unless entity @e[type=zombie,tag=dv_npc_mundo] as @a[gamemode=!spectator,predicate=canon:en_superficie,predicate=canon:de_dia,limit=1,sort=random] at @s if predicate canon:visitable if predicate canon:azar/1en1200 run function canon:npc/mundo_try
execute unless score #npcs dv.cfg matches 1 as @e[type=zombie,tag=dv_npcx] at @s run function canon:rig/despawn
''')
    c.npc('dv_npcx', 'npc/tick')
    c.frames('dv_npcx', 'npc/frames')
    c.brain_click('dv_npcx_click', 'zombie', 'dv_npcx', 'npc/clic', 'npc/golpe')
    pueblo = [n for n in NPCS if n[3] == 'pueblo']
    mundo = [n for n in NPCS if n[3] == 'mundo']
    F('npc/pueblo_try', '''
execute store result score #nn dv.tmp if entity @e[type=zombie,tag=dv_npc_pueblo,distance=..72]
execute if score #nn dv.tmp matches ..4 run function canon:npc/pueblo_elegir
''')
    pick('npc/pueblo_elegir', [f'execute unless entity @e[type=zombie,tag=dv_npc_{n[0]}] run function canon:npc/{n[0]}/lugar' for n in pueblo])
    pick('npc/mundo_try', [f'function canon:npc/{n[0]}/lugar' for n in mundo])
    resp_lines = []
    clic_lines = []
    for i, (nid, nombre, color, lugar, build, hs, col, scale, frases, temas) in enumerate(NPCS):
        idx = i + 1
        F(f'npc/{nid}/lugar', f'''
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^12 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^-9 ^ ^6 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:npc/{nid}/summon
kill @e[type=marker,tag=dv_spot]
''')
        F(f'npc/{nid}/summon', rig_summon(['dv_npcx', 'dv_humano', f'dv_npc_{nid}', f'dv_npc_{lugar}'], nombre, color, scale=scale) + '\n'
          f'execute as @e[type=zombie,tag=dv_new,tag=dv_npc_{nid},distance=..2,limit=1,sort=nearest] at @s run function canon:npc/{nid}/init')
        F(f'npc/{nid}/init', f'''
function canon:rig/init_common
{set_cmd('body', K[f'npc_{nid}_idle'])}
{head(K[f'npc_{nid}_cabeza_neutral'])}
scoreboard players set @s dv.say -1
scoreboard players set @s dv.timer 0
scoreboard players set @s dv.state 0
summon minecraft:interaction ~ ~ ~ {{Tags:["dv_link","dv_click","dv_npc_click","dv_xclick","dv_npcx_click","dv_new_link"],width:{0.8 * scale:.2f}f,height:{1.95 * scale:.2f}f,response:1b}}
scoreboard players operation @e[tag=dv_new_link] dv.id = @s dv.id
tag @e[tag=dv_new_link] remove dv_new_link
function canon:x/add_bubble
''')
        pick(f'npc/{nid}/frase', [say(nombre, color, '#f4f0e8', t, 110, '@a[distance=..12]') for t in frases])
        F(f'npc/{nid}/sonrie', head(K[f'npc_{nid}_cabeza_sonrisa']))
        F(f'npc/{nid}/miedo', head(K[f'npc_{nid}_cabeza_miedo']))
        F(f'npc/{nid}/neutral', head(K[f'npc_{nid}_cabeza_neutral']))
        btns = [(lab, f'/trigger dv.npc set {idx * 10 + k + 1}') for k, (lab, _t, _g) in enumerate(temas)] + [('Adiós', f'/trigger dv.npc set {idx * 10 + 9}')]
        clic_lines.append(f'execute if entity @s[tag=dv_npc_{nid}] run {menu("@a[tag=dv_talker]", nombre.upper(), color, btns)}')
        clic_lines.append(f'execute if entity @s[tag=dv_npc_{nid}] run function canon:npc/{nid}/sonrie')
        for k, (lab, texto, regalo) in enumerate(temas):
            body = say(nombre, color, '#f4f0e8', texto, 160, '@a[distance=..12]')
            if regalo == 'bendicion':
                body += '\neffect give @a[tag=dv_ntalk] minecraft:regeneration 10 1 true\neffect clear @a[tag=dv_ntalk] minecraft:darkness\n' \
                        'particle minecraft:end_rod ~ ~1.5 ~ 0.6 0.8 0.6 0.02 30 normal\nplaysound minecraft:block.bell.resonate neutral @a[distance=..16] ~ ~ ~ 0.6 1.4'
            elif regalo:
                gtag = f'dv_ng_{nid}'
                F(f'npc/{nid}/regalo', f'loot give @a[tag=dv_ntalk] loot {regalo}\ntag @a[tag=dv_ntalk] add {gtag}\nplaysound canon:fx.gift neutral @a[distance=..12] ~ ~ ~ 0.8 1')
                body += f'\nexecute unless entity @a[tag=dv_ntalk,tag={gtag}] run function canon:npc/{nid}/regalo'
            F(f'npc/{nid}/t{k + 1}', body)
            resp_lines.append(f'execute if entity @s[tag=dv_npc_{nid}] if score #nc dv.tmp matches {idx * 10 + k + 1} run function canon:npc/{nid}/t{k + 1}')
        F(f'npc/{nid}/adios', say(nombre, color, '#f4f0e8', 'Cuídese. Y no salga de noche.', 60, '@a[distance=..12]'))
        resp_lines.append(f'execute if entity @s[tag=dv_npc_{nid}] if score #nc dv.tmp matches {idx * 10 + 9} run function canon:npc/{nid}/adios')
        c.admin(f'/function canon:admin/npc/{nid}', f'Traer a {nombre}')
        F(f'admin/npc/{nid}', f'execute positioned ^ ^ ^3 run function canon:npc/{nid}/summon')
    F('npc/clic', 'execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0\nscoreboard players set @s dv.timer 0\n' + '\n'.join(clic_lines))
    F('npc/eleccion', '''
tag @s add dv_ntalk
scoreboard players operation #nc dv.tmp = @s dv.npc
scoreboard players set @s dv.npc 0
execute as @e[type=zombie,tag=dv_npcx,distance=..12,limit=1,sort=nearest] at @s run function canon:npc/responde
tag @s remove dv_ntalk
''')
    F('npc/responde', '\n'.join(resp_lines))
    pick('npc/golpe_dice', [say('?', '#c0c0c0', '#f4f0e8', t, 70, '@a[distance=..12]') for t in
                            ['¡Oiga! ¿Qué le pasa?', 'Así no se trata a la gente, mijo.', 'Le voy a contar a Ramírez.']])
    F('npc/golpe', 'function canon:npc/golpe_dice')
    # comportamiento
    F('npc/tick', '''
function canon:x/links_follow
scoreboard players remove @s[scores={dv.say=1..}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players add @s dv.timer 1
execute unless entity @a[distance=..96] run function canon:rig/despawn
tag @a remove dv_wtgt
tag @a[gamemode=!spectator,distance=..7,limit=1,sort=nearest] add dv_wtgt
execute if entity @e[tag=dv_horror,distance=..14] if score @s dv.say matches ..0 run function canon:npc/asustado
execute if entity @a[tag=dv_wtgt] if score #m4 dv.clock matches 0 run function canon:x/face
execute if entity @a[tag=dv_wtgt] if score #m200 dv.clock matches 90 if score @s dv.say matches ..0 if predicate canon:azar/1en2 run function canon:npc/frase
execute unless entity @a[tag=dv_wtgt] run function canon:npc/pasear
tag @a remove dv_wtgt
''')
    F('npc/frase', '\n'.join(f'execute if entity @s[tag=dv_npc_{n[0]}] run function canon:npc/{n[0]}/frase' for n in NPCS))
    F('npc/asustado', '\n'.join(f'execute if entity @s[tag=dv_npc_{n[0]}] run function canon:npc/{n[0]}/miedo' for n in NPCS) + '\n' +
      'function canon:npc/asustado_dice')
    pick('npc/asustado_dice', [say('!!!', '#c94a4a', '#ffe0e0', t, 80, '@a[distance=..16]') for t in HORROR_LINES])
    F('npc/pasear', '''
scoreboard players add @s dv.state 1
execute if score @s dv.state matches 200.. run scoreboard players set @s dv.state 0
execute if score @s dv.state matches 1 if predicate canon:azar/1en2 run tp @s ~ ~ ~ ~120 0
execute if score @s dv.state matches 1 if predicate canon:azar/1en2 run tp @s ~ ~ ~ ~-90 0
execute if score @s dv.state matches 1..50 if block ^ ^ ^0.6 #canon:pasable if block ^ ^1 ^0.6 #canon:pasable run function canon:npc/paso
execute if score @s dv.state matches 1..50 unless block ^ ^ ^0.6 #canon:pasable run tp @s ~ ~ ~ ~150 0
''')
    F('npc/paso', '''
tag @s add dv_xwalk
tp @s ^ ^ ^0.07
execute at @s run function canon:diana/ground
''')
    F('npc/frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
''')
