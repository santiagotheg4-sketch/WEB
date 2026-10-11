from canon.shim import *  # noqa: F401,F403
from canon import shim
from canon.models import *  # noqa: F401,F403
import random, json

# ---------------------------------------------------------------- modelos
def models_kevin():
    at = Atlas('kevin', 11)
    skin = '#8a5a3c'

    def shirt_paint(a, f, r):
        # camisa negra "bacana": estampado rojo/blanco en el frente
        if f == 'north':
            x, y, w, h = r
            cx, cy = x + w // 2, y + h // 2 - 2
            for t in range(-5, 6):
                px(a, cx + t, cy + abs(t) // 2, '#d33b3b')
                px(a, cx + t, cy + 1 + abs(t) // 2, '#e8e2d0')
            rect(a, cx - 2, cy + 4, 5, 3, '#e8e2d0')
            rect(a, cx - 1, cy + 5, 3, 1, '#d33b3b')

    def arm_paint(a, f, r):
        x, y, w, h = r
        rect(a, x, y + int(h * 0.55), w, h - int(h * 0.55), skin)

    def shoe_paint(a, f, r):
        x, y, w, h = r
        rect(a, x, y + h - 2, w, 2, '#f2f2f2')

    c = dict(skin=skin, pants='#1b1b1e', shoes='#2a2a2a', belt='#151517', shirt='#18181b', sleeve='#18181b',
             shirt_paint=shirt_paint, arm_paint=arm_paint, shoe_paint=shoe_paint, wide_shoulders=0.3, arm_w=2.3)
    P = humanoid_parts(at, c)
    for n in ['idle', 'walk_a', 'walk_b', 'dance_a', 'dance_b', 'laugh', 'offer']:
        write_model('kevin_' + n, 'kevin', pose(P, n))
    at.save()
    # cabeza
    ah = Atlas('kevin_cabeza', 12)
    H = head_parts(ah, dict(skin=skin, hair='#121010'), 'short')
    base = dict(iris='#1d120c', brow='#0f0b09', lips='#5a2e26')
    exprs = {
        'neutral': dict(base, mouth='smile'),
        'risa': dict(base, eyes='closed', mouth='laugh'),
        'drogado': dict(base, eyes='red', mouth='grin'),
        'miedo': dict(base, eyes='wide', mouth='open'),
    }
    for n, st in exprs.items():
        r = face_rect(ah)
        fe = face_element(ah, r, skin, st, 'face_' + n)
        write_model('kevin_cabeza_' + n, 'kevin_cabeza', all_elements(H) + [fe])
    ah.save()



def models_fiesteros():
    looks = [
        ('fiestero_0', '#c8a07c', '#2c6fd6', '#2d2d33', '#f2f2f2', '#2a1a10', 'short'),
        ('fiestero_1', '#a7774f', '#d6337a', '#1f2a44', '#151515', '#120c08', 'bob'),
        ('fiestero_2', '#e6c7ae', '#2fbf7a', '#3a3a3a', '#ffffff', '#c58f3a', 'short'),
    ]
    for name, skin, shirt, pants, shoes, hair, hs in looks:
        at = Atlas(name, sum(map(ord, name)))
        c = dict(skin=skin, pants=pants, shoes=shoes, belt='#222226', shirt=shirt, sleeve=shirt)
        P = humanoid_parts(at, c)
        H = head_parts(at, dict(skin=skin, hair=hair), hs)
        r = face_rect(at)
        fe = face_element(at, r, skin, dict(mouth='smile', eyes='closed'), 'face')
        # mirada fija (cuando la fiesta se pudre)
        r2 = face_rect(at)
        fe2 = face_element(at, r2, skin, dict(mouth='none', eyes='void'), 'face')
        head = all_elements(H)
        write_model(name + '_dance_a', name, pose(P, 'dance_a') + head + [fe])
        write_model(name + '_dance_b', name, pose(P, 'dance_b') + head + [fe])
        write_model(name + '_stare', name, pose(P, 'idle') + head + [fe2])
        at.save()



def models_alto():
    at = Atlas('alto', 51)
    c = dict(skin='#f1f1f1', pants='#0b0b0d', shoes='#060606', belt='#0b0b0d', shirt='#0e0e11', sleeve='#0e0e11')

    def tie(a, f, r):
        if f == 'north':
            x, y, w, h = r
            rect(a, x + w // 2 - 3, y, 6, h, '#f4f4f4')
            rect(a, x + w // 2 - 1, y, 2, h - 3, '#6e0f12')
    c['shirt_paint'] = tie
    P = humanoid_parts(at, c, 'thin')
    H = head_parts(at, dict(skin='#f4f4f4', hair='#f4f4f4'), 'bald')
    r = face_rect(at)
    fe = face_element(at, r, '#f4f4f4', dict(eyes='none', mouth='none', nose=False), 'face')
    head = all_elements(H) + [fe]
    for n in ['idle', 'walk_a', 'walk_b', 'reach']:
        write_model('alto_' + n, 'alto', pose(P, n) + head)
    at.save()



def models_masa():
    at = Atlas('masa', 61)
    flesh = '#8e3b3f'

    def veins(a, f, r):
        x, y, w, h = r
        for _ in range(w * h // 18):
            px(a, x + a.rng.randrange(w), y + a.rng.randrange(h), '#5a1d22')
        if f in ('north', 'east', 'west', 'up') and w > 8 and h > 6:
            ex, ey = x + a.rng.randrange(2, w - 4), y + a.rng.randrange(1, h - 3)
            rect(a, ex, ey, 3, 2, '#efe6c9'); px(a, ex + 1, ey, '#0a0a0a')
    blobs = [
        ('b0', [1, -14, 2], [15, -7, 14]),
        ('b1', [3, -8, 4], [13, -2, 12]),
        ('b2', [5, -3, 6], [11, 2, 11]),
        ('b3', [-2, -14, 5], [3, -9, 11]),
        ('b4', [13, -14, 4], [18, -10, 10]),
    ]
    P = {n: Part(at, n, a, b, flesh, paint=veins) for n, a, b in blobs}
    mouth = Part(at, 'boca', [5, -10, 1.6], [11, -7, 2.0], '#1a0505', faces=['north'])
    P['boca'] = mouth
    write_model('masa_idle', 'masa', all_elements(P))
    pa = [p.element() if n not in ('b2', 'b1') else p.element(rot=(22.5, 'z', [8, -8, 8])) for n, p in P.items()]
    pb = [p.element() if n not in ('b2', 'b1') else p.element(rot=(-22.5, 'z', [8, -8, 8])) for n, p in P.items()]
    write_model('masa_a', 'masa', pa)
    write_model('masa_b', 'masa', pb)
    at.save()




# ---------------------------------------------------------------- lógica


def kv_say(text, ticks=90, sel='@a[distance=..20]'):
    return bubble('dv_kbubble', text, '#ffd27a', ticks) + '\n' + chat('Kevin', '#ffb347', text, sel)


JOKES = [
    '¿Qué le dice un techo a otro? Techo de menos.',
    '¿Cómo se despiden los químicos? Ácido un placer.',
    'Fui al médico y le dije que me dolía aquí, aquí y aquí. Tenía el dedo roto.',
    '¿Por qué el libro de matemáticas está triste? Porque tiene muchos problemas.',
    'Mi abuela me dijo que viviera cada día como si fuera el último. Me pasé el día llorando y llamando a todos.',
    '¿Qué hace una abeja en el gimnasio? ¡Zum-ba!',
    'Le pregunté a la Devota si quería ser mi amiga. Ahora no me deja dormir. Literal.',
    '¿Sabes cuál es el colmo de un fantasma? Que lo dejen en visto.',
    '¿Qué le dijo el pez a otro pez? Nada.',
    'Mariana me miró una vez. Una. Ya no tengo cejas.',
    'Dicen que en la mina hay un man de negro. Yo digo que es el que vende pan. Nunca está.',
    'Me compré un libro de anti-gravedad. No lo puedo soltar.',
]

KEVIN_HOW = [
    'Bien, bien. Bueno, ayer vi una sombra mirándome desde el techo, pero bien.',
    'Con hambre. Siempre con hambre. ¿Tienes pan?',
    'Tranquilo, parce. Mientras tú estés vivo, yo estoy feliz.',
    'Raro. Desde la fiesta escucho música techno en todas partes.',
    'Mejor que nunca. Bueno, mejor que la semana pasada, que me perdí tres días.',
]


def gen_kevin():
    K = CMD
    body, hd = K['kevin_idle'], K['kevin_cabeza_neutral']
    risa, droga, miedo = K['kevin_cabeza_risa'], K['kevin_cabeza_drogado'], K['kevin_cabeza_miedo']
    F('kevin/summon', rig_summon(['dv_kevin'], 'Kevin', '#ffb347') + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_kevin,distance=..2,limit=1,sort=nearest] at @s run function canon:kevin/init')
    F('kevin/init', f'''
function canon:rig/init_common
{set_cmd('body', body)}
{head(hd)}
scoreboard players set @s dv.mode 0
scoreboard players set @s dv.say -1
scoreboard players set @s dv.timer 600
summon minecraft:interaction ~ ~ ~ {{Tags:["dv_link","dv_click","dv_npc_click","dv_kev_click","dv_xclick","dv_new_link"],width:0.8f,height:1.95f,response:1b}}
function canon:x/add_bubble
''')
    # global
    F('kevin/g/off', '''
execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn
execute as @e[type=zombie,tag=dv_kfake] at @s run function canon:rig/despawn
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/abort
''')
    F('kevin/g/run', '''
execute if score #kprog dv.dev matches 4 run function canon:kevin/dias/second
execute if score #kevcd dv.dev matches ..0 unless score #kprog dv.dev matches 4 unless score #kev dv.dev matches 1.. unless entity @e[type=zombie,tag=dv_kevin] as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s if predicate canon:azar/1en40 run function canon:kevin/arrive
''')
    F('kevin/arrive', '''
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^-7 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^3 ^ ^-4 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/summon
kill @e[type=marker,tag=dv_spot]
execute if score #ok dv.tmp matches 1 as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/greet
scoreboard players set #kevcd dv.dev 300
''')
    pick('kevin/greet_any', [kv_say(t, 100) for t in [
        '¡Eyyy! ¿Qué más, parce? Te estaba buscando.',
        '¡Eyyy! Adivina quién volvió. Exacto: el más bacano.',
        '¡Uy, qué susto! Pensé que eras la Devota. Jajaja.',
        '¡Eyy! Vine porque me aburro. ¿Hacemos algo?',
    ]])
    F('kevin/greet', '''
playsound canon:kevin.hey neutral @a[distance=..24] ~ ~1.6 ~ 1 1
execute if score #kprog dv.dev matches 0 run function canon:kevin/first
execute unless score #kprog dv.dev matches 0 run function canon:kevin/greet_any
''')
    F('kevin/first', kv_say('¡Eyyy! Soy Kevin. Tú no me conoces, pero yo a ti sí. Tengo planes. Muchos planes.', 140) + '\n' +
      'tellraw @a[distance=..20] ' + jt('(Haz clic derecho en Kevin para hablar con él. Te contará chistes y te llevará a sus aventuras.)', 'gray', True) + '\n'
      'scoreboard players set #kprog dv.dev 1')

    F('kevin/tick', '''
tag @s add dv_kme
scoreboard players operation #kme dv.tmp = @s dv.id
scoreboard players set #kdup dv.tmp 0
execute as @e[type=zombie,tag=dv_kevin,tag=!dv_kme] if score @s dv.id < #kme dv.tmp run scoreboard players set #kdup dv.tmp 1
tag @s remove dv_kme
execute if score #kdup dv.tmp matches 0 run function canon:kevin/tick2
execute if score #kdup dv.tmp matches 1 run function canon:rig/despawn
''')
    F('kevin/tick2', f'''
function canon:x/links_follow
scoreboard players remove @s[scores={{dv.say=1..}}] dv.say 1
execute if score @s dv.say matches 0 run function canon:x/bubble_clear
tag @s remove dv_xwalk
scoreboard players remove @s[scores={{dv.timer2=1..}}] dv.timer2 1
execute if score @s dv.timer2 matches 0 run function canon:kevin/pose_reset
tag @a remove dv_wtgt
tag @a[gamemode=!spectator,distance=..64,limit=1,sort=nearest] add dv_wtgt
execute if score @s dv.mode matches 0 run function canon:kevin/m_follow
execute if score @s dv.mode matches 1 if score #m4 dv.clock matches 0 run function canon:x/face
execute if score @s dv.mode matches 2 if score #m4 dv.clock matches 0 run function canon:x/face
tag @a remove dv_wtgt
execute if score @s dv.mode matches 0 unless entity @a[distance=..72] run function canon:kevin/leave
''')
    F('kevin/pose_reset', f'''
scoreboard players set @s dv.timer2 -1
tag @s remove dv_klaugh
tag @s remove dv_koffer
execute unless score @s dv.mode matches 1 run tag @s remove dv_kdance
{head(hd)}
''')
    F('kevin/m_follow', '''
execute if entity @a[tag=dv_wtgt,distance=4..] run function canon:x/walk
execute if entity @a[tag=dv_wtgt,distance=26..] at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-3 run function canon:kevin/catch_up
execute if entity @a[tag=dv_wtgt,distance=..4] if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players remove @s dv.timer 1
execute if score #kprog dv.dev matches 5 run scoreboard players remove @s dv.timer 1
execute if score @s dv.timer matches ..0 if score @s dv.say matches ..0 run function canon:kevin/joke_auto
''')
    F('kevin/catch_up', '''
scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 as @e[type=zombie,tag=dv_kevin,limit=1,sort=nearest] at @e[type=marker,tag=dv_spot,limit=1] run tp @s ~ ~ ~
kill @e[type=marker,tag=dv_spot]
''')
    F('kevin/leave', '''
particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.02 12 normal
scoreboard players set #kevcd dv.dev 900
function canon:rig/despawn
''')
    F('kevin/laugh', f'''
playsound canon:kevin.laugh neutral @a[distance=..20] ~ ~1.6 ~ 1 1
tag @s add dv_klaugh
scoreboard players set @s dv.timer2 40
{head(risa)}
''')
    pick('kevin/joke', [kv_say(j, 140, '@a[distance=..20]') + '\nfunction canon:kevin/laugh' for j in JOKES])
    F('kevin/joke_auto', '''
scoreboard players set @s dv.timer 1200
function canon:kevin/joke
''')
    pick('kevin/how', [kv_say(t, 120) for t in KEVIN_HOW])

    F('kevin/clicked', f'''
execute facing entity @a[tag=dv_talker,limit=1] feet run tp @s ~ ~ ~ ~ 0
playsound canon:kevin.hey neutral @a[distance=..12] ~ ~1.6 ~ 0.6 1.1
execute if score #kev dv.dev matches 1 run function canon:kevin/fiesta/clicked
execute if score #kev dv.dev matches 3 run {'function canon:kevin/cata/clicked'}
execute unless score #kev dv.dev matches 1.. run {menu('@a[tag=dv_talker]', 'KEVIN', '#ffb347', [
        ('Cuéntame un chiste', '/trigger dv.kv set 1'),
        ('¿Qué hacemos hoy?', '/trigger dv.kv set 2'),
        ('¿Cómo estás?', '/trigger dv.kv set 3'),
        ('Baila', '/trigger dv.kv set 4'),
        ('¿Tienes algo para mí?', '/trigger dv.kv set 6'),
        ('Chao', '/trigger dv.kv set 5')])}
''')
    F('kevin/attacked', kv_say('¡Ey, ey, tranquilo! Soy yo, Kevin. El bueno.', 80) + '\nfunction canon:kevin/laugh')

    # elecciones (se ejecuta como jugador)
    F('kevin/choice', '''
tag @s add dv_ktalk
scoreboard players set #kc dv.tmp 0
scoreboard players operation #kc dv.tmp = @s dv.kv
scoreboard players set @s dv.kv 0
scoreboard players set #kfound dv.tmp 0
execute as @e[type=zombie,tag=dv_kevin,distance=..16,limit=1,sort=nearest] run scoreboard players set #kfound dv.tmp 1
execute if score #kc dv.tmp matches 21..22 run function canon:kevin/fiesta/drink_choice
execute if score #kfound dv.tmp matches 0 unless score #kc dv.tmp matches 21..22 run tellraw @s {"text":"Kevin no está cerca.","color":"gray","italic":true}
execute if score #kfound dv.tmp matches 1 unless score #kc dv.tmp matches 21..22 as @e[type=zombie,tag=dv_kevin,distance=..16,limit=1,sort=nearest] at @s run function canon:kevin/c/run
tag @s remove dv_ktalk
''')
    F('kevin/c/run', '''
execute if score #kc dv.tmp matches 1 run function canon:kevin/joke
execute if score #kc dv.tmp matches 2 run function canon:kevin/c/plan
execute if score #kc dv.tmp matches 3 run function canon:kevin/how
execute if score #kc dv.tmp matches 4 run function canon:kevin/c/dance
execute if score #kc dv.tmp matches 5 run function canon:kevin/c/bye
execute if score #kc dv.tmp matches 6 run function canon:kevin/c/gift
execute if score #kc dv.tmp matches 11 run function canon:kevin/fiesta/try
execute if score #kc dv.tmp matches 12 run function canon:kevin/bosque/try
execute if score #kc dv.tmp matches 13 run function canon:kevin/cata/try
''')
    plan_menu = lambda sel, title, b: menu(sel, title, '#ffb347', b)
    F('kevin/c/plan', f'''
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/busy
execute unless score #kev dv.dev matches 1.. if score #kprog dv.dev matches 1 run function canon:kevin/c/plan1
execute unless score #kev dv.dev matches 1.. if score #kprog dv.dev matches 2 run function canon:kevin/c/plan2
execute unless score #kev dv.dev matches 1.. if score #kprog dv.dev matches 3 run function canon:kevin/c/plan3
execute unless score #kev dv.dev matches 1.. if score #kprog dv.dev matches 5.. run function canon:kevin/c/plan5
''')
    F('kevin/c/plan1', kv_say('Esta noche hay una fiesta techno. La mejor del mundo. Bueno, la única. ¿Vienes?', 140) + '\n' +
      plan_menu('@a[tag=dv_ktalk]', 'FIESTA TECHNO (de noche)', [('¡Vamos!', '/trigger dv.kv set 11'), ('Ahora no', '/trigger dv.kv set 5')]))
    F('kevin/c/plan2', kv_say('Quiero grabar un video en el bosque. Dicen que ahí vive un man altísimo, sin cara. Ideal para mi canal.', 160) + '\n' +
      plan_menu('@a[tag=dv_ktalk]', 'EL BOSQUE (de noche, en un bosque)', [('Vamos', '/trigger dv.kv set 12'), ('Ni loco', '/trigger dv.kv set 5')]))
    F('kevin/c/plan3', kv_say('Encontré una entrada a unas catacumbas. Huele a muerto. ¿Bajamos?', 140) + '\n' +
      plan_menu('@a[tag=dv_ktalk]', 'LAS CATACUMBAS', [('Bajemos', '/trigger dv.kv set 13'), ('Otro día', '/trigger dv.kv set 5')]))
    F('kevin/c/plan5', kv_say('Ya hicimos de todo... pero yo me lo gozo otra vez. Escoge.', 120) + '\n' +
      plan_menu('@a[tag=dv_ktalk]', 'OTRA VEZ', [('Fiesta', '/trigger dv.kv set 11'), ('Bosque', '/trigger dv.kv set 12'),
                                              ('Catacumbas', '/trigger dv.kv set 13'), ('Nada', '/trigger dv.kv set 5')]))
    F('kevin/c/dance', kv_say('¡Mírame! Paso prohibido número 7.', 100) + '''
tag @s add dv_kdance
scoreboard players set @s dv.timer2 120
function canon:kevin/laugh
scoreboard players set @s dv.timer2 120
''')
    F('kevin/c/bye', kv_say('¡Hágale pues! Nos vemos. Si ves a Mariana, no le digas que me viste.', 60) + '''
scoreboard players set #kevcd dv.dev 1200
scoreboard players set @s dv.mode 9
schedule function canon:kevin/bye_later 60t replace
''')
    F('kevin/bye_later', 'execute as @e[type=zombie,tag=dv_kevin,scores={dv.mode=9}] at @s run function canon:kevin/leave')
    F('kevin/c/gift', '''
execute if entity @a[tag=dv_ktalk,scores={dv.kpcd=1..}] run function canon:kevin/c/gift_no
execute unless entity @a[tag=dv_ktalk,scores={dv.kpcd=1..}] run function canon:kevin/c/gift_yes
''')
    F('kevin/c/gift_no', kv_say('Ya te di algo hoy. No soy un banco, parce.', 80))
    pick('kevin/c/gift_yes', [
        kv_say('Toma, pizza fría. Lo mejor que existe.', 90) + '\nloot give @a[tag=dv_ktalk] loot canon:items/pizza',
        kv_say('Unas balas que encontré por ahí. No preguntes.', 90) + '\nloot give @a[tag=dv_ktalk] loot canon:items/balas',
        kv_say('Una linterna. La vas a necesitar más que yo.', 90) + '\nloot give @a[tag=dv_ktalk] loot canon:items/linterna',
        kv_say('Unos billetes. Los gané en una apuesta con un vagabundo.', 90) + '\nloot give @a[tag=dv_ktalk] loot canon:items/billete',
        kv_say('Una lata de sopa. Romántico, ¿no?', 90) + '\nloot give @a[tag=dv_ktalk] loot canon:items/sopa',
    ])
    A('kevin/c/gift_yes', 'scoreboard players set @a[tag=dv_ktalk] dv.kpcd 1200')

    # ---- eventos: dispatcher
    F('kevin/ev/tick', '''
scoreboard players add #kt dv.dev 1
execute if score #kev dv.dev matches 1 run function canon:kevin/fiesta/tick
execute if score #kev dv.dev matches 2 run function canon:kevin/bosque/tick
execute if score #kev dv.dev matches 3 run function canon:kevin/cata/tick
''')
    F('kevin/ev/abort', '''
execute if score #kev dv.dev matches 1 run function canon:kevin/fiesta/cleanup
execute if score #kev dv.dev matches 2 run function canon:kevin/bosque/cleanup
execute if score #kev dv.dev matches 3 run function canon:kevin/cata/cleanup
scoreboard players set #kev dv.dev 0
tag @a remove dv_kpart
''')
    F('kevin/ev/busy', kv_say('Espera, que ya estamos en algo.', 60))



def gen_fiesta():
    K = CMD
    hd, risa, droga = K['kevin_cabeza_neutral'], K['kevin_cabeza_risa'], K['kevin_cabeza_drogado']
    F('kevin/fiesta/try', f'''
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/busy
execute unless score #kev dv.dev matches 1.. if entity @a[tag=dv_ktalk,predicate=canon:de_dia] run function canon:kevin/fiesta/day_no
execute unless score #kev dv.dev matches 1.. if entity @a[tag=dv_ktalk,predicate=canon:de_noche] run function canon:kevin/fiesta/start
''')
    F('kevin/fiesta/day_no', kv_say('La fiesta es de noche, parce. Vuelve a hablarme cuando oscurezca.', 100))
    F('kevin/fiesta/start', '''
scoreboard players set #kev dv.dev 1
scoreboard players set #kt dv.dev 0
scoreboard players set #kdrunk dv.dev 0
tag @a[gamemode=!spectator,distance=..32] add dv_kpart
kill @e[type=marker,tag=dv_fiesta_c]
summon minecraft:marker ~ ~ ~ {Tags:["dv_fiesta_c"]}
scoreboard players set @s dv.mode 1
tag @s add dv_kdance
execute positioned ~3 ~ ~ run function canon:kevin/fiesta/dancer_0
execute positioned ~-3 ~ ~1 run function canon:kevin/fiesta/dancer_1
execute positioned ~1 ~ ~3 run function canon:kevin/fiesta/dancer_2
execute positioned ~-1 ~ ~-3 run function canon:kevin/fiesta/dancer_0
execute positioned ~3 ~ ~-3 run function canon:kevin/fiesta/dancer_1
execute positioned ~-3 ~ ~3 run function canon:kevin/fiesta/dancer_2
execute positioned ~ ~6 ~ run summon minecraft:block_display ~-2 ~ ~ {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:magenta_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~6 ~ run summon minecraft:block_display ~2 ~ ~ {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:cyan_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~6 ~ run summon minecraft:block_display ~ ~ ~2 {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:lime_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ ~6 ~ run summon minecraft:block_display ~ ~ ~-2 {Tags:["dv_flight"],brightness:{sky:15,block:15},block_state:{Name:"minecraft:yellow_stained_glass"},transformation:{translation:[-0.5f,-0.5f,-0.5f],left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}
playsound canon:kevin.techno record @a[tag=dv_kpart] ~ ~ ~ 1 1
title @a[tag=dv_kpart] times 10 50 20
title @a[tag=dv_kpart] subtitle {"text":"La mejor fiesta del mundo. La única.","color":"#ffd27a","italic":true}
title @a[tag=dv_kpart] title {"text":"FIESTA TECHNO","color":"#ff5ad1","bold":true}
''' + kv_say('¡EYYY! ¡Bienvenidos a la mejor fiesta del mundo! ¡A bailar!', 120))
    for i in range(3):
        F(f'kevin/fiesta/dancer_{i}', '''
scoreboard players set #ok dv.tmp 0
function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/fiesta/dancer_summon_%d
kill @e[type=marker,tag=dv_spot]
''' % i)
        F(f'kevin/fiesta/dancer_summon_{i}', rig_summon(['dv_fiestero'], 'Fiestero', '#c06ad6', head=False) + '\n'
          f'execute as @e[type=zombie,tag=dv_new,tag=dv_fiestero,distance=..2,limit=1,sort=nearest] at @s run function canon:kevin/fiesta/dancer_init_{i}')
        F(f'kevin/fiesta/dancer_init_{i}', f'''
function canon:rig/init_common
{set_cmd('body', K[f'fiestero_{i}_dance_a'])}
scoreboard players set @s dv.anim {i * 3}
execute facing entity @e[type=marker,tag=dv_fiesta_c,limit=1] feet run tp @s ~ ~ ~ ~ 0
''')
    F('kevin/fiesta/dancer_tick', '''
execute unless score #kev dv.dev matches 1 run function canon:rig/despawn
tag @a remove dv_wtgt
execute if entity @s[tag=dv_fstare] run tag @a[tag=dv_kpart,distance=..32,limit=1,sort=nearest] add dv_wtgt
execute if entity @s[tag=dv_fstare] run function canon:x/face
tag @a remove dv_wtgt
''')
    F('kevin/fiesta/tick', '''
execute unless entity @e[type=marker,tag=dv_fiesta_c] run function canon:kevin/fiesta/cleanup
execute unless entity @a[tag=dv_kpart] run function canon:kevin/fiesta/cleanup
execute as @a[tag=dv_kpart] at @s unless entity @e[type=marker,tag=dv_fiesta_c,distance=..48] run tag @s remove dv_kpart
execute if score #kt dv.dev matches ..899 if score #m4 dv.clock matches 0 at @e[type=marker,tag=dv_fiesta_c] run function canon:kevin/fiesta/lights
execute if score #kt dv.dev matches ..899 if score #m20 dv.clock matches 0 run function canon:kevin/fiesta/spin
execute if score #kt dv.dev matches 400 run function canon:kevin/fiesta/offer
execute if score #kt dv.dev matches 520 as @e[type=zombie,tag=dv_kevin] run tag @s remove dv_koffer
execute as @a[tag=dv_kpart,tag=dv_kdrug] at @s if score #m40 dv.clock matches 0 run function canon:kevin/fiesta/trip
execute if score #kt dv.dev matches 900 run function canon:kevin/fiesta/wrong
execute if score #kt dv.dev matches 960 at @e[type=marker,tag=dv_fiesta_c] run function canon:kevin/fiesta/miron
execute if score #kt dv.dev matches 1040 run function canon:kevin/fiesta/scream
execute if score #kt dv.dev matches 1080 run function canon:kevin/fiesta/end
''')
    F('kevin/fiesta/lights', '''
scoreboard players operation #c dv.tmp = #kt dv.dev
scoreboard players operation #c dv.tmp %= #3 dv.math
execute if score #c dv.tmp matches 0 run particle minecraft:dust 1 0.2 0.8 1.6 ~ ~2.5 ~ 4 1.5 4 0 25 force @a[tag=dv_kpart]
execute if score #c dv.tmp matches 1 run particle minecraft:dust 0.2 0.9 1 1.6 ~ ~2.5 ~ 4 1.5 4 0 25 force @a[tag=dv_kpart]
execute if score #c dv.tmp matches 2 run particle minecraft:dust 0.6 1 0.2 1.6 ~ ~2.5 ~ 4 1.5 4 0 25 force @a[tag=dv_kpart]
particle minecraft:end_rod ~ ~6 ~ 2 0.2 2 0.05 3 force @a[tag=dv_kpart]
''')
    F('kevin/fiesta/spin', '''
scoreboard players operation #c dv.tmp = #kt dv.dev
scoreboard players operation #c dv.tmp %= #40 dv.math
execute if score #c dv.tmp matches 0..19 as @e[type=block_display,tag=dv_flight] run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{left_rotation:[0f,0.7071f,0f,0.7071f],scale:[1.3f,1.3f,1.3f]}}
execute if score #c dv.tmp matches 20..39 as @e[type=block_display,tag=dv_flight] run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{left_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
''')
    F('kevin/fiesta/offer', f'''
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/fiesta/offer2
''')
    F('kevin/fiesta/offer2', kv_say('Toma, prueba esto. Te va a encantar. Confía en mí.', 120, '@a[tag=dv_kpart]') + '''
tag @s add dv_koffer
''' + menu('@a[tag=dv_kpart]', 'Kevin te ofrece un vaso con algo brillante...', '#ff5ad1',
           [('Tomar', '/trigger dv.kv set 21'), ('No, gracias', '/trigger dv.kv set 22')]))
    F('kevin/fiesta/clicked', '''
execute if score #kt dv.dev matches ..399 run function canon:kevin/fiesta/talk
execute if score #kt dv.dev matches 400..899 run function canon:kevin/fiesta/offer2
''')
    pick('kevin/fiesta/talk', [kv_say(t, 80, '@a[tag=dv_kpart]') for t in [
        '¡Súbele, súbele! Ah no, no hay volumen. Es mi cabeza.',
        'Este DJ es mi primo. Bueno, no tengo primos. Pero ojalá.',
        '¡Baila conmigo! Nadie nos está mirando. Creo.',
    ]])
    F('kevin/fiesta/drink_choice', '''
execute unless score #kev dv.dev matches 1 run tellraw @s {"text":"Ya no hay nada que tomar.","color":"gray","italic":true}
execute if score #kev dv.dev matches 1 if score #kc dv.tmp matches 21 unless entity @s[tag=dv_kdrug] run function canon:kevin/fiesta/drink
execute if score #kev dv.dev matches 1 if score #kc dv.tmp matches 22 run function canon:kevin/fiesta/refuse
''')
    F('kevin/fiesta/drink', '''
tag @s add dv_kdrug
scoreboard players set #kdrunk dv.dev 1
effect give @s minecraft:nausea 40 0 true
effect give @s minecraft:speed 30 1 true
playsound canon:kevin.drugged music @s ~ ~ ~ 1 1
tellraw @s {"text":"Sabe a chicle y a pilas. Las luces empiezan a respirar.","color":"#ff5ad1","italic":true}
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/laugh
''')
    F('kevin/fiesta/refuse', '''
tellraw @s [{"text":"Kevin: ","color":"#ffb347"},{"text":"Bueno, más para mí. Jajaja.","color":"white","italic":true}]
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/laugh
''')
    F('kevin/fiesta/trip', '''
effect give @s minecraft:darkness 2 0 true
particle minecraft:dust 1 0 1 1 ^ ^1.5 ^2 1 1 1 0 10 normal @s
execute if predicate canon:azar/1en3 run playsound canon:devota.whisper ambient @s ^2 ^ ^-2 0.5 0.6
''')
    F('kevin/fiesta/wrong', f'''
stopsound @a[tag=dv_kpart] record canon:kevin.techno
playsound canon:fx.heartbeat ambient @a[tag=dv_kpart] ~ ~ ~ 1 1
tag @e[type=zombie,tag=dv_fiestero] add dv_fstare
execute as @e[type=block_display,tag=dv_flight] run data merge entity @s {{block_state:{{Name:"minecraft:red_stained_glass"}}}}
execute as @e[type=zombie,tag=dv_kevin,limit=1] run tag @s remove dv_kdance
execute as @e[type=zombie,tag=dv_kevin,limit=1] run {head(droga).splitlines()[0]}
execute as @e[type=zombie,tag=dv_kevin,limit=1] run {head(droga).splitlines()[1]}
tellraw @a[tag=dv_kpart] {{"text":"La música se corta. Todos dejan de bailar. Todos te miran.","color":"#c94a4a","italic":true}}
''')
    F('kevin/fiesta/miron', '''
execute positioned ~2 ~ ~2 run function canon:miron/spawn_here
execute as @e[type=zombie,tag=dv_miron,distance=..8] run scoreboard players set @s dv.timer2 1
playsound canon:miron.aparece hostile @a[tag=dv_kpart] ~ ~ ~ 1 0.9
''')
    F('kevin/fiesta/scream', '''
playsound canon:miron.grito master @a[tag=dv_kpart] ~ ~ ~ 1 1
execute as @a[tag=dv_kpart] at @s run function canon:x/jumpscare
execute as @a[tag=dv_kpart] at @s run function canon:x/blackout
''')
    F('kevin/fiesta/end', f'''
execute if score #kprog dv.dev matches ..1 run scoreboard players set #kprog dv.dev 2
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/fiesta/end_kevin
function canon:kevin/fiesta/cleanup
''')
    F('kevin/fiesta/end_kevin', f'''
scoreboard players set @s dv.mode 0
tag @s remove dv_kdance
execute if score #kdrunk dv.dev matches 1 run function canon:kevin/fiesta/end_drunk
execute if score #kdrunk dv.dev matches 0 run function canon:kevin/fiesta/end_sober
function canon:kevin/laugh
tellraw @a[distance=..40] {jt('(Kevin tiene otra idea. Háblale: ¿Qué hacemos hoy?)', 'gray', True)}
''')
    F('kevin/fiesta/end_drunk', kv_say('Jajaja, ¿qué te pasó? Te quedaste dormido parado. Te dije que te iba a encantar.', 160, '@a[distance=..40]'))
    F('kevin/fiesta/end_sober', kv_say('Bro... ¿viste eso? ¿Quién era ese man flaco? Mejor no volvamos a esa fiesta. O sí. Jajaja.', 160, '@a[distance=..40]'))
    F('kevin/fiesta/cleanup', '''
stopsound @a[tag=dv_kpart] record canon:kevin.techno
stopsound @a[tag=dv_kdrug] music canon:kevin.drugged
execute as @e[type=zombie,tag=dv_fiestero] at @s run function canon:rig/despawn
kill @e[type=block_display,tag=dv_flight]
kill @e[type=marker,tag=dv_fiesta_c]
execute as @e[type=zombie,tag=dv_miron] at @s run function canon:rig/despawn
execute as @e[type=zombie,tag=dv_kevin] run scoreboard players set @s dv.mode 0
execute as @e[type=zombie,tag=dv_kevin] run tag @s remove dv_kdance
tag @a remove dv_kdrug
tag @a remove dv_kpart
scoreboard players set #kev dv.dev 0
''')


NOTAS = ['SIEMPRE MIRA', 'NO CORRAS', 'DETRÁS DE TI', 'KEVIN NO ESTÁ SOLO', 'NO TIENE CARA', 'YA TE VIO']



NOTAS = ['SIEMPRE MIRA', 'NO CORRAS', 'DETRÁS DE TI', 'KEVIN NO ESTÁ SOLO', 'NO TIENE CARA', 'YA TE VIO']


def gen_bosque():
    F('kevin/bosque/try', f'''
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/busy
scoreboard players set #bok dv.tmp 0
execute if entity @a[tag=dv_ktalk,predicate=canon:de_noche,predicate=canon:en_bosque] run scoreboard players set #bok dv.tmp 1
execute unless score #kev dv.dev matches 1.. if score #bok dv.tmp matches 0 run function canon:kevin/bosque/no
execute unless score #kev dv.dev matches 1.. if score #bok dv.tmp matches 1 at @a[tag=dv_ktalk,limit=1] run function canon:kevin/bosque/start
''')
    F('kevin/bosque/no', kv_say('Tiene que ser de noche y en un bosque de verdad, con árboles. Llévame a uno y me hablas.', 120))
    notes = []
    offs = [(22, 0), (-20, 10), (6, 28), (-8, -26), (26, -18), (-28, -12)]
    for i, (x, z) in enumerate(offs):
        notes.append(f'execute positioned ~{x} ~ ~{z} positioned over motion_blocking_no_leaves run function canon:kevin/bosque/nota_spawn')
    F('kevin/bosque/start', '''
scoreboard players set #kev dv.dev 2
scoreboard players set #kt dv.dev 0
scoreboard players set #knotes dv.dev 0
tag @a[gamemode=!spectator,distance=..32] add dv_kpart
kill @e[type=marker,tag=dv_bosque_c]
summon minecraft:marker ~ ~ ~ {Tags:["dv_bosque_c"]}
''' + '\n'.join(notes) + '''
execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:kevin/bosque/kevin_runs
playsound canon:music.bosque music @a[tag=dv_kpart] ~ ~ ~ 1 1
title @a[tag=dv_kpart] times 10 60 20
title @a[tag=dv_kpart] subtitle {"text":"Encuentra las 6 notas. No lo mires mucho tiempo.","color":"gray","italic":true}
title @a[tag=dv_kpart] title {"text":"EL BOSQUE","color":"#d8d8d8"}
''')
    F('kevin/bosque/kevin_runs', kv_say('¡Yo grabo desde allá! ¡Busquen las 6 notas del Alto antes de que los encuentre! Jajaja...', 120, '@a[tag=dv_kpart]') + '''
particle minecraft:poof ~ ~1 ~ 0.3 0.6 0.3 0.02 12 normal
function canon:rig/despawn
''')
    F('kevin/bosque/nota_spawn', '''
summon minecraft:item_display ~ ~0.6 ~ {Tags:["dv_nota_vis","dv_bnew"],brightness:{sky:15,block:15},billboard:"vertical",view_range:0.5f,item:{id:"minecraft:paper",Count:1b},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:interaction ~ ~0.1 ~ {Tags:["dv_nota","dv_click","dv_npc_click","dv_bnew"],width:1.0f,height:1.2f,response:1b}
scoreboard players operation @e[tag=dv_bnew] dv.id = #next dv.id
scoreboard players add #next dv.id 1
tag @e[tag=dv_bnew] remove dv_bnew
''')
    F('kevin/bosque/tick', '''
execute unless entity @a[tag=dv_kpart] run function canon:kevin/bosque/fail
execute as @a[tag=dv_kpart] at @s unless entity @e[type=marker,tag=dv_bosque_c,distance=..120] run tag @s remove dv_kpart
execute if score #m40 dv.clock matches 0 as @e[type=item_display,tag=dv_nota_vis] at @s run particle minecraft:end_rod ~ ~0.4 ~ 0.15 0.3 0.15 0.01 2 normal
execute if score #kt dv.dev matches 100 at @a[tag=dv_kpart,limit=1,sort=random] positioned ^ ^ ^-30 positioned over motion_blocking_no_leaves run function canon:alto/spawn
execute if score #kt dv.dev matches 1920 run playsound canon:music.bosque music @a[tag=dv_kpart] ~ ~ ~ 1 1
execute if score #kt dv.dev matches 3840 run playsound canon:music.bosque music @a[tag=dv_kpart] ~ ~ ~ 1 1
execute as @a[tag=dv_kpart] at @s if predicate canon:azar/1en100 run function canon:kevin/bosque/ambient
execute if score #kt dv.dev matches 6000.. run function canon:kevin/bosque/fail
''')
    pick('kevin/bosque/ambient', [
        'playsound canon:bosque.rama ambient @s ^ ^ ^-6 1 1',
        'playsound canon:bosque.pasos ambient @s ^3 ^ ^-5 1 1',
        'playsound canon:bosque.buho ambient @s ^-10 ^4 ^6 0.8 1',
        'playsound canon:bosque.viento ambient @s ~ ~ ~ 0.5 1',
        'playsound canon:alto.silbido ambient @s ^ ^ ^-25 0.6 1',
    ])
    F('kevin/bosque/nota_taken', '''
scoreboard players operation #id dv.tmp = @s dv.id
execute as @e[type=item_display,tag=dv_nota_vis] if score @s dv.id = #id dv.tmp run kill @s
scoreboard players add #knotes dv.dev 1
playsound canon:fx.sub_hit master @a[tag=dv_kpart] ~ ~ ~ 0.8 1
playsound canon:miron.estatica ambient @a[tag=dv_talker] ~ ~ ~ 1 1
function canon:kevin/bosque/nota_text
title @a[tag=dv_kpart] actionbar [{"text":"Notas: ","color":"gray"},{"score":{"name":"#knotes","objective":"dv.dev"},"color":"white"},{"text":"/6","color":"gray"}]
execute if score #knotes dv.dev matches 6.. run function canon:kevin/bosque/win
kill @s
''')
    pick('kevin/bosque/nota_text', ['tellraw @a[tag=dv_kpart] ' + jt('La nota dice: «' + t + '»', '#d8d8d8', True) for t in NOTAS])
    F('kevin/bosque/win', '''
execute as @e[type=zombie,tag=dv_alto] at @s run function canon:alto/vanish
stopsound @a[tag=dv_kpart] music canon:music.bosque
effect clear @a[tag=dv_kpart] minecraft:darkness
execute at @a[tag=dv_talker,limit=1] run function canon:kevin/arrive_here
execute if score #kprog dv.dev matches ..2 run scoreboard players set #kprog dv.dev 3
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/bosque/win_kevin
function canon:kevin/bosque/cleanup
''')
    F('kevin/bosque/win_kevin', chat('Kevin', '#ffb347', '¡LO GRABÉ TODO! ... ay no. La cámara solo grabó estática. Jajaja. Bueno, tengo otra idea.', '@a[distance=..40]') + '\nfunction canon:kevin/laugh')
    F('kevin/arrive_here', '''
scoreboard players set #ok dv.tmp 0
execute unless entity @e[type=zombie,tag=dv_kevin] positioned ^ ^ ^3 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/summon
kill @e[type=marker,tag=dv_spot]
''')
    F('kevin/bosque/fail', '''
execute as @e[type=zombie,tag=dv_alto] at @s run function canon:alto/vanish
stopsound @a music canon:music.bosque
execute at @e[type=marker,tag=dv_bosque_c,limit=1] at @a[distance=..140,limit=1,sort=nearest] run function canon:kevin/arrive_here
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/bosque/fail_kevin
function canon:kevin/bosque/cleanup
''')
    F('kevin/bosque/fail_kevin', chat('Kevin', '#ffb347', 'Bro... ¿estás bien? Estabas gritando. Mejor lo intentamos otra noche.', '@a[distance=..60]'))
    F('kevin/bosque/cleanup', '''
kill @e[type=item_display,tag=dv_nota_vis]
kill @e[type=interaction,tag=dv_nota]
kill @e[type=marker,tag=dv_bosque_c]
execute as @e[type=zombie,tag=dv_alto] at @s run function canon:rig/despawn
tag @a remove dv_kpart
scoreboard players set #kev dv.dev 0
''')

    # ---- el Alto
    F('alto/spawn', rig_summon(['dv_alto'], 'El Alto', '#d8d8d8', head=False, scale=1.6) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_alto,distance=..2,limit=1,sort=nearest] at @s run function canon:alto/init')
    F('alto/init', f'''
function canon:rig/init_common
{set_cmd('body', CMD['alto_idle'])}
scoreboard players set @s dv.watch 0
playsound canon:alto.aparece hostile @a[tag=dv_kpart] ~ ~ ~ 0.6 0.8
''')
    F('alto/tick', '''
tag @s remove dv_xwalk
tag @a remove dv_wtgt
tag @a remove dv_lookers
tag @a[tag=dv_kpart,distance=..160,limit=1,sort=nearest] add dv_wtgt
tag @a[tag=dv_kpart] add dv_lookers
execute unless entity @a[tag=dv_wtgt] run function canon:alto/vanish
execute if entity @a[tag=dv_wtgt] run function canon:alto/think
tag @a remove dv_wtgt
tag @a remove dv_lookers
''')
    F('alto/think', '''
function canon:x/seen
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players add @s dv.timer 1
execute if score #seen dv.tmp matches 1 run scoreboard players add @s dv.watch 1
execute if score #seen dv.tmp matches 0 if score @s dv.watch matches 1.. run scoreboard players remove @s dv.watch 1
execute if score #seen dv.tmp matches 1 if score #m20 dv.clock matches 0 run function canon:alto/stare_fx
execute if score #seen dv.tmp matches 0 if entity @a[tag=dv_wtgt,distance=3..] run function canon:x/creep
scoreboard players set #aint dv.tmp 160
scoreboard players operation #an dv.tmp = #knotes dv.dev
scoreboard players operation #an dv.tmp *= #20 dv.math
scoreboard players operation #aint dv.tmp -= #an dv.tmp
execute if score #seen dv.tmp matches 0 if score @s dv.timer >= #aint dv.tmp run function canon:alto/blink
execute if score @s dv.watch matches 80.. run function canon:alto/lunge
tag @s remove dv_areach
execute if entity @a[tag=dv_wtgt,distance=..4] run tag @s add dv_areach
execute if entity @a[tag=dv_wtgt,distance=..1.8] run function canon:alto/catch
''')
    F('alto/stare_fx', '''
effect give @a[tag=dv_lookers,distance=..48] minecraft:darkness 2 0 true
playsound canon:miron.estatica ambient @a[tag=dv_lookers,distance=..48] ~ ~ ~ 0.7 0.8
''')
    F('alto/blink', '''
scoreboard players set @s dv.timer 0
scoreboard players set #ad dv.tmp 18
scoreboard players operation #an dv.tmp = #knotes dv.dev
scoreboard players operation #an dv.tmp *= #2 dv.math
scoreboard players operation #ad dv.tmp -= #an dv.tmp
execute if score #ad dv.tmp matches ..8 at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-8 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
execute if score #ad dv.tmp matches 9..12 at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-12 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
execute if score #ad dv.tmp matches 13.. at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^-18 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
execute at @s run playsound canon:alto.pasos hostile @a[tag=dv_wtgt] ~ ~ ~ 0.9 0.8
''')
    F('alto/lunge', '''
scoreboard players set @s dv.watch 0
execute at @a[tag=dv_wtgt,limit=1] positioned ^ ^ ^2 run tp @s ~ ~ ~
playsound canon:alto.golpe hostile @a[tag=dv_wtgt] ~ ~ ~ 1 0.7
''')
    F('alto/catch', '''
playsound canon:alto.aparece master @a[tag=dv_wtgt] ~ ~ ~ 1 1
execute as @a[tag=dv_wtgt] at @s run function canon:x/jumpscare
damage @a[tag=dv_wtgt,limit=1] 10 minecraft:mob_attack by @s
effect give @a[tag=dv_wtgt] minecraft:blindness 3 0 true
tellraw @a[tag=dv_wtgt] {"text":"No tenía cara. Pero sonreía.","color":"#d8d8d8","italic":true}
tag @a[tag=dv_wtgt] remove dv_kpart
scoreboard players set @s dv.timer 0
execute at @a[tag=dv_kpart,limit=1,sort=random] positioned ^ ^ ^-24 positioned over motion_blocking_no_leaves run tp @s ~ ~ ~
''')
    F('alto/vanish', '''
particle minecraft:large_smoke ~ ~1.5 ~ 0.3 1.2 0.3 0.02 30 normal
playsound canon:miron.estatica hostile @a[distance=..32] ~ ~ ~ 1 0.6
function canon:rig/despawn
''')



def gen_cata():
    # ------- laberinto (fijo) en el overworld profundo, lejos de todo
    X0, Z0, Y0 = 20000, 20000, -50
    N = 8
    C = 5  # celda: 3 de pasillo + 2 de muro
    W = N * C + 2
    rng = random.Random(7)
    vis = [[False] * N for _ in range(N)]
    walls = set()
    for i in range(N):
        for j in range(N):
            for d in ((1, 0), (0, 1)):
                walls.add(((i, j), (i + d[0], j + d[1])))
    stack = [(0, 0)]
    vis[0][0] = True
    order = {(0, 0): 0}
    while stack:
        i, j = stack[-1]
        nb = [(i + a, j + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= i + a < N and 0 <= j + b < N and not vis[i + a][j + b]]
        if not nb:
            stack.pop()
            continue
        n = rng.choice(nb)
        vis[n[0]][n[1]] = True
        order[n] = len(stack)
        a, b = sorted([(i, j), n])
        walls.discard((a, b))
        stack.append(n)
    # celda de la llave: la más profunda que no sea la salida
    exitc = (N - 1, N - 1)
    keyc = max((c for c in order if c != exitc and c != (0, 0)), key=lambda c: order[c])

    def cell_origin(c):
        return X0 + 2 + c[0] * C, Z0 + 2 + c[1] * C

    cmds = []
    y1, y2 = Y0, Y0 + 7
    cmds.append(f'fill {X0} {y1} {Z0} {X0 + W + 8} {y2} {Z0 + W} minecraft:deepslate_bricks')
    for i in range(N):
        for j in range(N):
            x, z = cell_origin((i, j))
            cmds.append(f'fill {x} {Y0 + 1} {z} {x + 2} {Y0 + 4} {z + 2} minecraft:air')
            if ((i, j), (i + 1, j)) not in walls and i + 1 < N:
                cmds.append(f'fill {x + 3} {Y0 + 1} {z} {x + 4} {Y0 + 4} {z + 2} minecraft:air')
            if ((i, j), (i, j + 1)) not in walls and j + 1 < N:
                cmds.append(f'fill {x} {Y0 + 1} {z + 3} {x + 2} {Y0 + 4} {z + 4} minecraft:air')
    # suelo y techo variados
    cmds.append(f'fill {X0} {Y0} {Z0} {X0 + W} {Y0} {Z0 + W} minecraft:deepslate_tiles')
    cmds.append(f'fill {X0} {Y0 + 5} {Z0} {X0 + W} {Y0 + 5} {Z0 + W} minecraft:cracked_deepslate_tiles')
    deco = []
    for i in range(N):
        for j in range(N):
            x, z = cell_origin((i, j))
            r = rng.random()
            if r < 0.18:
                deco.append(f'setblock {x + rng.randint(0, 2)} {Y0 + 1} {z + rng.randint(0, 2)} minecraft:skeleton_skull[rotation={rng.randint(0, 15)}]')
            elif r < 0.30:
                deco.append(f'setblock {x + rng.choice([0, 2])} {Y0 + 4} {z + rng.choice([0, 2])} minecraft:cobweb')
            elif r < 0.40:
                deco.append(f'setblock {x + 1} {Y0 + 4} {z + 1} minecraft:soul_lantern[hanging=true]')
            elif r < 0.48:
                deco.append(f'setblock {x + rng.choice([0, 2])} {Y0 + 1} {z + rng.choice([0, 2])} minecraft:bone_block')
            elif r < 0.56:
                deco.append(f'setblock {x + rng.randint(0, 2)} {Y0 + 1} {z + rng.randint(0, 2)} minecraft:candle[candles=3,lit=true]')
            for _ in range(2):
                xx, yy, zz = x + rng.choice([-1, 3]), Y0 + rng.randint(1, 4), z + rng.randint(0, 2)
                deco.append(f'fill {xx} {yy} {zz} {xx} {yy} {zz} minecraft:cracked_deepslate_bricks replace minecraft:deepslate_bricks')
    sx, sz = cell_origin((0, 0))
    ex, ez = cell_origin(exitc)
    kx, kz = cell_origin(keyc)
    # salida: pasillo extra al este de la celda final, con reja
    cmds2 = [
        f'fill {ex + 3} {Y0 + 1} {ez} {ex + 6} {Y0 + 4} {ez + 2} minecraft:air',
        f'fill {ex + 3} {Y0 + 1} {ez} {ex + 3} {Y0 + 3} {ez + 2} minecraft:iron_bars',
        f'setblock {ex + 6} {Y0 + 2} {ez + 1} minecraft:soul_lantern',
        f'setblock {sx + 1} {Y0 + 4} {sz + 1} minecraft:soul_lantern[hanging=true]',
    ]
    F('kevin/cata/build_place', '\n'.join(cmds + deco + cmds2) + '\nscoreboard players set #cata_built dv.build 2\n'
      f'forceload remove {X0} {Z0} {X0 + W + 8} {Z0 + W}')
    F('kevin/cata/build_try', f'execute in minecraft:overworld if loaded {X0} {Y0} {Z0} if loaded {X0 + W + 8} {Y0} {Z0 + W} if loaded {X0} {Y0} {Z0 + W} if loaded {X0 + W + 8} {Y0} {Z0} in minecraft:overworld run function canon:kevin/cata/build_place')
    F('kevin/cata/build_start', f'''
scoreboard players set #cata_built dv.build 1
execute in minecraft:overworld run forceload add {X0} {Z0} {X0 + W + 8} {Z0 + W}
''')
    sel_in = f'x={X0 - 2},y={Y0 - 2},z={Z0 - 2},dx={W + 12},dy=12,dz={W + 4}'
    F('kevin/cata/try', f'''
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/busy
execute unless score #kev dv.dev matches 1.. run function canon:kevin/cata/prep
''')
    F('kevin/cata/prep', f'''
scoreboard players set #kev dv.dev 3
scoreboard players set #kt dv.dev -100000
scoreboard players set #ckey dv.dev 0
tag @a[gamemode=!spectator,distance=..32] add dv_kpart
execute if score #cata_built dv.build matches 0 run function canon:kevin/cata/build_start
{kv_say('Síganme. Y no toquen los huesos. Bueno, tóquenlos si quieren, pero después no lloren.', 120, '@a[tag=dv_kpart]')}
tellraw @a[tag=dv_kpart] {jt('(Bajando a las catacumbas...)', 'gray', True)}
schedule function canon:kevin/cata/enter_wait 40t replace
''')
    F('kevin/cata/enter_wait', '''
execute if score #cata_built dv.build matches 2 run function canon:kevin/cata/enter
execute unless score #cata_built dv.build matches 2 if score #kev dv.dev matches 3 run schedule function canon:kevin/cata/enter_wait 20t replace
''')
    F('kevin/cata/enter', f'''
scoreboard players set #kt dv.dev 0
execute as @a[tag=dv_kpart] at @s run function canon:travel/store_return
execute as @a[tag=dv_kpart] in minecraft:overworld run tp @s {sx + 1}.5 {Y0 + 1} {sz + 1}.5 -90 0
execute as @a[tag=dv_kpart] run effect give @s minecraft:darkness 3 0 true
execute as @e[type=zombie,tag=dv_kevin] in minecraft:overworld run tp @s {sx + 1}.5 {Y0 + 1} {sz + 0}.5
playsound canon:cata.reja master @a[tag=dv_kpart] ~ ~ ~ 1 0.8
playsound canon:cata.ambient ambient @a[tag=dv_kpart] ~ ~ ~ 1 1
title @a[tag=dv_kpart] times 10 60 20
title @a[tag=dv_kpart] subtitle {{"text":"Encuentra la llave de la reja. Algo se arrastra ahí abajo.","color":"gray","italic":true}}
title @a[tag=dv_kpart] title {{"text":"LAS CATACUMBAS","color":"#9a9a9a"}}
kill @e[type=interaction,tag=dv_cllave]
kill @e[type=item_display,tag=dv_cllave_vis]
kill @e[type=interaction,tag=dv_creja]
execute in minecraft:overworld run summon minecraft:item_display {kx + 1}.5 {Y0 + 1}.4 {kz + 1}.5 {{Tags:["dv_cllave_vis"],brightness:{{sky:12,block:12}},billboard:"vertical",item:{{id:"minecraft:tripwire_hook",Count:1b}},transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f],right_rotation:[0f,0f,0f,1f]}}}}
execute in minecraft:overworld run summon minecraft:interaction {kx + 1}.5 {Y0 + 1} {kz + 1}.5 {{Tags:["dv_cllave","dv_click","dv_npc_click"],width:1.0f,height:1.0f,response:1b}}
execute in minecraft:overworld run summon minecraft:interaction {ex + 3}.5 {Y0 + 1} {ez + 1}.5 {{Tags:["dv_creja","dv_click","dv_npc_click"],width:1.2f,height:3.0f,response:1b}}
execute in minecraft:overworld run fill {ex + 3} {Y0 + 1} {ez} {ex + 3} {Y0 + 3} {ez + 2} minecraft:iron_bars
''')
    F('kevin/cata/tick', f'''
execute if score #kt dv.dev matches 0.. run function canon:kevin/cata/tick2
''')
    F('kevin/cata/tick2', f'''
execute as @a[tag=dv_kpart] unless entity @s[{sel_in}] run tag @s remove dv_kpart
execute unless entity @a[tag=dv_kpart] run function canon:kevin/cata/fail
execute if score #kt dv.dev matches 400 in minecraft:overworld positioned {sx + 1}.5 {Y0 + 1} {sz + 1}.5 run function canon:masa/spawn
execute if score #kt dv.dev matches 560 run playsound canon:masa.rugido hostile @a[tag=dv_kpart] ~ ~ ~ 1 0.8
execute if score #kt dv.dev matches 560 run tellraw @a[tag=dv_kpart] {jt('Algo enorme se mueve detrás de ustedes. Respira.', '#9a9a9a', True)}
scoreboard players operation #c dv.tmp = #kt dv.dev
scoreboard players operation #c dv.tmp %= #560 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:cata.ambient ambient @a[tag=dv_kpart] ~ ~ ~ 1 1
execute as @a[tag=dv_kpart] at @s if predicate canon:azar/1en600 run playsound canon:cata.derrumbe ambient @s ^ ^ ^-8 0.8 1
execute if score #m40 dv.clock matches 0 as @e[type=item_display,tag=dv_cllave_vis] at @s run particle minecraft:soul ~ ~0.3 ~ 0.1 0.2 0.1 0.01 1 normal
execute as @a[tag=dv_kpart] at @s if entity @s[x={ex + 5},y={Y0},z={ez},dx=2,dy=4,dz=3] run function canon:kevin/cata/player_out
execute if score #kt dv.dev matches 12000.. run function canon:kevin/cata/fail
''')
    F('kevin/cata/clicked', kv_say('Busquen la llave. Debe estar en el rincón más lejano. Siempre está en el rincón más lejano.', 100))
    F('kevin/cata/llave_taken', '''
scoreboard players set #ckey dv.dev 1
kill @e[type=item_display,tag=dv_cllave_vis]
playsound canon:cata.reja master @a[tag=dv_kpart] ~ ~ ~ 0.6 1.4
tellraw @a[tag=dv_kpart] [{"selector":"@a[tag=dv_talker]","color":"#e8c9a8"},{"text":" encontró una llave oxidada. Ahora: la reja.","color":"#9a9a9a","italic":true}]
kill @s
''')
    F('kevin/cata/reja_used', f'''
execute if score #ckey dv.dev matches 0 run tellraw @a[tag=dv_talker] {jt('La reja está cerrada con candado. Necesitan una llave.', '#9a9a9a', True)}
execute if score #ckey dv.dev matches 0 run playsound canon:cata.reja master @a[tag=dv_talker] ~ ~ ~ 0.5 0.6
execute if score #ckey dv.dev matches 1 run function canon:kevin/cata/open
''')
    F('kevin/cata/open', f'''
execute in minecraft:overworld run fill {ex + 3} {Y0 + 1} {ez} {ex + 3} {Y0 + 3} {ez + 2} minecraft:air
playsound canon:cata.reja master @a[tag=dv_kpart] ~ ~ ~ 1 1
tellraw @a[tag=dv_kpart] {jt('La reja chirría y se abre. Hay una escalera al fondo. ¡Corran!', '#e8c9a8', True)}
kill @s
''')
    F('kevin/cata/player_out', f'''
tag @s add dv_cout
tag @s remove dv_kpart
function canon:util/tp_return
effect give @s minecraft:darkness 3 0 true
stopsound @s ambient canon:cata.ambient
execute unless entity @a[tag=dv_kpart] run function canon:kevin/cata/win
''')
    F('kevin/cata/win', f'''
execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn
playsound canon:cata.derrumbe master @a[tag=dv_cout] ~ ~ ~ 1 0.8
tellraw @a[tag=dv_cout] {jt('Detrás de ustedes, el túnel se derrumba. Kevin gritaba: «¡Vayan, ya los alcanzo!»', '#9a9a9a', True)}
execute if score #kprog dv.dev matches ..3 run tellraw @a[tag=dv_cout] {jt('Kevin no salió.', '#c94a4a', True)}
execute if score #kprog dv.dev matches 5.. run tellraw @a[tag=dv_cout] {jt('Un rato después, Kevin sale de una alcantarilla, lleno de polvo, riéndose.', '#ffb347', True)}
execute if score #kprog dv.dev matches 5.. run scoreboard players set #kevcd dv.dev 30
execute if score #kprog dv.dev matches ..3 run function canon:kevin/dias/begin
tag @a remove dv_cout
function canon:kevin/cata/cleanup
''')
    F('kevin/cata/fail', f'''
execute as @a[{sel_in}] at @s run function canon:util/tp_return
execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn
tellraw @a[tag=dv_kpart] {jt('Las catacumbas los escupen afuera. Kevin quedó abajo... por ahora.', '#9a9a9a', True)}
scoreboard players set #kevcd dv.dev 600
function canon:kevin/cata/cleanup
''')
    F('kevin/cata/cleanup', '''
execute as @e[type=zombie,tag=dv_masa] at @s run function canon:rig/despawn
kill @e[type=interaction,tag=dv_cllave]
kill @e[type=item_display,tag=dv_cllave_vis]
kill @e[type=interaction,tag=dv_creja]
tag @a remove dv_kpart
tag @a remove dv_cout
scoreboard players set #kev dv.dev 0
''')
    # la Masa
    F('masa/spawn', rig_summon(['dv_masa'], 'La Masa', '#8e3b3f', head=False, scale=1.4) + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_masa,distance=..2,limit=1,sort=nearest] at @s run function canon:masa/init')
    F('masa/init', f'''
function canon:rig/init_common
{set_cmd('body', CMD['masa_idle'])}
playsound canon:masa.rugido hostile @a[distance=..48] ~ ~ ~ 1 0.7
''')
    F('masa/tick', '''
tag @a remove dv_wtgt
tag @a[tag=dv_kpart,distance=..80,limit=1,sort=nearest] add dv_wtgt
execute unless score #kev dv.dev matches 3 run function canon:rig/despawn
execute if entity @a[tag=dv_wtgt] run function canon:masa/think
tag @a remove dv_wtgt
''')
    F('masa/think', '''
execute facing entity @a[tag=dv_wtgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.085 run tp @s ~ ~ ~ ~ ~
scoreboard players add @s dv.timer 1
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #40 dv.math
execute if score #c dv.tmp matches 0 run playsound canon:masa.arrastre hostile @a[distance=..24] ~ ~ ~ 1 1
execute if score #c dv.tmp matches 0 run particle minecraft:block minecraft:redstone_block ~ ~0.3 ~ 0.6 0.2 0.6 0 12 normal
scoreboard players remove @s[scores={dv.timer2=1..}] dv.timer2 1
execute if entity @a[tag=dv_wtgt,distance=..1.8] unless score @s dv.timer2 matches 1.. run function canon:masa/hit
''')
    F('masa/hit', '''
scoreboard players set @s dv.timer2 25
damage @a[tag=dv_wtgt,limit=1] 6 minecraft:mob_attack by @s
effect give @a[tag=dv_wtgt] minecraft:slowness 3 2 true
playsound canon:masa.rugido hostile @a[distance=..16] ~ ~ ~ 1 1.3
''')
    return sx, sz, X0, Z0, Y0



def gen_dias():
    K = CMD
    F('kevin/dias/begin', '''
scoreboard players set #kprog dv.dev 4
scoreboard players set #kdays dv.dev 1
execute store result score #kday_last dv.dev run time query day
scoreboard players set #kfakecd dv.dev 120
''')
    F('kevin/dias/second', f'''
execute store result score #kday dv.tmp run time query day
execute unless score #kday dv.tmp = #kday_last dv.dev run function canon:kevin/dias/new_day
execute if score #kfakecd dv.dev matches 1.. run scoreboard players remove #kfakecd dv.dev 1
execute if score #kfakecd dv.dev matches ..0 unless entity @e[type=zombie,tag=dv_kfake] as @a[gamemode=!spectator,predicate=canon:en_superficie,predicate=canon:de_noche,limit=1,sort=random] at @s if predicate canon:azar/1en60 run function canon:kevin/dias/fake_spawn
''')
    F('kevin/dias/new_day', f'''
scoreboard players operation #kday_last dv.dev = #kday dv.tmp
scoreboard players add #kdays dv.dev 1
execute if score #kdays dv.dev matches 2 run tellraw @a {jt('Día 2 sin Kevin. Su celular suena apagado. De noche alguien grita tu nombre con su voz.', '#ffb347', True)}
execute if score #kdays dv.dev matches 3 run tellraw @a {jt('Día 3. Encuentras una gorra negra en la puerta, mojada de barro. Esta noche no salgas.', '#ffb347', True)}
execute if score #kdays dv.dev matches 4.. run function canon:kevin/dias/return
''')
    F('kevin/dias/return', f'''
scoreboard players set #kprog dv.dev 5
scoreboard players set #kdays dv.dev 0
scoreboard players set #kevcd dv.dev 0
execute as @e[type=zombie,tag=dv_kfake] at @s run function canon:rig/despawn
execute as @a[gamemode=!spectator,predicate=canon:en_superficie,limit=1,sort=random] at @s run function canon:kevin/dias/return_here
''')
    F('kevin/dias/return_here', f'''
function canon:kevin/arrive_here
execute as @e[type=zombie,tag=dv_kevin,limit=1] at @s run function canon:kevin/dias/return_say
''')
    F('kevin/dias/return_say', chat('Kevin', '#ffb347', '¡EYYYY! ¿Me extrañaron? Tres días perdido. Salí por una alcantarilla. Comí cosas que no voy a contar. Jajaja.', '@a') + '''
playsound canon:kevin.hey neutral @a[distance=..32] ~ ~1.6 ~ 1 1
function canon:kevin/laugh
title @a times 10 70 20
title @a subtitle {"text":"Ahora es más chistoso que nunca. Lástima.","color":"#ffd27a","italic":true}
title @a title {"text":"KEVIN VOLVIÓ","color":"#ffb347","bold":true}
''')
    F('kevin/dias/fake_spawn', '''
scoreboard players set #kfakecd dv.dev 240
scoreboard players set #ok dv.tmp 0
execute positioned ^ ^ ^22 run function canon:util/spot_search
execute if score #ok dv.tmp matches 0 positioned ^ ^ ^-18 run function canon:util/spot_search
execute if score #ok dv.tmp matches 1 at @e[type=marker,tag=dv_spot,limit=1] run function canon:kevin/dias/fake_summon
kill @e[type=marker,tag=dv_spot]
''')
    F('kevin/dias/fake_summon', rig_summon(['dv_kfake'], 'Kevin', '#ffb347') + '\n'
      'execute as @e[type=zombie,tag=dv_new,tag=dv_kfake,distance=..2,limit=1,sort=nearest] at @s run function canon:kevin/dias/fake_init')
    F('kevin/dias/fake_init', f'''
function canon:rig/init_common
{set_cmd('body', K['kevin_idle'])}
{head(K['kevin_cabeza_neutral'])}
function canon:x/add_bubble
''')
    F('kevin/dias/fake_tick', f'''
function canon:x/links_follow
tag @a remove dv_wtgt
tag @a[gamemode=!spectator,distance=..64,limit=1,sort=nearest] add dv_wtgt
execute unless entity @a[tag=dv_wtgt] run function canon:rig/despawn
execute if score #m4 dv.clock matches 0 run function canon:x/face
scoreboard players add @s dv.timer 1
scoreboard players operation #c dv.tmp = @s dv.timer
scoreboard players operation #c dv.tmp %= #60 dv.math
execute if score #c dv.tmp matches 1 run playsound canon:kevin.hey hostile @a[distance=..48] ~ ~1.6 ~ 1 0.92
execute if score #c dv.tmp matches 1 run function canon:kevin/dias/fake_call
execute if entity @a[tag=dv_wtgt,distance=..7] run function canon:kevin/dias/fake_reveal
execute if score @s dv.timer matches 800.. run function canon:rig/vanish
tag @a remove dv_wtgt
''')
    F('kevin/dias/fake_call', bubble('dv_xbubble', '¡Eyy! ¡Por aquí! ¡Ven!', '#ffd27a', 50))
    F('kevin/dias/fake_reveal', f'''
{head(K['kevin_cabeza_drogado'])}
playsound canon:miron.grito master @a[distance=..12] ~ ~ ~ 1 0.8
execute as @a[distance=..12] at @s run function canon:x/jumpscare
tellraw @a[distance=..12] {jt('Eso no era Kevin.', '#c94a4a', True)}
function canon:rig/vanish
''')


# =================================================================== NICOLÁS

INSULTOS = [
    'Nadie te va a extrañar aquí abajo.',
    'Cava, cava... estás cavando tu propia tumba.',
    '¿Crees que eres especial? Eres un chiste.',
    'Todos se ríen de ti cuando no estás.',
    'Mírate. Das pena.',
    'Aquí abajo nadie oye tus gritos.',
    'Eres lento. Eres débil. Eres mío.',
    'Tus amigos ya se fueron sin ti.',
    'Hueles a miedo.',
    'No eres nadie. Nunca lo fuiste.',
    '¿Por qué sigues intentando? Ya perdiste.',
    'Corre, gordito... ah no, ese soy yo. Jajaja.',
]



KEVIN_MODELS = (['kevin_' + n for n in ['idle', 'walk_a', 'walk_b', 'dance_a', 'dance_b', 'laugh', 'offer']]
                + ['kevin_cabeza_' + n for n in ['neutral', 'risa', 'drogado', 'miedo']])
FIESTERO_MODELS = [f'fiestero_{i}_' + n for i in range(3) for n in ['dance_a', 'dance_b', 'stare']]
ALTO_MODELS = ['alto_' + n for n in ['idle', 'walk_a', 'walk_b', 'reach']]
MASA_MODELS = ['masa_idle', 'masa_a', 'masa_b']


def build(c):
    shim.use(c)
    # CMD fijos (2.1.0): 7320115..7320125 Kevin, 133..141 fiesteros, 144..147 Alto, 148..150 Masa
    shim.models(KEVIN_MODELS, 7320115)
    shim.models(FIESTERO_MODELS, 7320133)
    shim.models(ALTO_MODELS, 7320144)
    shim.models(MASA_MODELS, 7320148)
    models_kevin()
    models_fiesteros()
    models_alto()
    models_masa()
    c.objective('dv.kv', 'trigger')
    c.objective('dv.kpcd')
    for n in (2, 3, 4, 8, 10, 12, 20, 24, 40, 60, 560):
        c.const(n)
    c.on('load', '''
execute unless score #kprog dv.dev matches -999999..999999 run scoreboard players set #kprog dv.dev 0
execute unless score #kdays dv.dev matches -999999..999999 run scoreboard players set #kdays dv.dev 0
execute unless score #kev dv.dev matches -999999..999999 run scoreboard players set #kev dv.dev 0
execute unless score #kt dv.dev matches -999999..999999 run scoreboard players set #kt dv.dev 0
execute unless score #kevcd dv.dev matches -999999..999999 run scoreboard players set #kevcd dv.dev 600
execute unless score #cata_built dv.build matches 0.. run scoreboard players set #cata_built dv.build 0
''')
    c.on('player', '''
scoreboard players enable @s dv.kv
execute if score @s dv.kv matches 1.. run function canon:kevin/choice
''')
    c.on('second', '''
scoreboard players remove @a[scores={dv.kpcd=1..}] dv.kpcd 1
execute if score #kevcd dv.dev matches 1.. run scoreboard players remove #kevcd dv.dev 1
execute if score #kevin dv.cfg matches 1 run function canon:kevin/g/run
execute unless score #kevin dv.cfg matches 1 run function canon:kevin/g/off
execute as @a[tag=dv_kpart] unless score #kev dv.dev matches 1.. run tag @s remove dv_kpart
''')
    c.on('tick', '''
execute if score #kev dv.dev matches 1.. run function canon:kevin/ev/tick
execute if score #cata_built dv.build matches 1 run function canon:kevin/cata/build_try
''')
    c.npc('dv_kevin', 'kevin/tick')
    c.npc('dv_kfake', 'kevin/dias/fake_tick')
    c.npc('dv_fiestero', 'kevin/fiesta/dancer_tick')
    c.npc('dv_alto', 'alto/tick')
    c.npc('dv_masa', 'masa/tick')
    c.click('dv_nota', 'kevin/bosque/nota_taken')
    c.click('dv_cllave', 'kevin/cata/llave_taken')
    c.click('dv_creja', 'kevin/cata/reja_used')
    c.brain_click('dv_kev_click', 'zombie', 'dv_kevin', 'kevin/clicked', 'kevin/attacked')
    c.frames('dv_kevin', 'kevin/frames')
    c.frames('dv_kfake', 'kevin/frames')
    c.frames('dv_fiestero', 'rig/frames/fiestero')
    c.frames('dv_alto', 'alto/frames')
    c.frames('dv_masa', 'rig/frames/masa')
    F('kevin/frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if entity @s[tag=dv_kdance] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 3
execute if entity @s[tag=dv_kdance] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 4
execute if entity @s[tag=dv_klaugh] run scoreboard players set #frame dv.tmp 5
execute if entity @s[tag=dv_koffer] run scoreboard players set #frame dv.tmp 6
''')
    F('alto/frames', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #12 dv.math
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 0..5 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_xwalk] if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 2
execute if entity @s[tag=dv_areach] run scoreboard players set #frame dv.tmp 3
''')
    F('rig/frames/fiestero', '''
scoreboard players set #frame dv.tmp 0
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #10 dv.math
execute if score #c dv.tmp matches 5..9 run scoreboard players set #frame dv.tmp 1
execute if entity @s[tag=dv_fstare] run scoreboard players set #frame dv.tmp 2
''')
    F('rig/frames/masa', '''
scoreboard players operation #c dv.tmp = @s dv.anim
scoreboard players operation #c dv.tmp %= #24 dv.math
execute if score #c dv.tmp matches 6..11 run scoreboard players set #frame dv.tmp 1
execute if score #c dv.tmp matches 18..23 run scoreboard players set #frame dv.tmp 2
''')
    biomes = ['forest', 'flower_forest', 'birch_forest', 'dark_forest', 'old_growth_birch_forest', 'old_growth_pine_taiga',
              'old_growth_spruce_taiga', 'taiga', 'snowy_taiga', 'jungle', 'sparse_jungle', 'bamboo_jungle', 'windswept_forest',
              'cherry_grove', 'mangrove_swamp', 'grove', 'swamp']
    c.json('data/canon/predicates/en_bosque.json', {'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:location_check', 'predicate': {'biome': 'minecraft:' + b}} for b in biomes]})
    gen_kevin()
    gen_fiesta()
    gen_bosque()
    gen_cata()
    gen_dias()
    for cmd, d in [('/function canon:admin/spawn/kevin', 'Traer a Kevin'),
                   ('/function canon:admin/kevin/fiesta', 'Kevin: empezar la fiesta'),
                   ('/function canon:admin/kevin/bosque', 'Kevin: empezar el bosque'),
                   ('/function canon:admin/kevin/catacumbas', 'Kevin: bajar a las catacumbas'),
                   ('/function canon:admin/kevin/tres_dias', 'Kevin: empezar los 3 días'),
                   ('/function canon:admin/kevin/volver', 'Kevin: terminar los 3 días'),
                   ('/function canon:admin/kevin/parar', 'Detener el evento de Kevin'),
                   ('/function canon:admin/kevin/reiniciar', 'Reiniciar la historia de Kevin')]:
        c.admin(cmd, d)
    F('admin/spawn/kevin', 'execute positioned ^ ^ ^2 run function canon:kevin/summon\nexecute as @e[type=zombie,tag=dv_kevin,distance=..4,limit=1,sort=nearest] at @s run function canon:kevin/greet')
    F('admin/kevin/fiesta', 'execute as @e[type=zombie,tag=dv_kevin,limit=1,sort=nearest] at @s run function canon:kevin/fiesta/start')
    F('admin/kevin/bosque', 'tag @s add dv_ktalk\nexecute as @e[type=zombie,tag=dv_kevin,limit=1,sort=nearest] at @s run function canon:kevin/bosque/start\ntag @s remove dv_ktalk')
    F('admin/kevin/catacumbas', 'tag @s add dv_ktalk\nexecute as @e[type=zombie,tag=dv_kevin,limit=1,sort=nearest] at @s run function canon:kevin/cata/prep\ntag @s remove dv_ktalk')
    F('admin/kevin/tres_dias', 'execute as @e[type=zombie,tag=dv_kevin] at @s run function canon:rig/despawn\nfunction canon:kevin/dias/begin\ntellraw @s {"text":"[Canon Event] Empiezan los 3 días sin Kevin.","color":"dark_gray"}')
    F('admin/kevin/volver', 'function canon:kevin/dias/return')
    F('admin/kevin/parar', 'function canon:kevin/ev/abort\ntellraw @s {"text":"[Canon Event] Evento de Kevin detenido.","color":"dark_gray"}')
    F('admin/kevin/reiniciar', 'scoreboard players set #kprog dv.dev 1\nscoreboard players set #kdays dv.dev 0\ntellraw @s {"text":"[Canon Event] Historia de Kevin reiniciada (fiesta disponible).","color":"dark_gray"}')
