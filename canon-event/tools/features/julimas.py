"""Canon Event 10: Juli habla de todos (temas según lo que ya descubriste y comenta tu día), Juli se encuentra con otros
personajes en el mundo, el jardín secreto tiene 5 misiones, Kevin te reta a aguantar la noche sin luz, y los cofres de tu
casa se pasan cosas entre ellos (poltergeist).
"""
from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon.ctx import bubble, chat, btn

JC, JB = '#f2a7c3', '#fde3ee'
TEMAS = [  # clave, adv del cuaderno (None = siempre), botón, frases
    ('dani', 'dani', 'Dani', ['Dani me cuida desde afuera. Me peina aunque no me despierte. A veces la oigo llorar en la cocina y hacerse la fuerte.',
                              'Dile a Dani que no venda tan barato. Y que coma ella también, siempre se le olvida.']),
    ('diana', 'dhum', 'Diana', ['Diana no siempre fue así. Antes cantaba en el colegio. Lo que la torció fue querer demasiado.',
                                'Si Diana te encuentra, no corras hacia lo oscuro. Corre hacia la luz. Ella odia que la vean bien.']),
    ('kevin', 'kevin', 'Kevin', ['Kevin es el único que me hace reír desde aquí. A veces oigo su música en el sueño.',
                                 'Kevin bajó a las catacumbas una vez. Volvió con una sonrisa que no era del todo suya. Cuídalo.']),
    ('abuela', 'abuela', 'La Abuela Esmeralda', ['La abuela Esmeralda me daba aguapanela cuando era chiquita. La de verdad. La de noche nunca me ha dado nada.',
                                                 'Si la abuela te pide que la acompañes de noche, dile que no. Ella misma me lo enseñó, cuando era ella.']),
    ('luna', 'luna', 'Luna', ['¡Luna! Dile que la extraño. Los perros pueden entrar a los sueños, ¿sabías? Ella a veces duerme en mi cama.',
                              'Si un día Luna no te mueve la cola, no es Luna. Hazme caso.']),
    ('mariana', 'mariana', 'Mariana', ['Mariana bailaba con Felipe en la fiesta del lago. Yo estaba ahí. Fue la última vez que bailó con alguien.',
                                       'Mariana no es mala. Está buscando. Cuando uno busca mucho tiempo, se le olvida ser amable.']),
    ('narrador', 'narrador', 'El Narrador', ['¿El hombre de ojeras? Él estaba aquí antes que la casa. Creo que él la soñó primero.',
                                             'No le creas todo al Narrador. Cuenta la verdad, pero no toda.']),
    ('nietos', 'nietos', 'Los nietos', ['Los primos de Santi juegan en el bosque. A veces vienen a mi jardín a buscar luciérnagas.',
                                        'Tomasito me enseñó a silbar. Aquí no suena, pero igual lo intento.']),
]
SANTI = ['Todos los días. Aunque aquí no hay días. Cuento las veces que vienes.',
         'Santi... cuando despierte, ¿me vas a reconocer? Yo a ti sí. Siempre.',
         'Te guardé una flor de cada visita. Ya no caben en el cuarto.']
ENCUENTROS = [  # tag del otro, tipo, nombre, color, línea de Juli, respuesta
    ('dv_dani', 'zombie', 'Dani', '#9fc3a8', '¡Dani! ¿Le diste de comer a Luna?', 'Juli... ¿estás despierta? ¿O estoy soñando yo?'),
    ('dv_kevin', 'zombie', 'Kevin', '#ffb347', 'Kevin, baja esa música, que me despiertas.', '¡Juli! Jajaja... espera, ¿tú no estabas dormida?'),
    ('dv_luna', 'wolf', 'Luna', '#ffd27a', '¡Luna! Ven, ven, mi niña...', '(Luna mueve la cola tan fuerte que se cae de lado.)'),
    ('dv_abuela', 'zombie', 'Abuela Esmeralda', '#c9a27a', 'Abuela Esmeralda... ¿es usted de verdad?', 'Hoy sí, mijita. Hoy sí. Pero no me espere de noche.'),
]
MISIONES = {1: 'Toca las tres campanitas de viento que cuelgan sobre los faroles de las esquinas.',
            2: 'Enterré una carta junto al árbol, en la tierra suelta. Búscala.',
            3: 'Siéntate en el columpio. Quiero contarte algo.',
            4: 'Tira cualquier cosa al estanque y pide un deseo. No me lo digas.',
            5: 'Ya hiciste todo lo que te pedí. Quédate un rato conmigo.'}
LUZ = ['torch', 'soul_torch', 'lantern', 'soul_lantern', 'glowstone', 'sea_lantern', 'jack_o_lantern', 'shroomlight', 'campfire',
       'soul_campfire', 'redstone_torch', 'end_rod', 'ochre_froglight', 'verdant_froglight', 'pearlescent_froglight', 'glow_berries']


def build(c):
    shim.use(c)
    jsay = lambda t, ticks=140: bubble('dv_juli_bubble', t, JB, ticks) + '\n' + chat('Juli', JC, t, '@a[distance=..10]')
    jvoz = lambda t, sel='@s': f'tellraw {sel} ["",{jt("Juli: ", JC, bold=True)},{jt(t, JB, True)}]'
    for o in ('dv.jmis', 'dv.jcamp'):
        c.objective(o)

    # ================================================================ JULI: temas sobre todos y tu día (casa blanca)
    c.patch('casa/clicked', lambda s: s if 'dv.jr set 11' in s else s.rstrip('\n') + '\n' + menu('@a[tag=dv_talker]', '', JC, [
        ('Hablemos de alguien...', '/trigger dv.jr set 11'), ('¿Qué viste de mi día?', '/trigger dv.jr set 12')]) + '\n')
    run_add = ['execute if score #jc dv.tmp matches 11 run function canon:jm/temas', 'execute if score #jc dv.tmp matches 12 run function canon:jm/dia',
               'execute if score #jc dv.tmp matches 30 run function canon:jm/t/santi']
    temas = ['tellraw @a[tag=dv_jtalk] ' + jt('\n¿De quién quieres hablar?', JC)]
    for i, (k, adv, nom, frases) in enumerate(TEMAS):
        n = 21 + i
        c.pick(f'jm/t/{k}', [jsay(t) for t in frases])
        run_add.append(f'execute if score #jc dv.tmp matches {n} run function canon:jm/t/{k}')
        temas.append(f'execute if entity @a[tag=dv_jtalk,advancements={{canon:cuaderno/{adv}=true}}] run tellraw @a[tag=dv_jtalk] [{btn(" [" + nom + "] ", f"/trigger dv.jr set {n}")}]')
    temas.append(f'execute if entity @a[tag=dv_jtalk,tag=dv_santi] run tellraw @a[tag=dv_jtalk] [{btn(" [¿Me extrañas?] ", "/trigger dv.jr set 30")}]')
    temas.append('tellraw @a[tag=dv_jtalk] ' + jt('(Aparecen más nombres a medida que conoces a la gente.)', 'gray', True))
    F('jm/temas', '\n'.join(temas))
    c.pick('jm/t/santi', [jsay(t) for t in SANTI])
    c.patch('casa/c/run', lambda s: s if 'jm/temas' in s else s.rstrip('\n') + '\n' + '\n'.join(run_add) + '\n')
    F('jm/dia', '\n'.join([
        jsay('Déjame ver tu día...', 60),
        'execute as @a[tag=dv_jtalk,scores={dv.racha=3..}] run ' + 'tellraw @s ["",' + jt('Juli: ', JC, bold=True) + ',' + jt('Llevas ', JB, True) +
        ',{"score":{"name":"@s","objective":"dv.racha"},"color":"white"},' + jt(' noches sin morir. Estoy orgullosa de ti.', JB, True) + ']',
        'execute as @a[tag=dv_jtalk,scores={dv.racha=0}] run ' + jvoz('Hoy te vi caer. No me gustó nada. Ten más cuidado, por favor.'),
        'execute as @a[tag=dv_jtalk,tag=dv_pagtodas] run ' + jvoz('Ya tienes todas las páginas de Diana. Ya sabes cómo termina esto. No lo hagas solo.'),
        'execute as @a[tag=dv_jtalk,tag=dv_pag1,tag=!dv_pagtodas] run ' + jvoz('Estás juntando las páginas de Diana. Léelas despacio. Duelen.'),
        'execute if score #felipe_fin dv.dev matches 1 as @a[tag=dv_jtalk] run ' + jvoz('Mariana encontró a Felipe. Hoy la casa huele a lago.'),
        'execute if score #jefe_ganado dv.dev matches 1 as @a[tag=dv_jtalk] run ' + jvoz('Lo lograron. Ya casi me despierto. Gracias, de verdad.'),
        'execute as @a[tag=dv_jtalk,scores={dv.miedo=60..}] run ' + jvoz('Tienes miedo. Se te nota hasta aquí. Quédate un rato, aquí no entra nada.'),
        'execute as @a[tag=dv_jtalk,scores={dv.nietos=5..}] run ' + jvoz('Encontraste a los nietos de la abuela. Ahora juegan en mi jardín.'),
        'execute as @a[tag=dv_jtalk] run ' + jvoz('Gracias por venir a verme. Aunque sea en sueños.'),
    ]))

    # ================================================================ JULI se encuentra con otros personajes en el mundo
    enc = ['scoreboard players set #jxf dv.tmp 0']
    for i, (tag, typ, nom, col, lj, lo) in enumerate(ENCUENTROS):
        cond = 'if predicate canon:de_dia ' if tag == 'dv_abuela' else ''
        F(f'jm/enc/e{i}', jsay(lj, 120) + f'\ntellraw @a[distance=..16] ["",{jt(nom + ": ", col, bold=True)},{jt(lo, "#e8e8e8", True)}]'
          f'\nscoreboard players set #jxf dv.tmp 1\nscoreboard players set #jx_cd dv.dev 600')
        enc.append(f'execute if score #jxf dv.tmp matches 0 {cond}if entity @e[type={typ},tag={tag},distance=..12] run function canon:jm/enc/e{i}')
    F('jm/encuentro', '\n'.join(enc))
    c.on('second', '''
execute if score #jx_cd dv.dev matches 1.. run scoreboard players remove #jx_cd dv.dev 1
execute unless score #jx_cd dv.dev matches 1.. as @e[type=zombie,tag=dv_juli,tag=!dv_jcasa,limit=1] at @s run function canon:jm/encuentro
''')

    # ================================================================ JARDÍN: 5 misiones
    c.patch('rel/jardin/premio', lambda s: s if 'dv.jmis' in s else s.rstrip('\n') + '\nexecute unless score @s dv.jmis matches 1.. run scoreboard players set @s dv.jmis 1\n')
    c.patch('rel/jardin/entrar2', lambda s: s if 'jm/jardin/llegar' in s else s.rstrip('\n') + '\nfunction canon:jm/jardin/llegar\n')
    F('jm/jardin/llegar', 'execute unless entity @e[type=interaction,tag=dv_jm_obj,x=33,y=105,z=33,dx=15,dy=15,dz=15] run function canon:jm/jardin/objetos\n'
      'schedule function canon:jm/jardin/mision_todos 60t replace')
    F('jm/jardin/mision_todos', 'execute in canon:sueno_blanco as @a[x=31,y=100,z=31,dx=18,dy=25,dz=18] run function canon:jm/jardin/mision')
    mis = ['execute unless score @s dv.jmis matches 1.. run tellraw @s ' + jt('(Misión del jardín: atrapa las 5 luciérnagas.)', 'gray', True)]
    for k, t in MISIONES.items():
        mis.append(f'execute if score @s dv.jmis matches {k} run ' + jvoz(t))
    mis.append('execute if score @s dv.jmis matches 1.. run tellraw @s ["",' + jt('(Misión del jardín ', 'gray', True) +
               ',{"score":{"name":"@s","objective":"dv.jmis"},"color":"white"},' + jt(' de 5)', 'gray', True) + ']')
    F('jm/jardin/mision', '\n'.join(mis))
    obj = lambda tag, x, y, z, w, h: (f'summon minecraft:interaction {x} {y} {z} {{Tags:["dv_jm_obj","{tag}","dv_click","dv_npc_click"],width:{w}f,height:{h}f,response:1b}}')
    camp = [(33.5, 111.1, 33.5), (47.5, 111.1, 47.5), (33.5, 111.1, 47.5)]
    lines = []
    for i, (x, y, z) in enumerate(camp, 1):
        lines.append(f'summon minecraft:item_display {x} {y + 0.45:.2f} {z} {{Tags:["dv_jm_vis"],item:{{id:"minecraft:bell",Count:1b}},brightness:{{sky:15,block:15}},'
                     'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.45f,0.45f,0.45f],right_rotation:[0f,0f,0f,1f]}}')
        lines.append(obj(f'dv_jm_c{i}', x, y, z, 0.7, 0.7))
    lines += ['setblock 46 109 36 minecraft:coarse_dirt', obj('dv_jm_carta', 46.5, 109.9, 36.5, 1.0, 0.25),
              obj('dv_jm_columpio', 37.5, 111.0, 36.5, 0.9, 0.9)]
    F('jm/jardin/objetos', '\n'.join(lines))
    for i in range(1, 4):
        c.click(f'dv_jm_c{i}', f'jm/jardin/campana{i}')
        F(f'jm/jardin/campana{i}', f'''
playsound minecraft:block.amethyst_block.chime player @a[distance=..12] ~ ~ ~ 1 {1.2 + 0.2 * i:.1f}
particle minecraft:end_rod ~ ~0.6 ~ 0.2 0.2 0.2 0.01 8 normal
execute as @a[tag=dv_talker,scores={{dv.jmis=1}},tag=!dv_jmc{i}] run function canon:jm/jardin/campana_ok{i}
''')
        F(f'jm/jardin/campana_ok{i}', f'tag @s add dv_jmc{i}\nscoreboard players add @s dv.jcamp 1\n'
          'execute if score @s dv.jcamp matches 3.. run function canon:jm/jardin/hecha_campanas')
    F('jm/jardin/hecha_campanas', 'tag @s remove dv_jmc1\ntag @s remove dv_jmc2\ntag @s remove dv_jmc3\nscoreboard players set @s dv.jcamp 0\n' +
      jvoz('¿Oíste? Así sonaba la casa antes, cuando todos estaban despiertos. Gracias.') + '\nloot give @s loot canon:items/petalo\nfunction canon:jm/jardin/siguiente')
    c.click('dv_jm_carta', 'jm/jardin/carta')
    F('jm/jardin/carta', 'execute as @a[tag=dv_talker,scores={dv.jmis=2}] run function canon:jm/jardin/carta_ok\nplaysound minecraft:block.rooted_dirt.break block @a[distance=..8] ~ ~ ~ 1 0.9')
    F('jm/jardin/carta_ok', 'loot give @s loot canon:items/carta\n' + jvoz(
        'Esa carta la escribí antes de dormirme. Dice: «Si me quedo dormida mucho tiempo, no me olviden. Yo los sigo oyendo». Ya está. Ya la leíste.') +
      '\nfunction canon:jm/jardin/siguiente')
    c.click('dv_jm_columpio', 'jm/jardin/columpio')
    F('jm/jardin/columpio', 'playsound minecraft:block.chain.step block @a[distance=..8] ~ ~ ~ 1 0.7\nexecute as @a[tag=dv_talker,scores={dv.jmis=3}] run function canon:jm/jardin/columpio_ok')
    F('jm/jardin/columpio_ok', jvoz('Mi papá colgó este columpio el día que nací. Cuando me dormí, lo traje aquí para que no se oxidara. '
                                   'A veces se mueve solo. Soy yo, empujando desde el otro lado.') + '\nfunction canon:jm/jardin/siguiente')
    c.on('second', 'execute in canon:sueno_blanco as @e[type=item,x=34,y=107,z=43,dx=4,dy=4,dz=4] at @s if block ~ ~ ~ minecraft:water run function canon:jm/jardin/estanque')
    F('jm/jardin/estanque', 'execute as @p[distance=..14,scores={dv.jmis=4}] run function canon:jm/jardin/deseo\nparticle minecraft:glow ~ ~0.5 ~ 0.4 0.2 0.4 0 20 normal\n'
      'playsound minecraft:entity.generic.splash block @a[distance=..12] ~ ~ ~ 0.8 1.3\nkill @s')
    F('jm/jardin/deseo', jvoz('Pediste un deseo. No me lo digas. Los deseos de aquí no cobran nada. Toma, esto es por ayudarme con todo.') + '''
loot give @s loot canon:items/petalo
loot give @s loot canon:items/petalo
loot give @s loot canon:items/billete
loot give @s loot canon:items/billete
loot give @s loot canon:items/billete
function canon:rel/pag/dar
advancement grant @s only canon:logros/jardin2
function canon:jm/jardin/siguiente
''')
    F('jm/jardin/siguiente', 'scoreboard players add @s dv.jmis 1\nplaysound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4\nfunction canon:jm/jardin/mision')
    c.json('data/canon/advancements/logros/jardin2.json', {'parent': 'canon:logros/raiz', 'display': {
        'icon': {'item': 'minecraft:bell'}, 'title': {'text': 'Todo el jardín', 'color': '#d77a8a'}, 'description': {'text': 'Termina las 5 misiones del jardín de Juli.'},
        'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}, 'criteria': {'c': {'trigger': 'minecraft:impossible'}}})

    # ================================================================ KEVIN: aguanta la noche sin luz
    c.json('data/canon/predicates/mano_luz.json', {'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {s: {'items': [f'minecraft:{x}' for x in LUZ]}}}}
        for s in ('mainhand', 'offhand')]})
    c.patch('kevin/clicked', lambda s: s if 'dv.kv set 14' in s else s.rstrip('\n') + '\nexecute unless score #kev dv.dev matches 1.. run ' +
            menu('@a[tag=dv_talker]', '', '#ffb347', [('Reto: aguanta la noche sin luz', '/trigger dv.kv set 14')]) + '\n')
    c.patch('kevin/c/run', lambda s: s if 'jm/kevin/noche' in s else s.rstrip('\n') + '\nexecute if score #kc dv.tmp matches 14 run function canon:jm/kevin/noche\n')
    ks = lambda t, sel='@a[distance=..20]': say('Kevin', '#ffb347', '#ffd27a', t, 140, sel)
    F('jm/kevin/noche', '''
execute store result score #kd dv.tmp run time query daytime
execute if score #kd dv.tmp matches 1000..11000 run function canon:jm/kevin/noche_dia
execute unless score #kd dv.tmp matches 1000..11000 as @a[tag=dv_ktalk] run function canon:jm/kevin/noche_acepta
''')
    F('jm/kevin/noche_dia', ks('Eso es de noche, mano. Vuelve cuando se esté poniendo el sol.'))
    F('jm/kevin/noche_acepta', 'tag @s add dv_kreto\ntellraw @s ' + jt('Kevin: ¡Reto! Aguanta hasta el amanecer sin luz. Nada de antorchas, faroles ni linterna en la mano. '
                                                                    'Si lo logras, te doy algo bueno. Si no... me debes dos arepas. Jajaja.', '#ffd27a', True) +
      '\ntitle @s actionbar {"text":"Reto de Kevin: sin luz hasta el amanecer","color":"#ffb347"}')
    c.on('second', '''
execute as @a[tag=dv_kreto,predicate=canon:mano_luz] run function canon:jm/kevin/noche_pierde
execute as @a[tag=dv_kreto,scores={dv.lint=1..}] run function canon:jm/kevin/noche_pierde
execute store result score #kd2 dv.tmp run time query daytime
execute if score #kd2 dv.tmp matches 0..60 as @a[tag=dv_kreto] run function canon:jm/kevin/noche_gana
''')
    F('jm/kevin/noche_pierde', 'tag @s remove dv_kreto\ntellraw @s ' + jt('Kevin (desde lejos): ¡Jajaja, prendiste luz! Perdiste. Me debes dos arepas.', '#ffb347', True) +
      '\nplaysound canon:kevin.laugh neutral @s ~ ~ ~ 0.8 1')
    F('jm/kevin/noche_gana', '''
tag @s remove dv_kreto
title @s times 10 60 20
title @s title {"text":"¡AGUANTASTE LA NOCHE!","color":"#ffb347","bold":true}
tellraw @s {"text":"Kevin: Uy, mano... aguantaste toda la noche a oscuras. Respeto. Toma, te lo ganaste.","color":"#ffd27a","italic":true}
give @s minecraft:diamond 2
loot give @s loot canon:items/billete
loot give @s loot canon:items/billete
loot give @s loot canon:items/billete
loot give @s loot canon:sus/campanita
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1
''')
    c.patch('rel/muerte', lambda s: s if 'dv_kreto' in s else s.rstrip('\n') + '\nexecute if entity @s[tag=dv_kreto] run function canon:jm/kevin/noche_pierde\n')

    # ================================================================ POLTERGEIST: los cofres se pasan cosas
    F('jm/polter/cofres', 'function canon:rel/polter/scan_cofre\nexecute store result score #nc dv.tmp if entity @e[type=marker,tag=dv_pco]\n'
      'execute if score #nc dv.tmp matches 2.. run function canon:jm/polter/cofres2\nkill @e[type=marker,tag=dv_pco]')
    F('jm/polter/cofres2', '''
tag @e[type=marker,tag=dv_pco,limit=1,sort=random] add dv_pcA
tag @e[type=marker,tag=dv_pco,tag=!dv_pcA,limit=1,sort=random] add dv_pcB
scoreboard players set #ts dv.tmp -1
data remove storage canon:tmp cof
execute at @e[type=marker,tag=dv_pcB,limit=1] run function canon:jm/polter/libre
execute if score #ts dv.tmp matches 0.. at @e[type=marker,tag=dv_pcA,limit=1] run function canon:jm/polter/sacar
execute if score #ts dv.tmp matches 0.. if data storage canon:tmp cof at @e[type=marker,tag=dv_pcB,limit=1] run function canon:jm/polter/poner
''')
    F('jm/polter/libre', '\n'.join(f'execute unless data block ~ ~ ~ Items[{{Slot:{n}b}}] run scoreboard players set #ts dv.tmp {n}' for n in range(26, -1, -1)))
    F('jm/polter/sacar', 'data modify storage canon:tmp cof set from block ~ ~ ~ Items[-1]\nexecute if data storage canon:tmp cof run data remove block ~ ~ ~ Items[-1]\n'
      'execute if data storage canon:tmp cof run playsound minecraft:block.chest.open block @a[distance=..16] ~ ~ ~ 0.8 0.7')
    F('jm/polter/poner', '''
execute store result storage canon:tmp cof.Slot byte 1 run scoreboard players get #ts dv.tmp
data modify block ~ ~ ~ Items append from storage canon:tmp cof
playsound minecraft:block.chest.close block @a[distance=..16] ~ ~ ~ 0.8 0.6
tellraw @a[distance=..16] {"text":"Oíste un cofre abrirse... y otro cerrarse. Algo cambió de lugar.","color":"gray","italic":true}
''')

    # ================================================================ admin
    for nm, body, desc in [('juli_temas', 'tag @s add dv_jtalk\nfunction canon:jm/temas\ntag @s remove dv_jtalk', 'Temas de Juli (ver la lista)'),
                           ('cofres', 'function canon:jm/polter/cofres', 'Los cofres se pasan algo'),
                           ('reto_noche', 'function canon:jm/kevin/noche_acepta', 'Reto de Kevin: noche sin luz')]:
        F(f'admin/jm/{nm}', body)
        c.admin(f'/function canon:admin/jm/{nm}', desc)
